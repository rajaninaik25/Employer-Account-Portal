# Data Model — Employer Account Portal

**Showcase:** WorkflowFox Showcase #2<br>
**Phase:** 8 — Data Model<br>
**Status:** Approved<br>
**Authoritative baselines:** [Business Discovery](../discovery/01-business-discovery.md), [Functional Requirements](../requirements/02-functional-requirements.md), [Domain Model](../domain-model/03-domain-model.md), [Solution Architecture](../architecture/04-solution-architecture.md), [Implementation Design](../design/05-implementation-design.md), [API Specification](../api/06-api-specification.md), [`contracts/openapi.yaml`](../../contracts/openapi.yaml), and [Security Design](../security/07-security-design.md)<br>
**Scope:** Logical and physical data model for the read-only Employer Account 360 MVP

## 1. Executive Summary

The Employer Account Portal owns only the operational data needed to authenticate its fixed sample users, maintain server-side sessions, and enforce the approved local login limits. Salesforce remains authoritative for Employer Account, Employer Contact, and Enrollment business data. The portal does not copy those records into SQLite.

One immutable UUID correlates a portal user with exactly one Salesforce Contact. The Employer Portal generates that UUID; the portal user record and the corresponding Salesforce Contact store the same value. The Contact's standard Account relationship establishes the single authorized Employer Account. The portal does not persist Salesforce Contact or Account record IDs, and the session identifies only the portal user.

The Salesforce reference implementation uses standard Account and Contact fields where their semantics match. It adds only the business-specific fields needed for Employer/Group ID, Employer Status, and portal correlation. Enrollment is represented by a small custom object, `Enrollment__c`, with one required Account lookup and the five approved display fields. It does not introduce Member, Employee, Plan, Policy, Benefit, or Coverage objects.

Salesforce source records are translated inside the adapter into technology-neutral domain models, then into the approved API models. Source field names and record IDs stop at the adapter boundary. Enrollment Summary is calculated from a complete validated Enrollment collection and is never persisted.

No application code, SQL, migration, Salesforce metadata, or source-system change is created in this phase.

## 2. Data Modeling Principles

1. **Ownership precedes structure.** The portal owns identity/session operations; Salesforce owns employer business data.
2. **Representations are not entities.** A Salesforce object, persistence row, domain object, and API DTO can represent related information without becoming one shared model.
3. **The adapter is the source boundary.** Salesforce API names, record IDs, relationship fields, and source validation remain inside the Salesforce adapter.
4. **Correlation is logical, not record-ID coupling.** A stable UUID connects the portal user to a Contact without making the portal dependent on Salesforce record identity.
5. **Authorization is re-derived.** A session resolves a portal user; the current user record supplies the correlation UUID; Salesforce supplies the Contact-to-Account relationship.
6. **No second business source of truth.** Account, Contact, and Enrollment data is processed transiently and not stored in SQLite.
7. **Incomplete is not empty.** Invalid, truncated, or unavailable source collections cannot be modeled as confirmed empty data.
8. **The model remains intentionally small.** Display strings are acceptable where normalization would add unapproved entities or behavior.

The representation path is:

```text
Salesforce Account
        ↓ Salesforce Adapter source model
EmployerAccount domain model
        ↓ API mapping
EmployerAccount API model
```

The domain and API layers depend on business names, not Salesforce field API names.

## 3. Data Ownership

| Data | Owner / authority | Persistence | Important boundary |
|---|---|---|---|
| Portal User | Employer Portal | SQLite | Not a Salesforce User; stores no Salesforce record ID or employer business data. |
| Portal Session | Employer Portal | SQLite | Stores a session digest and portal-user relationship only. |
| Login throttle entries | Employer Portal | SQLite, short-lived | Security-operational data required by the approved login-abuse controls; not a business entity. |
| Employer Account | Salesforce | Salesforce Account | Retrieved live and never replicated into portal storage. |
| Employer Contact | Salesforce | Salesforce Contact | Includes the standard Account relationship and, where portal-enabled, the correlation UUID. |
| Enrollment Record | Salesforce | Reference custom object `Enrollment__c` | Retrieved live; no portal-owned copy. |
| Enrollment Summary | Application Business Services | Not persisted | Derived from one complete trusted Enrollment collection. |
| Salesforce source models | Salesforce Adapter | Transient memory only | May contain source record IDs needed for relationship traversal; never cross the adapter boundary. |
| Domain models | Application/domain layer | Transient memory only | Technology-neutral business representation. |
| API models | Portal API | HTTP response only | Contract representation defined by `contracts/openapi.yaml`; contains no source record IDs. |
| Salesforce credentials/tokens | Runtime security configuration | Outside source control; token in process memory only | Never stored in SQLite or returned through the Portal API. |

The split ownership of the correlation value is deliberate: the portal owns generation and assignment to a portal user, while Salesforce stores the matching value on the authoritative Contact. Both systems enforce uniqueness; neither treats the UUID as a login credential.

## 4. Conceptual Data Model

```text
Employer Portal                                         Salesforce

Portal User 1 ─────── has ─────── 0..1 active Session
     │
     │ stable Contact correlation UUID
     └──────────────────────────────────────────────┐
                                                    ↓
                                              Contact  *
                                                    │
                                                    │ AccountId
                                                    ↓
                                               Account 1
                                                    │
                                                    ├──── * Contact
                                                    │
                                                    └──── * Enrollment__c

Complete Enrollment collection ── application rule ──> Enrollment Summary
```

Conceptual cardinalities for the MVP:

- each portal user has one correlation UUID and maps to exactly one Salesforce Contact;
- each correlated Contact belongs to exactly one Account;
- one Account has zero or more Contacts;
- one Account has zero or more Enrollment records;
- each Enrollment record belongs to exactly one Account; and
- one complete Enrollment collection, including an empty collection, produces one available summary.

The one-active-session cardinality reflects the approved concurrent-session rule. Revoked and expired session history can exist temporarily until cleanup.

## 5. Portal User Model

### 5.1 Logical definition

`PortalUser` is a portal-owned identity record used only for authentication and resolution of the approved Salesforce Contact correlation. It is not an Employer Contact replica and does not represent a Salesforce User.

| Attribute | Logical type | Required | Rule / purpose |
|---|---|---:|---|
| Internal user identifier | UUID | Yes | Portal-generated immutable UUIDv4; primary portal identity and session relationship target. |
| Username | Normalized string | Yes | NFKC-normalized, surrounding whitespace removed, case-folded canonical value; unique; maximum 128 characters. |
| Password hash | Argon2id encoded string | Yes | Non-empty self-describing encoding using the approved Security Design parameters. |
| Enabled status | Boolean | Yes | Disabled users cannot authenticate or continue an authenticated business request. |
| Contact correlation UUID | UUID | Yes | Immutable logical linkage to exactly one Salesforce Contact; unique in the portal. |
| Created timestamp | UTC timestamp | Yes | Records initial creation for controlled seeding and operational review. |
| Updated timestamp | UTC timestamp | Yes | Changes when enabled state, password encoding, or correlation assignment is deliberately changed. |

### 5.2 Prohibited portal-user data

A portal-user record must not store:

- Salesforce username, password, client secret, or access token;
- Salesforce Contact ID, Account ID, User ID, or any other Salesforce record ID;
- Employer Name, Employer/Group ID, employer Status, or Industry;
- Contact name, email, phone, or title;
- Enrollment records or summary values; or
- raw session identifiers.

The Contact correlation UUID is the only approved persistent linkage to Salesforce business data.

## 6. Portal Session Model

### 6.1 Logical definition

`PortalSession` is a server-side authentication record. It identifies one portal user and carries no employer or Salesforce context.

| Attribute | Logical type | Required | Rule / purpose |
|---|---|---:|---|
| Session digest | 32-byte digest | Yes | SHA-256 digest of the random 256-bit cookie value; unique. The raw cookie value is never persisted. |
| Portal user identifier | UUID | Yes | Required relationship to an existing `PortalUser`. |
| Created timestamp | UTC timestamp | Yes | Time the post-authentication session was issued. |
| Last-seen timestamp | UTC timestamp | Yes | Most recent accepted authenticated use, updated according to the approved five-minute write interval. |
| Absolute expiry timestamp | UTC timestamp | Yes | Exactly the configured maximum lifetime after creation; currently eight hours. |
| Revoked timestamp | UTC timestamp or absent | No | Its presence is the authoritative revoked state and records logout, replacement, or administrative invalidation time. |

The idle timeout is evaluated from `last_seen_at`; it is not stored as a second expiry value. This prevents multiple independently mutable timeout representations.

### 6.2 Prohibited session data

A portal session must not store:

- the raw `portal_session` cookie value;
- the Contact correlation UUID;
- Salesforce Contact, Account, Enrollment, or User IDs;
- Employer Account, Contact, or Enrollment business fields;
- an employer authorization claim or selected employer identifier; or
- a Salesforce credential or access token.

Every Employer Account 360 request reloads the current enabled portal user and re-derives the employer context through the correlation chain.

## 7. Salesforce Account Model

The Salesforce Account represents the authoritative Employer Account. The reference implementation uses two standard fields and two custom fields:

| Business attribute | Salesforce field | Choice and reasoning |
|---|---|---|
| Employer Name | `Account.Name` | Standard Account display name has the correct meaning; no duplicate custom name field is needed. |
| Employer / Group ID | `Account.Employer_Group_Id__c` | Custom Text(50), unique. The business identifier is distinct from the Salesforce record ID. It is not marked External ID because the approved correlation and authorization flow does not use it for integration lookup. |
| Status | `Account.Employer_Status__c` | Custom Text(40). No Account-status enumeration is approved, so the model does not invent a restricted picklist taxonomy. |
| Industry | `Account.Industry` | Standard industry picklist has the approved semantic meaning. |

For an Account used by the portal, all four values must be present and non-blank because the approved `EmployerAccount` API model requires them. `Employer_Group_Id__c` is unique across populated values. The Salesforce record `Id` is used transiently inside the adapter to retrieve related records but is not a business identifier and is never exposed or persisted by the portal.

## 8. Salesforce Contact Model

The Salesforce Contact remains the authoritative Employer Contact. Standard Contact fields cover all approved display attributes and the Account relationship.

| Business attribute | Salesforce field | Choice and reasoning |
|---|---|---|
| First Name | `Contact.FirstName` | Standard field; required by the portal representation even though Salesforce can permit it to be blank. |
| Last Name | `Contact.LastName` | Standard field and required display value. |
| Email | `Contact.Email` | Standard field; nullable in the approved API. |
| Phone | `Contact.Phone` | Standard field; nullable in the approved API. |
| Role / Title | `Contact.Title` | Standard job-title field; nullable in the approved API. |
| Employer Account relationship | `Contact.AccountId` | Standard many-to-one Account lookup. Required for the correlated Employer Administrator in this MVP. |
| Portal correlation | `Contact.Portal_Correlation_Id__c` | Custom Text(36), Unique, External ID; stores a canonical UUID string for portal-enabled Contacts. |

`Portal_Correlation_Id__c` is nullable for Contacts that are not portal-enabled. When populated, it must use the canonical lowercase UUID format and match exactly one enabled or deliberately provisioned portal user. Salesforce **Unique** prevents more than one Contact from holding the same non-null value. **External ID** is selected because this is a cross-system correlation key and provides indexed exact-match lookup semantics; it does not imply that Salesforce is the identity owner or that the Contact is a Salesforce User.

The correlation field is readable by the integration identity but is not exposed through the Portal API. The integration identity has no Edit access to it.

## 9. Salesforce Enrollment Model

### 9.1 Reference object

The reference implementation uses `Enrollment__c`, a Salesforce custom object that represents one employee/member enrollment in an employer-sponsored plan for the limited showcase. This API name is a reference-implementation choice, not a claim that Salesforce supplies a universal Enrollment object or that every organization should use this schema.

### 9.2 Fields

| Business attribute | Salesforce field | Type | Choice and reasoning |
|---|---|---|---|
| Enrollment ID | `Enrollment__c.Name` | Auto Number, format such as `ENR-{00000}` | The custom object's record name is configured as a generated, user-visible business identifier. It is not the 18-character Salesforce record ID. A separate duplicate ID field would add no value for this reference data. |
| Employee / Member Display Name | `Enrollment__c.Member_Display_Name__c` | Text(160) | Display-oriented string; no Employee or Member object is approved. |
| Plan Name | `Enrollment__c.Plan_Name__c` | Text(120) | Display-oriented string; no Plan object is approved. |
| Status | `Enrollment__c.Status__c` | Restricted Picklist | Values are exactly `Active`, `Pending`, and `Terminated`, matching the approved domain and API enum. |
| Effective Date | `Enrollment__c.Effective_Date__c` | Date | Represents the approved date-only value without inventing time-zone behavior. |
| Employer Account relationship | `Enrollment__c.Employer_Account__c` | Required Lookup(Account) | Establishes the required many-to-one relationship without adding cascade deletion or parent-controlled lifecycle. |

All six fields are required for Enrollment records used by the portal. The platform Auto Number makes `Name` unique for this reference object. If an actual environment already has a separate authoritative business ID, the adapter may map that approved field instead after a controlled Data Model revision; the API must still receive a business identifier, never `Enrollment__c.Id`.

### 9.3 Account relationship decision

The model selects a **required Lookup(Account)** rather than Master-Detail.

Reasoning:

- the MVP needs a required association for authorization and retrieval, but no Salesforce roll-up summary;
- an Enrollment record should not be cascade-deleted merely because its Account is deleted;
- independent record ownership and sharing are safer defaults for a reference enrollment record; and
- a Lookup keeps the example less prescriptive for organizations whose enrollment lifecycle is not controlled by Account lifecycle.

Trade-off: Lookup does not inherit parent sharing or automatically provide roll-up summaries, so record-level access for the integration identity must be configured explicitly. A Master-Detail relationship would provide stronger lifecycle coupling and parent-controlled sharing but would introduce behavior that is neither required nor desirable for this showcase. Salesforce documents that Master-Detail controls detail security and cascade behavior, while Lookup provides association without those behaviors ([Salesforce relationship overview](https://help.salesforce.com/s/articleView?id=sf.overview_of_custom_object_relationships.htm&language=en_US&type=5)).

## 10. Cross-System Correlation Model

```text
PortalUser.contact_correlation_uuid
        │
        │ exact canonical UUID match
        ↓
Contact.Portal_Correlation_Id__c
        │
        │ standard Contact.AccountId
        ↓
Account.Id
```

### 10.1 Ownership and format

- The Employer Portal generates an RFC 4122 UUIDv4 using a cryptographically secure generator.
- The canonical stored representation is 36 lowercase characters in `8-4-4-4-12` hyphenated form.
- `portal_users.contact_correlation_uuid` is non-null and unique.
- `Contact.Portal_Correlation_Id__c` is Unique and External ID and may be null only for Contacts without portal access.
- The value is an opaque correlation key, not a credential, Salesforce record ID, or user-visible business identifier.

### 10.2 Provisioning and lifecycle

The MVP has no user-administration interface. A controlled seed/provisioning process:

1. generates the UUID in the Employer Portal context;
2. places it on the intended Salesforce Contact through authorized environment setup—not through the read-only portal integration identity;
3. creates the portal user with the same UUID but keeps the user disabled until validation succeeds;
4. verifies exactly one Contact match and one Account relationship; and
5. enables the portal user only after reconciliation.

The UUID is expected to remain immutable for the lifetime of the linkage. Correcting a wrong linkage requires disabling the portal user, updating both systems through a controlled administrative process, validating exact cardinality, and then re-enabling the user. The application never silently replaces or guesses the value.

### 10.3 Why Salesforce record IDs are not persisted

- Salesforce record IDs are source-specific implementation identities, not portal-owned identity.
- Contact replacement, data migration, sandbox refresh, or an alternative system of record can change source record identity without changing the portal-user concept.
- Persisting Account ID on the user or session would bypass the approved Contact-to-Account authorization chain.
- The correlation UUID creates a stable logical boundary while keeping relationship traversal authoritative in Salesforce.
- Avoiding source IDs in SQLite prevents accidental frontend exposure and reduces migration coupling.

The adapter can use `Contact.AccountId`, `Account.Id`, and `Enrollment__c.Employer_Account__c` transiently within one request. Those values never enter portal persistence, domain models, API models, or logs.

## 11. Salesforce Physical Field Mapping

| Business concept | Salesforce object | Salesforce field | Standard / Custom | Type | Required for MVP | Notes |
|---|---|---|---|---|---:|---|
| Internal Account traversal identity | Account | `Id` | Standard | Salesforce ID | Yes, adapter only | Never exposed or persisted by the portal. |
| Employer Name | Account | `Name` | Standard | Text | Yes | Maps to the business display name. |
| Employer / Group ID | Account | `Employer_Group_Id__c` | Custom | Text(50), Unique | Yes | Business identifier; not a Salesforce record ID; not External ID for this MVP. |
| Employer Status | Account | `Employer_Status__c` | Custom | Text(40) | Yes | Non-empty; no unapproved enum. |
| Industry | Account | `Industry` | Standard | Picklist | Yes | Mapped to non-empty business text. |
| Contact First Name | Contact | `FirstName` | Standard | Text | Yes for displayed Contacts | Source can permit null, but the API cannot; invalid record makes the Contacts section unavailable. |
| Contact Last Name | Contact | `LastName` | Standard | Text | Yes | Non-empty for display. |
| Contact Email | Contact | `Email` | Standard | Email | No | Present as API `null` when absent. |
| Contact Phone | Contact | `Phone` | Standard | Phone | No | Present as API `null` when absent. |
| Contact Role / Title | Contact | `Title` | Standard | Text | No | Present as API `null` when absent. |
| Account relationship | Contact | `AccountId` | Standard | Lookup(Account) | Yes for correlated user and displayed set | Adapter-only traversal/filter value; never exposed. |
| Portal correlation UUID | Contact | `Portal_Correlation_Id__c` | Custom | Text(36), Unique, External ID | Yes for portal-enabled Contact | Nullable for other Contacts; adapter-only. |
| Internal Enrollment record identity | Enrollment | `Id` | Standard | Salesforce ID | No for business mapping | May occur in source mechanics; never exposed or persisted. |
| Enrollment ID | Enrollment | `Name` | Standard on custom object | Auto Number | Yes | Reference business ID, for example `ENR-00001`; not Salesforce `Id`. |
| Member display name | Enrollment | `Member_Display_Name__c` | Custom | Text(160) | Yes | Display string; no Member/Employee entity. |
| Plan name | Enrollment | `Plan_Name__c` | Custom | Text(120) | Yes | Display string; no Plan entity. |
| Enrollment Status | Enrollment | `Status__c` | Custom | Restricted Picklist | Yes | `Active`, `Pending`, `Terminated` only. |
| Effective Date | Enrollment | `Effective_Date__c` | Custom | Date | Yes | Maps to ISO 8601 date-only API value. |
| Employer relationship | Enrollment | `Employer_Account__c` | Custom | Required Lookup(Account) | Yes | Adapter-only retrieval/filter value; never exposed. |

This is the complete reference field set for the MVP. Additional Salesforce fields are neither queried nor mapped merely because they exist.

## 12. Portal SQLite Physical Model

SQLite stores UTC timestamps as canonical ISO 8601 text with a `Z` suffix. UUIDs use canonical lowercase text. Booleans use SQLite integer values constrained to `0` or `1`. These are physical storage choices; no SQL or migration is defined here.

### 12.1 `portal_users`

| Column | SQLite type | Nullability | Uniqueness / indexing | Purpose |
|---|---|---|---|---|
| `id` | TEXT | NOT NULL | Primary key; unique | Canonical portal-user UUIDv4. |
| `username` | TEXT | NOT NULL | Unique index | Canonical NFKC-normalized, trimmed, case-folded login name. |
| `password_hash` | TEXT | NOT NULL | Not indexed | Argon2id encoded value; never logged or committed. |
| `enabled` | INTEGER | NOT NULL | Not indexed at showcase scale | Boolean authentication/authorization state. |
| `contact_correlation_uuid` | TEXT | NOT NULL | Unique index | Canonical UUID matching `Contact.Portal_Correlation_Id__c`. |
| `created_at` | TEXT | NOT NULL | Not indexed | UTC creation timestamp. |
| `updated_at` | TEXT | NOT NULL | Not indexed | UTC timestamp of last controlled change. |

The username and correlation unique indexes enforce the two critical portal-side identity invariants. An index on `enabled` would have low selectivity and no useful MVP query path.

### 12.2 `portal_sessions`

| Column | SQLite type | Nullability | Uniqueness / indexing | Purpose |
|---|---|---|---|---|
| `session_digest` | BLOB | NOT NULL | Primary key; unique | Exact 32-byte SHA-256 digest used for session lookup. |
| `portal_user_id` | TEXT | NOT NULL | Foreign key to `portal_users.id`; indexed; partial unique index for non-revoked rows | Identifies the current portal user and enforces one active session per user. |
| `created_at` | TEXT | NOT NULL | Not indexed | UTC post-authentication creation time. |
| `last_seen_at` | TEXT | NOT NULL | Not indexed | UTC time used for idle-timeout evaluation. |
| `absolute_expires_at` | TEXT | NOT NULL | Indexed | Supports expiry validation and cleanup. |
| `revoked_at` | TEXT | NULL | Indexed for cleanup | Presence means revoked; absence means not explicitly revoked. |

The foreign key prevents orphan sessions. Login atomically revokes the existing active row before inserting a new row. Expired but not yet cleaned rows are also revoked during login/session evaluation so the active-session unique invariant remains accurate.

### 12.3 `login_attempts`

The approved Security Design requires SQLite-backed rolling login limits. This narrow operational table is therefore necessary even though it is not a domain entity.

| Column | SQLite type | Nullability | Uniqueness / indexing | Purpose |
|---|---|---|---|---|
| `id` | INTEGER | NOT NULL | Primary key | Internal event-row identity. |
| `scope` | TEXT | NOT NULL | Composite index with `subject_key` and `attempted_at` | Identifies `username` failure scope or `ip` attempt scope. |
| `subject_key` | TEXT | NOT NULL | Composite index with `scope` and `attempted_at` | Canonical username or trusted client IP used only for rate-limit evaluation. |
| `attempted_at` | TEXT | NOT NULL | Composite rolling-window index | UTC attempt time. |
| `expires_at` | TEXT | NOT NULL | Cleanup index | Deletes the entry after the longest applicable rolling window. |

Only qualifying security events are retained: username-scope rows for failed attempts and IP-scope rows for all attempts. Successful authentication removes current username-scope rows; IP rows expire normally. The table contains no password, hash, session, correlation UUID, Salesforce value, or business data.

## 13. Domain Model Mapping

Salesforce adapter-private source models may contain source fields and relationship IDs. Domain models contain only approved business values.

### 13.1 `EmployerAccount`

| Salesforce source | Domain property | Transformation |
|---|---|---|
| `Account.Name` | `EmployerAccount.name` | Require non-empty trimmed text. |
| `Account.Employer_Group_Id__c` | `EmployerAccount.employer_group_id` | Require non-empty business identifier; preserve value. |
| `Account.Employer_Status__c` | `EmployerAccount.status` | Require non-empty text; do not invent enum normalization. |
| `Account.Industry` | `EmployerAccount.industry` | Require non-empty display text. |

`Account.Id` is used for adapter traversal and is not part of `EmployerAccount`.

### 13.2 `EmployerContact`

| Salesforce source | Domain property | Transformation |
|---|---|---|
| `Contact.FirstName` | `EmployerContact.first_name` | Require non-empty text. |
| `Contact.LastName` | `EmployerContact.last_name` | Require non-empty text. |
| `Contact.Email` | `EmployerContact.email` | Validate email syntax when present; otherwise `None`. |
| `Contact.Phone` | `EmployerContact.phone` | Preserve bounded text when present; otherwise `None`. |
| `Contact.Title` | `EmployerContact.role_title` | Preserve bounded text when present; otherwise `None`. |

`Contact.Id`, `Contact.AccountId`, and `Contact.Portal_Correlation_Id__c` are not part of the displayed domain model. They remain adapter authorization/traversal values.

### 13.3 `EnrollmentRecord`

| Salesforce source | Domain property | Transformation |
|---|---|---|
| `Enrollment__c.Name` | `EnrollmentRecord.enrollment_id` | Require generated non-empty business ID. |
| `Enrollment__c.Member_Display_Name__c` | `EnrollmentRecord.member_display_name` | Require non-empty bounded text. |
| `Enrollment__c.Plan_Name__c` | `EnrollmentRecord.plan_name` | Require non-empty bounded text. |
| `Enrollment__c.Status__c` | `EnrollmentRecord.status` | Accept exactly `Active`, `Pending`, or `Terminated`. |
| `Enrollment__c.Effective_Date__c` | `EnrollmentRecord.effective_date` | Convert Salesforce Date to a date-only domain value. |

`Enrollment__c.Id` and `Enrollment__c.Employer_Account__c` remain adapter-private.

## 14. API Model Mapping

The application composes domain objects and explicit section states into the authoritative OpenAPI contract. It does not serialize domain objects implicitly.

| Domain/application value | API property | Rule |
|---|---|---|
| `EmployerAccount.name` | `employer.employerName` | Required, non-null, non-empty. |
| `EmployerAccount.employer_group_id` | `employer.employerGroupId` | Business identifier only; never Account `Id`. |
| `EmployerAccount.status` | `employer.status` | Required string; no unapproved enum. |
| `EmployerAccount.industry` | `employer.industry` | Required string. |
| `EmployerContact.first_name` | `contacts.items[].firstName` | Required for every available item. |
| `EmployerContact.last_name` | `contacts.items[].lastName` | Required for every available item. |
| `EmployerContact.email` | `contacts.items[].email` | String or `null`. |
| `EmployerContact.phone` | `contacts.items[].phone` | String or `null`. |
| `EmployerContact.role_title` | `contacts.items[].roleTitle` | String or `null`. |
| `EnrollmentRecord.enrollment_id` | `enrollment.items[].enrollmentId` | Business ID only; never Salesforce `Id`. |
| `EnrollmentRecord.member_display_name` | `enrollment.items[].memberDisplayName` | Required string. |
| `EnrollmentRecord.plan_name` | `enrollment.items[].planName` | Required string. |
| `EnrollmentRecord.status` | `enrollment.items[].status` | Approved enum value. |
| `EnrollmentRecord.effective_date` | `enrollment.items[].effectiveDate` | ISO 8601 `YYYY-MM-DD`. |

Application state, rather than source nulls, selects the `available`, `empty`, or `unavailable` Contact/Enrollment schema. An available collection contains one or more items, empty contains none, and unavailable contains no partial items. No source ID or correlation value is mapped into the API.

## 15. Enrollment Summary Derivation

```text
Complete validated Enrollment records
        ↓ Application business logic
Enrollment Summary
        ├── total
        ├── active
        ├── pending
        └── terminated
```

The Enrollment Summary is not a Salesforce object, SQLite row, cached aggregate, or independent source of truth.

Rules:

- `total` equals the number of complete Enrollment records for the authorized Account;
- `active` counts records where status is exactly `Active`;
- `pending` counts records where status is exactly `Pending`;
- `terminated` counts records where status is exactly `Terminated`;
- `total = active + pending + terminated`;
- a confirmed empty Enrollment collection produces four zero values; and
- an unavailable, invalid, truncated, or otherwise incomplete Enrollment collection produces an unavailable Summary with no counts.

The calculation receives technology-neutral domain records and has no Salesforce, persistence, or API dependency.

## 16. Data Validation Rules

### 16.1 Portal User

- `id` and `contact_correlation_uuid` must parse as canonical UUIDv4 values.
- Username normalization must follow the approved NFKC, trim, and case-fold rule before lookup or persistence.
- Username and correlation UUID must each be unique.
- Username is 1–128 characters after normalization.
- `password_hash` must be a valid non-empty Argon2id encoding with approved parameters.
- `enabled` must be a valid Boolean value.
- `created_at` and `updated_at` must be valid UTC timestamps; updated time cannot precede creation time.

### 16.2 Portal Session

- `session_digest` must be exactly 32 bytes and unique; no raw session value may be persisted.
- `portal_user_id` must reference an existing portal user.
- `created_at ≤ last_seen_at < absolute_expires_at` for a usable session.
- `absolute_expires_at` must equal the configured absolute lifetime after creation.
- `revoked_at`, when present, must be a valid UTC timestamp and makes the session unusable.
- At most one non-revoked session row may exist per portal user.
- Idle expiry is evaluated from the approved 30-minute interval and is never treated as a valid active session merely because cleanup has not run.

### 16.3 Salesforce Contact

- A populated correlation field must parse as a canonical lowercase UUID and be unique.
- An authenticated portal user must resolve to exactly one Contact; zero or multiple results fail closed even when metadata claims uniqueness.
- The correlated Contact must have exactly one non-null `AccountId`.
- Every displayed Contact must match the resolved Account.
- First and Last Name must be non-empty for an available Contact section; Email must be syntactically valid when present.

### 16.4 Salesforce Account

- `Account.Id` must identify the one Account resolved through the correlated Contact.
- Name, Employer/Group ID, Status, and Industry must be present and non-empty.
- Employer/Group ID must be unique across populated portal-reference Accounts.
- Status remains a bounded non-empty string because no business taxonomy is approved.
- A response that cannot validate all required Account fields cannot produce a partial Employer Account 360.

### 16.5 Salesforce Enrollment

- Every record must have the resolved Account in `Employer_Account__c`.
- Enrollment ID, Member Display Name, Plan Name, Status, and Effective Date are required.
- Enrollment ID must be unique within the complete returned collection and, for the reference Auto Number, within `Enrollment__c`.
- Status must be exactly `Active`, `Pending`, or `Terminated`.
- Effective Date must parse as a valid date-only value.
- Display strings must be non-empty and within the configured Salesforce field bounds.
- Source paging must complete before the collection is treated as available.

## 17. Data Integrity and Failure Handling

The application does not repair, deduplicate, infer, or silently substitute source data.

| Integrity condition | Required behavior |
|---|---|
| Portal user has a missing/malformed correlation UUID | Reject/fail closed; return no employer data. |
| Duplicate portal correlation UUID | Prevent through the SQLite unique constraint; fail provisioning or startup validation. |
| No Salesforce Contact matches | Fail the authorized context with `403 ACCESS_UNAVAILABLE`. |
| Multiple Contacts match | Fail closed as a correlation-integrity violation, even if Salesforce uniqueness was expected. |
| Correlated Contact has no Account | Fail closed with no Account, Contacts, or Enrollment data. |
| Contact resolves an unexpected/ambiguous Account relationship | Fail closed; do not guess or accept a client-selected Account. |
| Required Account value is missing, malformed, or not trusted | Fail the complete Account 360; return the approved parent unavailable response according to cause. |
| A displayed Contact lacks required name data or violates source validation | Mark the entire Contacts section unavailable; do not return a partial Contact list. |
| Enrollment has an invalid status or malformed date | Mark Enrollment and Enrollment Summary unavailable; preserve authorized Account and valid Contacts. |
| Salesforce response or paging is incomplete | Treat the affected child collection as unavailable; never treat truncation as a complete or empty collection. |
| Duplicate Enrollment business IDs occur in a returned collection | Treat Enrollment as invalid and unavailable; do not deduplicate; no Summary counts. |
| Confirmed zero Contacts | Return Contacts `empty`. |
| Confirmed zero Enrollment records | Return Enrollment `empty` and Summary `available` with zero counts. |

Integrity events use the approved request ID and safe category. They do not log correlation values, Salesforce record IDs, or business payloads.

## 18. Sensitive Data Classification

This is a lightweight engineering classification. Business Discovery has not established a legal or regulatory classification, so this document does not claim one.

| Class | Examples | Storage implication | Logging implication |
|---|---|---|---|
| Authentication-sensitive | Password hash, session digest, raw password/session value | Hash/digest only in restricted SQLite; raw values transient only; never source controlled. | Never log, even in debug/error paths. |
| Security-sensitive internal | Correlation UUID, source record IDs, Salesforce client secret and token | Correlation UUID in portal user and Contact; source IDs transient in adapter; secrets outside source; token memory only. | Never log values; only safe event categories. |
| Security-operational | Login-attempt username/IP keys and timestamps | Short-lived SQLite rows with cleanup at window expiry. | Log only aggregate/throttled outcome; not raw subject key. |
| Business data | Employer fields, Contact details, Enrollment details | Salesforce authoritative; transient application/API processing only; no SQLite copy. | Do not log payloads or unnecessary field values. |
| Non-sensitive configuration | Timeouts, cookie name, approved source object/field mappings | Typed backend configuration may be committed when no secret is embedded. | May log configuration version/category, not a complete dump. |

The API exposes only the approved business fields and operational request ID. It does not expose authentication-sensitive or security-sensitive internal values.

## 19. Salesforce Permission Matrix

The dedicated integration identity requires object-level Read plus field-level Read for the following minimum set. Create, Edit, and Delete are denied at object level and therefore for every listed field.

| Object | Field | Read | Create | Edit | Delete | Frontend exposure / purpose |
|---|---|:---:|:---:|:---:|:---:|---|
| Account | `Id` | Yes | No | No | No | No; adapter relationship traversal. |
| Account | `Name` | Yes | No | No | No | Yes as `employerName`. |
| Account | `Employer_Group_Id__c` | Yes | No | No | No | Yes as approved business ID. |
| Account | `Employer_Status__c` | Yes | No | No | No | Yes as employer `status`. |
| Account | `Industry` | Yes | No | No | No | Yes as `industry`. |
| Contact | `FirstName` | Yes | No | No | No | Yes. |
| Contact | `LastName` | Yes | No | No | No | Yes. |
| Contact | `Email` | Yes | No | No | No | Yes when present. |
| Contact | `Phone` | Yes | No | No | No | Yes when present. |
| Contact | `Title` | Yes | No | No | No | Yes when present. |
| Contact | `AccountId` | Yes | No | No | No | No; authorization and Account-scoped retrieval. |
| Contact | `Portal_Correlation_Id__c` | Yes | No | No | No | No; exact portal-user correlation. |
| Enrollment__c | `Name` | Yes | No | No | No | Yes as business `enrollmentId`. |
| Enrollment__c | `Member_Display_Name__c` | Yes | No | No | No | Yes. |
| Enrollment__c | `Plan_Name__c` | Yes | No | No | No | Yes. |
| Enrollment__c | `Status__c` | Yes | No | No | No | Yes. |
| Enrollment__c | `Effective_Date__c` | Yes | No | No | No | Yes. |
| Enrollment__c | `Employer_Account__c` | Yes | No | No | No | No; Account-scoped retrieval. |

The integration identity also needs API access and record-level visibility for the representative records, but not `View All Data`, `Modify All Data`, administrative Setup permissions, unrelated objects, or unrelated fields. Because Enrollment uses Lookup rather than Master-Detail, its record-level sharing must be configured explicitly and validated. Relationship fields required only for traversal remain adapter-private.

The field-permission matrix above defines the maximum field surface required by the application. Record-level visibility for Account, Contact, and Enrollment must be validated separately under the target Salesforce sharing model. Field-level permission does not substitute for record-level sharing enforcement.

## 20. Indexing and Data Volume

Approved showcase validation bounds are:

- one Employer Account per authenticated portal user;
- approximately 50 Contacts maximum for the resolved Account; and
- approximately 1,000 Enrollment records maximum for the resolved Account.

These are validation bounds for the reference implementation, not enterprise scalability claims.

### 20.1 Portal indexes

| Data access | Index | Reason |
|---|---|---|
| Username login lookup | Unique `portal_users.username` | Enforces canonical uniqueness and makes login lookup direct. |
| Portal-to-Contact correlation | Unique `portal_users.contact_correlation_uuid` | Enforces one portal user per shared UUID. |
| Session lookup | Primary/unique `portal_sessions.session_digest` | Exact bearer-digest lookup. |
| User session revocation | `portal_sessions.portal_user_id` plus partial uniqueness for non-revoked rows | Supports revoke-all and the one-active-session rule. |
| Session expiry cleanup | `portal_sessions.absolute_expires_at` | Finds expired sessions without scanning all rows. |
| Revocation cleanup | `portal_sessions.revoked_at` | Finds revoked rows eligible for removal. |
| Login rolling window | Composite `login_attempts(scope, subject_key, attempted_at)` | Counts qualifying attempts within each approved window. |
| Login-attempt cleanup | `login_attempts.expires_at` | Removes short-lived limiter rows efficiently. |

### 20.2 Salesforce selectivity

- `Contact.Portal_Correlation_Id__c` is External ID and Unique, providing the required indexed exact-match correlation.
- `Contact.AccountId` and `Enrollment__c.Employer_Account__c` are relationship fields used for Account-scoped retrieval.
- `Account.Employer_Group_Id__c` is unique for data integrity, not for authorization.
- No speculative filtering, search, or additional custom index is introduced.

The adapter must complete any Salesforce paging before returning the bounded collection. If representative measurements exceed the approved response or payload targets, pagination/caching is a new design decision rather than an undocumented data-model change.

## 21. No-Replication Decision

**Decision:** the Employer Portal does not replicate Account, Contact, or Enrollment data into SQLite.

Reasons:

- Salesforce remains the authoritative system of record;
- avoiding copies eliminates synchronization, conflict, freshness, retention, and reconciliation logic;
- live retrieval directly demonstrates modernization around an existing enterprise platform;
- the small MVP does not require an offline business-data store; and
- the portal database remains narrowly responsible for users, sessions, and local security operations.

Trade-off: Account 360 availability and latency depend partly on Salesforce, its API, the network, and source-data quality. The approved partial-failure model mitigates child-section failures, but required Account context still fails when Salesforce cannot provide trusted data. Caching or replication may be considered only in a later production architecture with explicit freshness, authorization, invalidation, privacy, and ownership requirements.

## 22. Data Model Decisions and Trade-offs

| Decision | Reason | Trade-off | Future evolution |
|---|---|---|---|
| Correlation UUID instead of Salesforce Contact ID | Stable logical cross-system key without source-record coupling; supports exact indexed lookup. | Requires coordinated provisioning and uniqueness in two systems. | Replace the source-side mapping while preserving portal identity if the trusted system changes. |
| SQLite portal users/sessions instead of enterprise identity storage | Responsible persistence for a few sample users with uniqueness, sessions, and no external infrastructure. | Single-node scale and portal-owned credential lifecycle. | Replace identity/session repositories with enterprise IdP and production session storage after new requirements. |
| Live Salesforce retrieval instead of replication | Preserves source authority and avoids synchronization complexity. | Availability and latency depend on Salesforce. | Add governed caching/replication only with approved freshness and ownership rules. |
| Required Enrollment Account Lookup instead of Master-Detail | Enforces association without cascade deletion, inherited ownership, or unneeded rollups. | Sharing and integrity must be configured/validated explicitly. | Reconsider Master-Detail only if Account-controlled lifecycle and sharing become actual requirements. |
| Standard fields where semantics match; minimal custom fields otherwise | Reduces unnecessary metadata while preserving exact business meaning. | Custom Account/correlation fields require environment setup and governance. | Map equivalent existing fields through the adapter after validation rather than forcing duplicate fields. |
| Enrollment display strings instead of Member/Employee/Plan entities | Meets the approved display use case without expanding the domain. | Repetition and limited referential normalization. | Introduce normalized entities only through new discovery and requirements. |
| Derived Enrollment Summary instead of persisted counts | Guarantees reconciliation with the complete current collection and avoids another source of truth. | Recalculated on every available response. | Consider source aggregates/cache only for approved production volume and freshness needs. |
| `Enrollment__c.Name` Auto Number as business ID | Smallest model that supplies a stable display identifier distinct from Salesforce `Id`. | Less suitable if an upstream system already owns Enrollment identifiers. | Map an approved external business-ID field when such a source is established. |

## 23. Future Evolution

Without implementing them now, the boundaries support later evolution to:

- enterprise SSO and external identity lifecycle while keeping employer authorization business-oriented;
- multiple employers per user through an explicitly approved authorization relationship rather than a session claim shortcut;
- alternative systems of record by replacing the adapter and correlation-field mapping;
- production relational/distributed session and rate-limit persistence;
- normalized Member, Employee, Plan, Policy, or Coverage concepts only after business discovery establishes them;
- bounded cache or read model with explicit freshness, invalidation, ownership, privacy, and authorization rules;
- larger collections with approved API pagination and summary semantics; and
- stronger data-governance, retention, privacy, lineage, and audit controls for real client data.

Future extensibility does not authorize any of these capabilities in the MVP.

## 24. Resolved Decisions and Environment Validation

### 24.1 Resolved design decisions

The reference implementation decisions are resolved in this document: field names/types, UUID ownership and format, External ID/Unique behavior, required Lookup relationship, Auto Number Enrollment ID, SQLite models/indexes, source-to-domain mappings, API mappings, summary derivation, and failure behavior are not open.

### 24.2 Required environment validation items

The following depend on the actual Salesforce development environment and do not automatically block Data Model approval:

1. Confirm that `Employer_Group_Id__c`, `Employer_Status__c`, `Portal_Correlation_Id__c`, `Enrollment__c`, and the proposed Enrollment field API names do not conflict with existing metadata.
2. Confirm that existing Account `Industry` values and the two custom Account values are populated for every representative portal Account.
3. Confirm that `Enrollment__c.Name` can be configured as Auto Number in the target object; if an existing object already has a Text name or authoritative Enrollment ID field, bring the equivalent mapping back for controlled approval.
4. Confirm `Portal_Correlation_Id__c` can be configured as Text(36), Unique, External ID and that existing populated values are valid and duplicate-free.
5. Confirm the required `Employer_Account__c` Lookup and record-level sharing allow the dedicated integration identity to read only the representative Enrollment records without broad permissions.
6. Confirm the final field-level permission set exactly matches Section 19 and that all unapproved field and mutation tests fail.

### 24.3 Remaining design questions

No unresolved business or reference-design question remains for this phase. A material mismatch discovered during environment validation requires a documented Data Model amendment; it does not authorize an ad hoc source or API change.

## 25. Phase Exit Criteria

Data Model is complete when reviewers have:

- approved portal ownership of users, sessions, and local login-attempt data;
- approved Salesforce ownership of Account, Contact, and Enrollment business data;
- confirmed that persistence, source, domain, and API representations remain distinct;
- approved the portal-generated UUIDv4 correlation, uniqueness, External ID behavior, provisioning, immutability, and fail-closed rules;
- approved the complete Salesforce reference field mapping and required Enrollment Account Lookup;
- approved the `portal_users`, `portal_sessions`, and security-operational `login_attempts` SQLite models and indexes;
- confirmed that no raw session, Salesforce record ID, business-data replica, Salesforce token, or employer claim enters portal persistence;
- approved all source-to-domain and domain-to-API mappings;
- approved non-persisted Enrollment Summary derivation and reconciliation rules;
- approved validation, integrity, failure-handling, classification, and data-volume decisions;
- approved the exact minimum Salesforce field-permission matrix and prohibited broad permissions;
- confirmed that Account, Contact, and Enrollment data is not replicated into SQLite;
- confirmed that no new business entity, application capability, runtime AI feature, SQL, migration, Salesforce metadata, or application code has been introduced; and
- approved progression to User Experience Design.

The Phase 8 Data Model is approved for progression to User Experience Design. Environment-specific Salesforce metadata, sharing, and permission checks remain mandatory validation tasks before implementation is declared complete.
