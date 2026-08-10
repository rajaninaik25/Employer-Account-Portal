# Domain Model — Employer Account Portal

**Showcase:** WorkflowFox Showcase #2  
**Phase:** 3 — Domain Model  
**Status:** Draft for review  
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
| **Enrollment Summary** | A read-only, derived description of Enrollment Records for one Employer Account using approved summary rules. | It is derived information, not a separately mastered business record. Exact measures remain unresolved. |
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

**Identity:** The administrator must be distinguishable from other portal users. The approved requirements anticipate portal-managed users and a small fixed set of MVP users; the identity mechanism and implementation remain deferred to Security Design and Implementation Design.

**Lifecycle in this MVP:** Used only to establish the viewing actor and authorized context. User registration, invitation, recovery, delegation, and administration are not in scope.

**Authoritative ownership:** Not established by Salesforce Account 360 data. The requirements clarification calls for portal user management, but no technical ownership model is selected here.

**Traceability:** FR-001, FR-002, SC-002; Business Discovery §§4, 7, 11, and 14 Q4–Q6.

### DM-002 — Employer Account

**Classification:** Business entity.

**Definition:** The business representation of an employer organization whose basic information is shown in Employer Account 360.

**Identity:** Each Employer Account must be distinguishable so authorization and related information can be scoped correctly. The identifier exposed within the domain is not selected in this phase.

**Lifecycle in this MVP:** View-only. Creation, modification, replacement, and deletion are outside scope.

**Authoritative ownership:** Salesforce is the trusted system of record for the reference implementation.

**Attributes:** The required Account fields must come from Salesforce, but the approved field set and prohibited fields remain unresolved and are not invented here.

**Traceability:** FR-002–FR-004, FR-010–FR-012, SC-001–SC-004.

### DM-003 — Employer Contact

**Classification:** Business entity.

**Definition:** A person record associated with the Employer Account in the current Authorized Employer Context.

**Identity:** Each presented Employer Contact must be distinguishable within the associated Contact collection. The identifier and approved attributes are deferred.

**Lifecycle in this MVP:** View-only. Contact creation, updates, and deletion are outside scope.

**Authoritative ownership:** Salesforce is the trusted system of record for the reference implementation.

**Important distinction:** Employer Contact and Employer Administrator are separate concepts. The baselines do not establish that a portal user must be, or must not be, one of the associated Contacts.

**Traceability:** FR-002, FR-005, FR-008–FR-012; AC-002–AC-004 and AC-008.

### DM-004 — Enrollment Record

**Classification:** Business entity with unresolved business semantics.

**Definition:** A record of the approved Enrollment business concept associated with the Employer Account in the current Authorized Employer Context.

**Identity:** Each presented Enrollment Record must be distinguishable within the associated Enrollment collection. The identifier and approved business attributes are deferred.

**Lifecycle in this MVP:** View-only. Enrollment submission, change, and deletion are outside scope.

**Authoritative ownership:** Salesforce is the trusted system of record. The approved requirements clarify that the current source representation is a Salesforce custom object.

**Unresolved definition:** The baselines do not yet define what Enrollment represents. Statuses, dates, counts, groupings, record granularity, and other attributes must not be assumed.

**Traceability:** FR-002, FR-006–FR-012; AC-002, AC-003, AC-005, AC-006, and AC-008.

### DM-005 — Enrollment Summary

**Classification:** Derived business concept; not an independently mastered entity.

**Definition:** A summary calculated from the Enrollment Records associated with one Employer Account according to approved business rules.

**Identity:** It is identified by the Employer Account context and the approved set of Enrollment Records and summary rules; it does not require an independent business identity in this MVP.

**Lifecycle in this MVP:** Produced for viewing and never edited directly.

**Derivation:** Only Enrollment Records in the current Authorized Employer Context may contribute. The summary measures and zero-record result remain subject to business approval.

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
| REL-001 | Employer Administrator is authorized to view Employer Account | Exactly one authenticated administrator and one active Employer Account context per interaction. | The stored administrator-to-account cardinality and association mechanism are not defined. A small fixed set of MVP users may exist. |
| REL-002 | Employer Account has associated Employer Contacts | One Employer Account to zero or more presented Employer Contacts. | Every Contact included in the view must be associated with the current account. Cross-account Contact semantics are unresolved. |
| REL-003 | Employer Account has associated Enrollment Records | One Employer Account to zero or more presented Enrollment Records. | The current source represents Enrollment as an Account-related Salesforce custom object. |
| REL-004 | Enrollment Records produce Enrollment Summary | One in-scope Enrollment collection, including an empty collection, to one summary result. | The zero-record result and other summary rules require approval. An unavailable collection cannot be summarized as if it were empty. |
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
| BR-012 | Only approved fields may be included in Employer Account 360; the exact Account, Contact, and Enrollment field sets remain unresolved. | FR-004–FR-006; Requirements §4.1 |
| BR-013 | The business domain must not depend on Salesforce object names, query language, or platform interfaces as its business vocabulary. | FR-012; SC-004 |
| BR-014 | Employer Administrator and Employer Contact must not be treated as the same business entity unless a later approved rule explicitly relates them. | Requirements open question 4; domain ambiguity control |

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
| Employer Account | Account | Concept confirmed; field mapping unresolved. |
| Employer Contact | Contact associated with the employer Account | Relationship concept confirmed; fields and cross-account semantics unresolved. |
| Enrollment Record | Account-related custom object | Source type confirmed by approved clarification; business meaning, relationship details, and fields unresolved. |
| Enrollment Summary | Derived from in-scope Enrollment Records | Summary measures and derivation rules unresolved; not assumed to be a mastered Salesforce record. |
| Employer Administrator | Portal-managed user concept | Not assumed to be a Salesforce user or Contact; approved MVP anticipates a small fixed user set, with design deferred. |

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
- **Keep Employer Administrator separate from Employer Contact.** The approved baselines do not establish identity between the user and a Salesforce Contact.
- **Treat Enrollment Summary as derived information.** It depends on the associated Enrollment collection and approved rules rather than becoming a second source of truth.
- **Model only business-relevant states.** Empty, unavailable, and unauthorized carry distinct meanings required by the functional requirements.
- **Leave unresolved semantics explicit.** Enrollment meaning, field sets, summary measures, and stored authorization cardinality are not inferred.

### Trade-offs

- A platform-independent vocabulary improves reuse across enterprise systems but requires an explicit source-to-domain mapping later.
- Separating Employer Administrator from Employer Contact avoids an unsupported identity assumption but leaves any legitimate relationship for later business confirmation.
- A derived Enrollment Summary prevents duplicate authoritative ownership, but its usefulness cannot be validated until the business approves summary measures.
- Restricting cardinality to the active MVP context keeps the model accurate but does not answer future multi-employer or delegated-administration needs.

### Alternatives considered and not selected

- **Mirror the Salesforce object model as the domain model:** not selected because it would make platform implementation terminology drive the business model.
- **Treat Employer Administrator as a Salesforce Contact:** not selected because the approved baselines do not establish that relationship.
- **Treat Enrollment Summary as an editable or independently mastered entity:** not selected because the approved requirement defines it as derived from Enrollment Records.
- **Model future portal capabilities:** not selected because they are outside the approved Employer Account 360 scope.

## 11. Assumptions and Open Questions

### Assumptions carried forward

- Salesforce contains usable and authoritative Employer Account, Employer Contact, and Enrollment information for this MVP.
- Enrollment is represented by an Account-related Salesforce custom object.
- One active Employer Account context is sufficient for the MVP.
- A small fixed set of portal users can support MVP validation; hard-coding is an implementation choice to be evaluated later, not a domain rule.
- The MVP uses summary information rather than introducing an independent Enrollment Summary record of authority.
- “Data owned by Salesforce” means Salesforce is the system of record; an accountable business data owner still needs to be identified for governance and approval.

### Open questions requiring resolution

1. What business event or state does an Enrollment Record represent?
2. Which Account, Contact, and Enrollment attributes are required, and which are prohibited from external display?
3. What measures, groupings, statuses, dates, and zero-record behavior define a useful Enrollment Summary?
4. Is an Employer Administrator ever also an Employer Contact, and if so, what business relationship links them?
5. What is the persistent cardinality between Employer Administrators and Employer Accounts, independent of the one-context MVP interaction?
6. Can an Employer Contact or Enrollment Record be associated with more than one Employer Account?
7. What conditions qualify information as unavailable rather than empty, and what business-safe exception wording is required?
8. Who is the accountable business owner for the data even though Salesforce is the trusted system of record?

These questions constrain later work; they do not authorize architecture, security, data-model, API, or UX decisions in this phase.

## 12. Validation Approach

The Domain Model will be validated through:

- **Terminology review:** business stakeholders confirm that each canonical term has one understood meaning and that platform terms do not redefine the domain.
- **Entity review:** each entity is necessary for an approved functional requirement, has a clear business identity, and introduces no new use case.
- **Relationship review:** populated, empty, unavailable, and unauthorized scenarios satisfy the stated relationships and cardinalities.
- **Business-rule review:** BR-001 through BR-014 are testable, internally consistent, and traceable to approved discovery or requirements.
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
- approved BR-001 through BR-014;
- confirmed that Enrollment's unresolved business meaning, field sets, and summary rules remain visible and assigned for resolution;
- confirmed that Employer Administrator is not assumed to be a Salesforce Contact or Salesforce user;
- verified traceability to the approved discovery and functional requirements;
- confirmed that no architecture, API, security mechanism, data schema, UX design, or implementation decision has been introduced;
- accepted the validation approach; and
- approved progression to the next lifecycle phase.

Until these criteria are met, this document remains a Domain Model draft and no later major phase should begin.
