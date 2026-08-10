# Domain Model — Employer Account Portal

**Showcase:** WorkflowFox Showcase #2  
**Phase:** 3 — Domain Model  
**Status:** Updated for approval  
**Baselines:** [Business Discovery](../discovery/01-business-discovery.md) and [Functional Requirements](../requirements/02-functional-requirements.md)  
**Scope:** Employer Account 360 read-only MVP

## 1. Purpose

This document defines the business concepts, relationships, terminology, and rules needed for the Employer Account 360 MVP. It translates the approved discovery and functional requirements into a technology-agnostic domain language.

This is not an architecture or data-model artifact. It does not define applications, components, services, APIs, storage, schemas, Salesforce queries, integration patterns, authentication technology, or user-interface structure.

## 2. Domain Boundary

The domain is limited to one business capability:

> An authenticated Employer Administrator views a consolidated, read-only representation of one authorized Employer Account, its associated Employer Contacts, and its Enrollment information.

The domain includes:

- the Employer Administrator acting in the portal;
- the Employer Account the administrator is authorized to view;
- Employer Contacts associated with that account;
- Enrollment Records associated with that account;
- a derived Enrollment Summary; and
- the combined Employer Account 360 representation.

The domain excludes all transactional employer services, additional portal use cases, application-level AI, and ownership of the Salesforce-managed business data.

**Traceability:** Business Discovery §§4–5, 7, and 9–12; Functional Requirements UC-001, FR-001–FR-012, and SC-001–SC-006.

## 3. Ubiquitous Language

The following terms are the canonical business language for this showcase.

| Term | Definition | Usage guidance |
|---|---|---|
| **Employer Administrator** | An authenticated representative permitted to view information for an Employer Account. | Describes the business actor and portal role. It does not imply a Salesforce user or Contact. |
| **Employer Account** | The business record representing an employer organization for the Account 360 experience. | Use instead of the unqualified term *Account* when discussing the domain. Salesforce Account is the current source representation, not the domain definition. |
| **Employer Contact** | A person record associated with an Employer Account and included in that account's Contacts information. | Use instead of the generic term *Contact* when business context matters. An Employer Contact is not assumed to be an Employer Administrator. |
| **Enrollment Record** | An occurrence of the approved Enrollment business concept associated with an Employer Account. | Its precise business meaning and attributes still require approval. In the current source it is represented by a Salesforce custom object. |
| **Enrollment Summary** | A read-only, derived description of Enrollment Records for one Employer Account using approved summary rules. | It is derived information, not a separately mastered business record. MVP measures are Total, Active, Pending, and Terminated enrollment counts. |
| **Employer Account 360** | The consolidated read-only business representation containing the Employer Account overview, Employer Contacts, Enrollment Records, and Enrollment Summary. | It is a composed view of domain information, not a new system of record or independent entity. |
| **Authorized Employer Context** | The single Employer Account whose information the authenticated Employer Administrator is permitted to view during the MVP interaction. | Describes the access boundary. It does not prescribe how authentication or authorization is implemented. |
| **Associated** | Related to the Employer Account currently in the Authorized Employer Context. | Inclusion in Contacts or Enrollment requires this relationship to the current account. |
| **Empty** | The trusted source confirms that no associated records exist for a collection. | Empty is a valid business result and is distinct from unavailable. |
| **Unavailable** | The required source information cannot be obtained or confirmed. | Unavailable must result in an exception message; it must not be interpreted as an empty collection. |
| **Read-only** | Information may be viewed but not created, changed, submitted, or deleted through this MVP. | Applies to Employer Account, Employer Contact, and Enrollment information. |
| **Trusted source** | The authoritative source from which the MVP obtains Employer Account, Employer Contact, and Enrollment information. | Salesforce fulfills this role for the reference implementation. This describes system-of-record authority, not organizational data-governance ownership. |

### 3.1 Terms not treated as domain concepts

- **Salesforce Account**, **Salesforce Contact**, and the **Salesforce Enrollment custom object** are source-platform representations of business concepts.
- **SOQL**, Salesforce APIs, endpoints, services, components, databases, caches, and screens are technical concepts to be addressed only in later approved phases.
- **Chatbot**, autonomous agent, workflow, notification, invoice, payment, claim, case, and document are outside this domain boundary.

## 4. Business Entities and Derived Concepts

### DM-001 — Employer Administrator

**Classification:** Business actor and identifiable portal user.

**Definition:** A representative who authenticates to the portal and is authorized to view the MVP Employer Account context.

**Identity:** The Employer Portal owns the Employer Administrator identity. For the MVP, a small fixed set of sample portal users is sufficient. Each sample user has portal credentials and a unique portal-user identifier. The concrete credential storage and password-protection mechanism is deferred to Security Design and Implementation Design.

**Lifecycle in this MVP:** Used only to authenticate the viewing actor and establish one authorized Employer Account context. Self-registration, invitation, password recovery, delegation, account switching, and user administration are outside scope.

**Authoritative ownership:** The Employer Portal owns portal-user identity. An Employer Administrator is not a Salesforce User and does not require a Salesforce user license. For the MVP, each portal user is linked to one Salesforce Employer Contact through a stable shared identifier. The linked Contact provides the business-person association; it does not provide Salesforce login access.

**Traceability:** FR-001, FR-002, SC-002; Business Discovery §§4, 7, 11, and 14 Q4–Q6.

### DM-002 — Employer Account

**Classification:** Business entity.

**Definition:** The business representation of an employer organization whose basic information is shown in Employer Account 360.

**Identity:** Each Employer Account must be distinguishable so authorization and related information can be scoped correctly. The identifier exposed within the domain is not selected in this phase.

**Lifecycle in this MVP:** View-only. Creation, modification, replacement, and deletion are outside scope.

**Authoritative ownership:** Salesforce is the trusted system of record for the reference implementation.

**Attributes:** The MVP uses Employer Name, Employer/Group ID, Status, and Industry from Salesforce. Additional fields are out of scope unless later approved.

**Traceability:** FR-002–FR-004, FR-010–FR-012, SC-001–SC-004.

### DM-003 — Employer Contact

**Classification:** Business entity.

**Definition:** A person record associated with the Employer Account in the current Authorized Employer Context.

**Identity:** Each Employer Contact is identified by its Salesforce record identity and a stable external identifier used to correlate the Contact with the corresponding Employer Portal user when applicable. The correlation identifier is not a login credential and does not make the Contact a Salesforce User.

**Lifecycle in this MVP:** View-only. Contact creation, updates, and deletion are outside scope.

**Authoritative ownership:** Salesforce is the trusted system of record for the reference implementation.

**Important distinction:** Employer Contact and Employer Administrator remain separate concepts. For this MVP, every Employer Administrator is linked to exactly one Employer Contact through a shared stable identifier, but an Employer Contact does not automatically become a portal user. A Salesforce Contact consumes no Salesforce user license merely because it is linked to a portal identity.

**Traceability:** FR-002, FR-005, FR-008–FR-012; AC-002–AC-004 and AC-008.

### DM-004 — Enrollment Record

**Classification:** Business entity with MVP semantics defined for the showcase.

**Definition:** A read-only employee/member benefit-enrollment record associated with the Employer Account in the current Authorized Employer Context. For the MVP, it represents one person's enrollment in an employer-sponsored plan and exists only to demonstrate account-related child data retrieved from Salesforce.

**Identity:** Each presented Enrollment Record has a unique Enrollment identifier within the Salesforce source data and belongs to exactly one Employer Account for the MVP.

**Lifecycle in this MVP:** View-only. Enrollment submission, change, and deletion are outside scope.

**Authoritative ownership:** Salesforce is the trusted system of record. The approved requirements clarify that the current source representation is a Salesforce custom object.

**Approved MVP semantics:** An Enrollment Record represents one employee/member enrollment under the employer group. The MVP uses a deliberately small field set: Enrollment ID, employee/member display name, plan name, enrollment status, and effective date. Supported sample statuses are **Active**, **Pending**, and **Terminated**. These are showcase semantics for representative fictional data, not a universal insurance-domain standard.

**Traceability:** FR-002, FR-006–FR-012; AC-002, AC-003, AC-005, AC-006, and AC-008.

### DM-005 — Enrollment Summary

**Classification:** Derived business concept; not an independently mastered entity.

**Definition:** A summary calculated from the Enrollment Records associated with one Employer Account according to approved business rules.

**Identity:** It is identified by the Employer Account context and the approved set of Enrollment Records and summary rules; it does not require an independent business identity in this MVP.

**Lifecycle in this MVP:** Produced for viewing and never edited directly.

**Derivation:** Only Enrollment Records in the current Authorized Employer Context may contribute. The MVP summary contains **Total Enrollments**, **Active**, **Pending**, and **Terminated** counts. If Salesforce successfully returns no Enrollment Records, all summary counts are zero. If Enrollment data is unavailable, no zero-valued summary may be presented as though it were confirmed data.

**Traceability:** FR-007, FR-008, FR-011; AC-002, AC-005, and AC-008.

### DM-006 — Employer Account 360

**Classification:** Composed business-information concept; not an independently mastered entity.

**Definition:** The coherent, read-only representation of the Employer Account, associated Employer Contacts, associated Enrollment Records, and derived Enrollment Summary.

**Identity:** The representation is scoped by the Authorized Employer Context. It does not establish a new identity separate from the Employer Account.

**Lifecycle in this MVP:** Assembled for viewing. It does not own or mutate the underlying business information.

**Traceability:** UC-001, FR-003–FR-012, SC-001, and SC-003.

## 5. Relationships and Cardinality

The following is a conceptual business relationship view, not an architecture or physical data diagram.

```text
Employer Administrator
        │
        │ is authorized to view in the active MVP context
        ▼
Employer Account
        ├── has 0..* associated Employer Contacts
        └── has 0..* associated Enrollment Records
                              │
                              └── collectively produce 1 Enrollment Summary

Employer Account + Employer Contacts + Enrollment Records + Enrollment Summary
        └── compose 1 Employer Account 360 representation for the active context
```

| ID | Relationship | Cardinality within the MVP | Qualification |
|---|---|---|---|
| REL-001 | Employer Administrator is authorized to view Employer Account | Each MVP Employer Administrator is linked to exactly one Employer Contact and exactly one Employer Account context. | The Employer Portal owns the user identity. A stable shared identifier correlates the portal user with the Salesforce Contact; the Contact's Account relationship establishes the authorized employer context. |
| REL-002 | Employer Account has associated Employer Contacts | One Employer Account to zero or more presented Employer Contacts; each in-scope Employer Contact belongs to exactly one Employer Account for the MVP. | Every Contact included in the view must be associated with the current account. Shared or cross-account Contacts are outside MVP scope. |
| REL-003 | Employer Account has associated Enrollment Records | One Employer Account to zero or more presented Enrollment Records; each Enrollment Record belongs to exactly one Employer Account for the MVP. | The current source represents Enrollment as an Account-related Salesforce custom object. Cross-account Enrollment relationships are outside MVP scope. |
| REL-004 | Enrollment Records produce Enrollment Summary | One in-scope Enrollment collection, including an empty collection, to one summary result. | Summary counts are Total, Active, Pending, and Terminated. A successfully retrieved empty collection produces zero for all counts. An unavailable collection cannot be summarized as if it were empty. |
| REL-005 | In-scope concepts compose Employer Account 360 | One active Employer Account context to one Account 360 representation. | Composition does not transfer authoritative ownership from Salesforce. |

The cardinalities apply only to the approved MVP interaction. They do not establish future multi-employer, shared-contact, delegated-administration, or historical Enrollment behavior.

## 6. Business Rules

| ID | Business rule | Source |
|---|---|---|
| BR-001 | Employer Account 360 information may be viewed only after the Employer Administrator is authenticated. | FR-001; AC-001 |
| BR-002 | An Employer Administrator may view only the Employer Account established as that administrator's Authorized Employer Context. | FR-002; AC-002–AC-003 |
| BR-003 | The MVP interaction has one active Employer Account context. | SC-002; approved requirement clarification Q5 |
| BR-004 | Every Employer Contact presented in Account 360 must be associated with the active Employer Account. | FR-005; AC-002–AC-004 |
| BR-005 | Every Enrollment Record presented in Account 360 must be associated with the active Employer Account. | FR-006; AC-002, AC-003, AC-005 |
| BR-006 | An Enrollment Summary may use only the Enrollment Records in scope for the active Employer Account and the approved summary rules. | FR-007; AC-002, AC-005, AC-008 |
| BR-007 | An empty Contact or Enrollment collection is a valid confirmed result and must remain distinct from unavailable information. | FR-008; AC-004–AC-006 |
| BR-008 | Unavailable Account 360 information must produce an exception message and must not be represented as confirmed empty data. | FR-008, FR-009; approved requirement clarification Q6 |
| BR-009 | Account, Contact, Enrollment Record, and Enrollment Summary information is read-only in the MVP. | FR-010; SC-001; AC-007 |
| BR-010 | Employer Account, Employer Contact, and Enrollment values presented by the MVP must represent the authoritative Salesforce source data. | FR-011; SC-003; AC-008 |
| BR-011 | The Enrollment Summary must reconcile to the authoritative in-scope Enrollment Records and approved summary rules. | FR-007, FR-011; AC-008 |
| BR-012 | Only the approved MVP field sets may be included in Employer Account 360. Account: Employer Name, Employer/Group ID, Status, Industry. Contact: First Name, Last Name, Email, Phone, Role/Title. Enrollment: Enrollment ID, Employee/Member Display Name, Plan Name, Status, Effective Date. | FR-004–FR-006; Requirements §4.1 |
| BR-013 | The business domain must not depend on Salesforce object names, query language, or platform interfaces as its business vocabulary. | FR-012; SC-004 |
| BR-014 | Employer Administrator and Employer Contact are separate business entities. For the MVP, an Employer Administrator must correlate to exactly one Employer Contact through a stable shared identifier; that Contact remains a Salesforce Contact, not a Salesforce User. | Requirements clarification; domain identity decision |
| BR-015 | Salesforce data is retrieved on behalf of the portal through an application/service identity, not through the Employer Administrator's Salesforce identity. End users therefore require no Salesforce login or user license for the MVP. | Approved MVP integration boundary decision |

## 7. States Relevant to the Domain

The MVP requires only the following information states:

| State | Business meaning | Permitted interpretation |
|---|---|---|
| **Available with data** | The trusted source confirms one or more in-scope values or records. | Present the approved information and, for Enrollment, derive the approved summary. |
| **Available and empty** | The trusted source confirms no associated records exist for a collection. | Represent a valid empty collection; use the approved zero-record Enrollment summary rule. |
| **Unavailable** | The source information cannot be obtained or confirmed. | Present an exception message; do not infer zero records or calculate a misleading summary. |
| **Unauthorized** | The Employer Administrator is not permitted to view the requested Employer Account context. | Do not present that employer's Account, Contact, or Enrollment information. |

This state model defines business meaning only. Error types, status codes, message wording, retry behavior, and presentation are later design concerns.

## 8. Source Representation Mapping

This mapping exists only to preserve terminology and source ownership. It is not a logical or physical data model.

| Domain concept | Current Salesforce representation | Mapping status |
|---|---|---|
| Employer Account | Account | Concept confirmed. MVP business fields: Employer Name, Employer/Group ID, Status, Industry. Concrete Salesforce API field names are deferred to the Data Model. |
| Employer Contact | Contact associated with the employer Account | MVP fields: First Name, Last Name, Email, Phone, Role/Title. Each displayed Contact belongs to one Employer Account for the MVP; concrete Salesforce API field names are deferred. |
| Enrollment Record | Account-related custom object | Represents one employee/member benefit enrollment for the MVP. Approved showcase fields: Enrollment ID, Employee/Member Display Name, Plan Name, Status, Effective Date. |
| Enrollment Summary | Derived from in-scope Enrollment Records | Derived counts: Total Enrollments, Active, Pending, and Terminated. It is not a mastered Salesforce record. |
| Employer Administrator | Employer Portal-managed user linked to Salesforce Contact | The portal owns the login identity. A stable shared identifier links a portal user to one Salesforce Contact. The Contact is not a Salesforce User and consumes no Salesforce user license for this relationship. |

## 9. Traceability Matrix

| Approved capability or constraint | Domain concepts | Relationships and rules |
|---|---|---|
| Authenticated and authorized Employer Administrator | DM-001, Authorized Employer Context | REL-001; BR-001–BR-003 |
| Employer Account overview | DM-002, DM-006 | REL-005; BR-002, BR-010, BR-012 |
| Associated Contacts | DM-003, DM-006 | REL-002; BR-004, BR-007, BR-010, BR-012 |
| Enrollment records | DM-004, DM-006 | REL-003; BR-005, BR-007, BR-009, BR-010, BR-012 |
| Useful Enrollment summary | DM-005, DM-006 | REL-004; BR-006, BR-007, BR-011 |
| Empty, unavailable, and unauthorized outcomes | Information states | BR-001, BR-002, BR-007, BR-008 |
| Read-only behavior | All in-scope concepts | BR-009 |
| Salesforce remains authoritative | DM-002–DM-005 | REL-005; BR-010–BR-011 |
| Business-oriented, platform-independent language | Ubiquitous Language | BR-013 |
| Single-context MVP and explicit exclusions | Domain Boundary | REL-001; BR-003 |

## 10. Decisions, Trade-offs, and Alternatives

### Decisions

- **Use business terms as canonical language.** Employer Account, Employer Contact, and Enrollment Record describe the domain; Salesforce names describe the current source representation.
- **Keep Employer Administrator separate from Employer Contact, but explicitly correlate them for the MVP.** The Employer Portal owns login identity; a stable shared identifier links each sample portal user to one Salesforce Contact. The Contact remains a business record and is not a licensed Salesforce User.
- **Treat Enrollment Summary as derived information.** It depends on the associated Enrollment collection and approved rules rather than becoming a second source of truth.
- **Model only business-relevant states.** Empty, unavailable, and unauthorized carry distinct meanings required by the functional requirements.
- **Resolve only the semantics required by the showcase.** Enrollment represents one employee/member benefit enrollment; field sets and summary counts are deliberately minimal; each portal user has one employer context. Broader enterprise semantics remain out of scope.

### Trade-offs

- A platform-independent vocabulary improves reuse across enterprise systems but requires an explicit source-to-domain mapping later.
- Separating portal identity from Salesforce Contact identity avoids Salesforce-user licensing and authentication coupling, while the shared identifier still provides a simple auditable business-person correlation for the MVP.
- A derived Enrollment Summary prevents duplicate authoritative ownership. The MVP uses Total, Active, Pending, and Terminated counts because they are sufficient to demonstrate the pattern without inventing a broader enrollment analytics product.
- Restricting cardinality to the active MVP context keeps the model accurate but does not answer future multi-employer or delegated-administration needs.

### Alternatives considered and not selected

- **Mirror the Salesforce object model as the domain model:** not selected because it would make platform implementation terminology drive the business model.
- **Use Salesforce User accounts for Employer Administrators:** not selected because portal users should not consume Salesforce user licenses or depend on Salesforce authentication. The portal owns the login identity and correlates it to a Salesforce Contact instead.
- **Treat Enrollment Summary as an editable or independently mastered entity:** not selected because the approved requirement defines it as derived from Enrollment Records.
- **Model future portal capabilities:** not selected because they are outside the approved Employer Account 360 scope.

## 11. Assumptions and Open Questions

### Assumptions carried forward

- Salesforce contains usable and authoritative Employer Account, Employer Contact, and Enrollment information for this MVP.
- Enrollment is represented by an Account-related Salesforce custom object.
- One active Employer Account context is sufficient for the MVP.
- The Employer Portal owns a small fixed set of sample user identities for MVP validation.
- Each sample portal user is linked through a stable shared identifier to one Salesforce Contact, and that Contact belongs to one Employer Account.
- Employer Contacts used for portal correlation are not Salesforce Users and do not require Salesforce user licenses.
- The portal-to-Salesforce integration uses an application/service account rather than the end user's Salesforce identity. The credential mechanism and permissions belong to Security Design.
- The MVP uses summary information rather than introducing an independent Enrollment Summary record of authority.
- Workflow Insurance Employer Operations is the accountable business owner for the showcase data; the Salesforce/CRM team is the technical custodian of the source platform.

### Resolved domain questions

1. **What does Enrollment represent?** One employee/member benefit enrollment under an Employer Account, used as representative account-related child data.
2. **Which fields are required?** Account: Employer Name, Employer/Group ID, Status, Industry. Contact: First Name, Last Name, Email, Phone, Role/Title. Enrollment: Enrollment ID, Employee/Member Display Name, Plan Name, Status, Effective Date. Additional fields are out of scope unless later approved.
3. **What defines the Enrollment Summary?** Total Enrollments plus counts for Active, Pending, and Terminated. A confirmed empty collection produces zero for each count.
4. **How are Employer Administrator and Employer Contact related?** They are separate entities. Each MVP portal user carries a stable correlation identifier that matches one Salesforce Contact. The Contact remains a non-user Salesforce business record.
5. **What is the MVP user-to-account cardinality?** Exactly one portal user → one linked Employer Contact → one Employer Account. Multi-employer access and account switching are out of scope.
6. **Can Contact or Enrollment records belong to multiple Employer Accounts?** Not in the MVP. Each displayed Contact and Enrollment Record belongs to exactly one Employer Account.
7. **When is data unavailable rather than empty?** Empty means Salesforce successfully returned zero associated records. Unavailable means the source cannot be reliably obtained, including Salesforce/integration authentication failure, timeout, connectivity failure, source error, or invalid required response data. The business-safe user message is: **“This information is temporarily unavailable. Please try again later.”**
8. **Who owns the data?** Workflow Insurance Employer Operations is the business owner for the showcase; Salesforce remains the system of record and the Salesforce/CRM team acts as technical custodian.

### Decisions intentionally deferred

- Password hashing, session/token handling, secret storage, and login-security controls.
- Salesforce service-account authentication mechanism and least-privilege permissions.
- API shape and transport.
- Physical persistence for the sample portal users.
- Concrete Salesforce custom-object and field API names.
- UI wording beyond the business-safe unavailable-data message.

These belong to later Security, Architecture, Data, API, and UX phases and should not be pulled into the Domain Model.

## 12. Validation Approach

The Domain Model will be validated through:

- **Terminology review:** business stakeholders confirm that each canonical term has one understood meaning and that platform terms do not redefine the domain.
- **Entity review:** each entity is necessary for an approved functional requirement, has a clear business identity, and introduces no new use case.
- **Relationship review:** populated, empty, unavailable, and unauthorized scenarios satisfy the stated relationships and cardinalities.
- **Business-rule review:** BR-001 through BR-015 are testable, internally consistent, and traceable to approved discovery or requirements.
- **Source reconciliation review:** Salesforce subject-matter experts confirm the conceptual Account, Contact, and Enrollment mappings without turning the source schema into the domain model.
- **Scope review:** the model contains no transactional workflow, application-level AI, or excluded portal capability.
- **Human approval:** business, data, and security owners review assumptions and resolve or assign the remaining open questions.

Validation evidence should record reviewers, decisions, corrections, and unresolved items. AI-assisted generation does not replace domain-owner approval.

## 13. Future Extensibility

The model supports future portability by separating stable employer business concepts from their current Salesforce representations. A future approved implementation could map the same concepts to another trusted enterprise platform without redefining the user-facing domain.

This extensibility does not expand the MVP. Additional employer contexts, transactions, user-management capabilities, Enrollment workflows, or application-level AI require new discovery and approved requirements before they may enter the domain.

## 14. Phase Exit Criteria

The Domain Model is complete when reviewers have:

- approved the ubiquitous language and entity definitions;
- confirmed the relationships and MVP cardinalities;
- approved BR-001 through BR-015;
- confirmed the approved MVP Enrollment meaning, field sets, statuses, and summary rules;
- confirmed that the Employer Portal owns user identity and that each Employer Administrator is linked to one Salesforce Contact without becoming a Salesforce User or consuming a Salesforce user license;
- verified traceability to the approved discovery and functional requirements;
- confirmed that no architecture, API, security mechanism, data schema, UX design, or implementation decision has been introduced;
- accepted the validation approach; and
- approved progression to the next lifecycle phase.

Until these criteria are met, this document remains a Domain Model draft and no later major phase should begin.
