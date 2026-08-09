# Functional Requirements — Employer Account Portal

**Showcase:** WorkflowFox Showcase #2  
**Phase:** 2 — Functional Requirements  
**Status:** Draft for review  
**Requirements baseline:** `docs/discovery/01-business-discovery.md`  
**Scope:** Employer Account 360 read-only MVP

## 1. Purpose and Traceability Basis

This document translates the approved Business Discovery into testable functional requirements for the Employer Account Portal MVP. Every requirement is derived from the discovery baseline; no additional use case is introduced.

Traceability uses the following identifiers:

- **FR-xxx:** functional requirement;
- **SC-xxx:** approved solution or scope constraint; and
- **AC-xxx:** acceptance scenario used to validate one or more requirements.

Exact fields, enrollment measures, identity mechanics, technology choices, API contracts, security controls, data structures, and user-interface designs remain outside this phase unless the discovery already establishes a boundary.

## 2. Business and Scope Baseline

The MVP enables one authenticated Employer Administrator to view a consolidated, read-only Employer Account 360 for one authorized employer context. The experience includes:

- an Employer Account overview;
- Contacts associated with that employer; and
- Enrollment child records with a useful summary.

Salesforce remains the trusted source of this information. The external experience is organized around employer-facing business concepts rather than Salesforce implementation details.

**Primary business thesis:** Modernize around trusted enterprise platforms, not necessarily away from them.

**Source:** Business Discovery §§1–5, 7, and 9.

## 3. Actor and Use Case

### 3.1 Primary actor

**Employer Administrator** — an authenticated representative authorized to view information for the employer context presented by the MVP.

### 3.2 Primary use case

**UC-001 — View Employer Account 360**

- **Goal:** Understand the employer's account, associated contacts, and enrollment information in one coherent experience.
- **Preconditions:** The Employer Administrator is authenticated; an employer context has been established; and the user is authorized for that context.
- **Trigger:** The Employer Administrator requests the Employer Account 360 experience.
- **Successful outcome:** The portal presents the available Account overview, associated Contacts, Enrollment records, and Enrollment summary for the authorized employer.
- **Alternate outcomes:** A section has no available records, or some or all source information cannot be retrieved. The portal communicates the applicable state without treating unavailable information as confirmed empty data.
- **Postcondition:** No Account, Contact, or Enrollment data is created, changed, submitted, or deleted.

**Source:** Business Discovery §§4–7, 9, 11, 13, and 14.

## 4. Functional Requirements

All requirements are **Must** priority because this phase defines only the approved MVP. Items that need later clarification are expressed as open parameters, not guessed requirements.

| ID | Requirement | Acceptance intent | Discovery source |
|---|---|---|---|
| FR-001 | The portal shall require the Employer Administrator to be authenticated before presenting Employer Account 360 information. | An unauthenticated request does not present employer information. | §§4, 7; §14 Q4, Q6 |
| FR-002 | The portal shall present information only for the employer context the authenticated Employer Administrator is authorized to view. | Data belonging to a different or unauthorized employer is not presented. | §§4, 9, 11; §13 authorization risk; §14 Q4–Q6 |
| FR-003 | The portal shall provide one coherent Employer Account 360 experience for the authorized employer context. | The user can access Account, Contacts, and Enrollment information as parts of the same business experience. | §§5, 7, 9 |
| FR-004 | The portal shall present an Account overview using the approved basic employer information available from Salesforce. | The approved Account fields for the authorized employer are represented without exposing unapproved fields. | §§5, 9, 11; §14 Q2 |
| FR-005 | The portal shall present Contacts associated with the authorized employer Account. | Associated Contacts are represented; Contacts outside the authorized employer context are not represented. | §§5, 9, 11; §14 Q2 |
| FR-006 | The portal shall present Enrollment child records associated with the authorized employer Account. | Associated Enrollment records are represented; records outside the authorized employer context are not represented. | §§5, 9, 11; §14 Q3 |
| FR-007 | The portal shall present a useful Enrollment summary derived from the Enrollment records in scope for the authorized employer. | The displayed summary agrees with the approved definition and the records from which it is derived. | §§5, 9; §13 enrollment risk; §14 Q3 |
| FR-008 | The portal shall distinguish between an empty collection and information that could not be retrieved. | A confirmed absence of Contacts or Enrollment records is not represented as a retrieval failure, and a retrieval failure is not represented as zero records. | §13 data-quality and non-functional risks; §14 Q8 |
| FR-009 | The portal shall communicate when any Account 360 section cannot be presented because its source information is unavailable. | The affected section has an identifiable unavailable state; unaffected information may remain usable where later design permits. | §13 data-quality risk; §14 Q8 |
| FR-010 | The portal shall operate as a read-only experience for Account, Contact, and Enrollment information. | No user path creates, updates, submits, or deletes the in-scope business information. | §§5, 9–11 |
| FR-011 | The information presented by the portal shall represent data supplied by Salesforce as the trusted system of record. | Test evidence can reconcile displayed business information to the approved source data. | §§1–3, 5, 7, 9, 11–12 |
| FR-012 | The portal shall present employer-facing business concepts without exposing Salesforce objects, SOQL, or Salesforce APIs to the Employer Administrator or directly coupling the frontend to them. | User-visible and frontend-facing behavior is expressed as Account 360 business capabilities rather than Salesforce implementation contracts. | §§2, 7, 9–10, 12–13 |

### 4.1 Parameters requiring approval

The following details are intentionally not invented in this phase:

| Parameter | Affects | Required decision |
|---|---|---|
| Account overview fields | FR-004 | Identify essential fields and fields prohibited from external display. |
| Contact fields | FR-005 | Identify essential fields and fields prohibited from external display. |
| Enrollment business definition and record fields | FR-006 | Confirm what an Enrollment record represents and which attributes are useful. |
| Enrollment summary definition | FR-007 | Approve the counts, statuses, dates, or groupings that make the summary useful. |
| Employer-context establishment | FR-002 | Confirm how the authenticated user is associated with an employer. |
| Missing and unavailable-state wording | FR-008, FR-009 | Agree the business meaning; detailed presentation belongs to UX Design. |

## 5. Approved Constraints

| ID | Constraint | Reason | Discovery source |
|---|---|---|---|
| SC-001 | The MVP is read-only. | It proves access to trusted information without introducing transactional risk or scope. | §§5, 9–11 |
| SC-002 | The MVP supports one Employer Administrator operating in one authorized employer context. | A single focused context is sufficient to demonstrate the modernization pattern; multi-employer behavior is unconfirmed. | §§4, 9, 11; §14 Q5 |
| SC-003 | Salesforce remains the trusted system of record for Account, Contact, and Enrollment information. | Modernization improves the experience without replacing trusted data ownership. | §§1–3, 5, 7, 9, 11–12 |
| SC-004 | The frontend does not directly use Salesforce objects, SOQL, or Salesforce APIs. | A business-oriented boundary reduces platform coupling and preserves reuse of the pattern. | §§2, 7, 9–10, 12–13 |
| SC-005 | Application-level AI is not part of the approved MVP. | The AI story is AI-assisted engineering; no application-level AI business problem has been approved. | §§3, 10–12 |
| SC-006 | Technology, API, security, data-model, and UX design decisions are deferred to their approved lifecycle phases. | Requirements define required behavior without prematurely selecting implementation mechanisms. | §§9–10, 12, 15 |

## 6. Explicitly Excluded Requirements

No requirement is established for:

- enrollment submission or any other data-changing enrollment workflow;
- document upload or document processing;
- billing, invoices, or payments;
- claims processing;
- case management;
- notifications;
- workflow engines;
- autonomous agents or chatbots;
- replacement or migration of Salesforce;
- broad employer self-service;
- multi-employer account switching;
- Account, Contact, or Enrollment create, update, or delete operations; or
- any additional portal use case.

These exclusions preserve the approved MVP boundary. Adding any of them requires explicit scope approval and an update to the discovery and requirements baselines.

**Source:** Business Discovery §§9–10 and the approved Phase 2 instruction.

## 7. Acceptance Scenarios

These scenarios define validation intent without prescribing user-interface, API, or implementation design.

### AC-001 — Authentication required

**Given** no authenticated Employer Administrator context exists  
**When** Employer Account 360 information is requested  
**Then** no employer Account, Contact, or Enrollment information is presented.

**Validates:** FR-001.

### AC-002 — Authorized Employer Account 360

**Given** an authenticated Employer Administrator is authorized for the MVP employer context  
**And** representative Account, Contact, and Enrollment source data exists  
**When** the Employer Administrator requests Employer Account 360  
**Then** the portal presents the approved Account overview  
**And** associated Contacts  
**And** associated Enrollment records  
**And** the approved Enrollment summary.

**Validates:** FR-002–FR-007, FR-011, FR-012.

### AC-003 — Unauthorized employer isolation

**Given** an authenticated Employer Administrator is not authorized for another employer  
**When** information for that employer is requested  
**Then** the other employer's Account, Contacts, and Enrollment information is not presented.

**Validates:** FR-002, FR-004–FR-006.

### AC-004 — No associated Contacts

**Given** the authorized employer has no associated Contacts in the trusted source  
**When** Employer Account 360 is presented  
**Then** the portal represents the Contacts collection as empty rather than unavailable.

**Validates:** FR-005, FR-008.

### AC-005 — No associated Enrollment records

**Given** the authorized employer has no associated Enrollment records in the trusted source  
**When** Employer Account 360 is presented  
**Then** the portal represents the Enrollment collection as empty  
**And** the summary follows the approved zero-record definition.

**Validates:** FR-006–FR-008.

### AC-006 — Source information unavailable

**Given** one or more Account 360 sections cannot obtain their source information  
**When** Employer Account 360 is presented  
**Then** each affected section is represented as unavailable rather than empty  
**And** no unapproved internal platform detail is exposed.

**Validates:** FR-008, FR-009, FR-012.

### AC-007 — Read-only boundary

**Given** an authenticated Employer Administrator is using Employer Account 360  
**When** all available user paths are evaluated  
**Then** no path creates, changes, submits, or deletes Account, Contact, or Enrollment information.

**Validates:** FR-010 and SC-001.

### AC-008 — Source reconciliation

**Given** approved representative source records and summary rules  
**When** Employer Account 360 output is compared with those records  
**Then** the Account, Contacts, Enrollment records, and calculated summary agree with the trusted source and approved rules.

**Validates:** FR-004–FR-007, FR-011.

## 8. Traceability and Coverage Matrix

| Discovery statement | Requirement coverage | Validation coverage |
|---|---|---|
| Authenticated and authorized Employer Administrator (§§4, 7, 11) | FR-001, FR-002 | AC-001–AC-003 |
| One coherent Employer Account 360 (§§5, 7, 9) | FR-003 | AC-002 |
| Basic Account overview (§§5, 9) | FR-004 | AC-002, AC-003, AC-008 |
| Associated Contacts (§§5, 9) | FR-005 | AC-002–AC-004, AC-008 |
| Enrollment records and useful summary (§§5, 9) | FR-006, FR-007 | AC-002, AC-003, AC-005, AC-008 |
| Missing or unavailable information (§13; §14 Q8) | FR-008, FR-009 | AC-004–AC-006 |
| Read-only MVP (§§5, 9–11) | FR-010, SC-001 | AC-007 |
| Salesforce is authoritative (§§1–3, 5, 7, 9, 11–12) | FR-011, SC-003 | AC-008 |
| Business-oriented boundary and no direct Salesforce coupling (§§2, 7, 9–10, 12–13) | FR-012, SC-004 | AC-002, AC-006 |
| Application-level AI not assumed (§10) | SC-005 | Scope review |
| Explicit non-goals (§10) | §6 exclusions | Scope review |

## 9. Decisions, Trade-offs, and Alternatives

### Decisions carried forward from discovery

- **One read-only use case:** keeps the showcase small enough to validate the modernization pattern with engineering depth.
- **Salesforce remains authoritative:** avoids duplicating data ownership or turning the showcase into a platform replacement exercise.
- **Business-oriented separation:** protects the external experience from direct Salesforce coupling while leaving detailed architecture and contracts to later phases.
- **Application AI excluded:** keeps the AI narrative grounded in engineering acceleration rather than adding an unvalidated feature.

### Trade-offs

- Read-only scope limits immediate self-service value but materially reduces workflow, validation, and data-integrity complexity.
- One employer context avoids premature delegated-administration and account-switching rules, but does not yet represent users responsible for multiple employers.
- Deferring exact fields and Enrollment summary rules prevents invented business definitions, but those decisions must be resolved before downstream design and acceptance tests can be finalized.
- Deferring measurable non-functional targets preserves phase discipline, but unresolved targets may affect later architecture choices.

### Alternatives considered and not selected

- **Expose Salesforce directly to external users or the frontend:** not selected because it weakens the business boundary and increases platform coupling.
- **Replace Salesforce:** not selected because replacement is unnecessary to demonstrate the target modernization outcome and conflicts with the thesis.
- **Add transactional employer services:** not selected because they expand the MVP beyond Employer Account 360.
- **Add application-level AI:** not selected because discovery identified no clear user problem that requires it.

## 10. Assumptions and Open Questions

### Assumptions carried forward

- Salesforce contains usable Account, Contact, and Enrollment information for the MVP.
- Enrollment records can be related to the employer Account.
- Authorization can establish one employer context for the authenticated user.
- Representative, non-sensitive test data and a suitable Salesforce environment will be available.
- AI-assisted requirements and later artifacts will receive human review and validation.

### Open questions requiring requirements approval or later-phase resolution

1. Which Account and Contact fields are required, and which are prohibited from external display? Requird fields from Salesforce
2. What precisely does Enrollment represent, and what record attributes are required? Custom Object on Salesforce
3. Which summary measures and rules make Enrollment useful to the Employer Administrator? Summarized information
4. How is an authenticated Employer Administrator associated with the employer context? Employer Portal should have its own user management. for mvp, hard code couple of users
5. Is one employer context confirmed as the complete MVP boundary? yes
6. What business behavior is expected when data is missing, stale, duplicated, or unavailable? show exception message
7. Which measurable security, privacy, audit, accessibility, performance, availability, freshness, and volume expectations apply? mvp
8. Who owns the business data, requirements approval, security approval, and final MVP acceptance? data is owned by salesforce
9. Which business and engineering measures will establish showcase success? end to end success 

Unresolved questions must remain visible inputs to the appropriate later phase; they do not authorize assumptions or additional functionality.

## 11. Validation Approach

Functional validation will use:

- **Requirements review:** confirm each FR and constraint against the approved discovery baseline.
- **Traceability review:** verify every in-scope discovery capability maps to requirements and acceptance scenarios, and every requirement maps back to discovery.
- **Scope review:** search downstream artifacts and implementation for excluded capabilities and unapproved Salesforce coupling.
- **Scenario validation:** exercise AC-001 through AC-008 with representative authorized, unauthorized, empty, unavailable, and populated conditions.
- **Source reconciliation:** compare Account, Contact, Enrollment, and summary results with approved representative Salesforce data and business rules.
- **Read-only validation:** verify that no supported user path or exposed business capability mutates in-scope data.
- **Human approval:** require review by the identified business, data, and security owners; AI-generated evidence is not self-approving.

Detailed test cases, quality targets, and implementation-specific checks will be created only in their approved later phases.

## 12. Future Extensibility

The requirements preserve future extensibility by expressing employer-facing capabilities independently of Salesforce implementation details and by assigning stable identifiers for traceability. This allows the modernization pattern to be reused around other trusted enterprise platforms.

Extensibility is a design quality, not permission to expand this MVP. Transactions, additional employer services, multiple employer contexts, application-level AI, and other excluded capabilities require new discovery, explicit approval, and updated requirements before design or implementation.

## 13. Phase Exit Criteria

Functional Requirements is complete when reviewers have:

- confirmed that FR-001 through FR-012 express only the approved Employer Account 360 scope;
- confirmed bidirectional traceability between discovery, requirements, and acceptance scenarios;
- approved or assigned owners for the open parameters affecting Account, Contact, and Enrollment content;
- confirmed the read-only, single-employer-context boundary and explicit exclusions;
- agreed that unresolved architecture, API, security, data-model, UX, and non-functional decisions remain deferred;
- accepted the validation approach; and
- approved progression to the next lifecycle phase.

Until these criteria are met, this document remains a requirements draft and no later major phase should begin.
