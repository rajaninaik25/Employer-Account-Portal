# Business Discovery — Employer Account Portal

**Showcase:** WorkflowFox Showcase #2  
**Phase:** 1 — Business Discovery  
**Status:** Draft for review  
**Scope:** Small, production-inspired MVP

## 1. Executive Context

Many organizations rely on established enterprise platforms to hold trusted business data, but the experiences provided by those platforms may not meet the needs of external users. Replacing a trusted system of record can introduce cost, risk, and disruption when the underlying data capabilities remain valuable.

This showcase explores a pragmatic modernization pattern: retain the existing enterprise platform as the trusted system of record while delivering a modern, purpose-built digital experience around it.

> **Business thesis:** Modernize around trusted enterprise platforms, not necessarily away from them.

Salesforce is the system of record in this reference implementation. The pattern is intended to remain applicable to other enterprise platforms and custom systems.

## 2. Business Problem

Employer administrators need a clear, convenient way to view essential information about their organization. That information may already exist in Salesforce, but exposing the internal platform directly can create a poor external-user experience, unnecessary platform coupling, and avoidable security and maintenance concerns.

The business needs a way to improve the employer experience without duplicating ownership of trusted data or committing to a disruptive replacement of the current enterprise platform.

## 3. Showcase Objective

Build a small, production-inspired Employer Account 360 MVP that demonstrates how an enterprise can place a modern digital application and an enterprise integration/application layer around an existing system of record.

The showcase is primarily evidence of an engineering approach, not a proposal for a complete employer portal.

> **Showcase thesis:** AI-assisted engineering can accelerate enterprise modernization by enabling teams to rapidly build modern applications around existing systems of record.

The work will demonstrate AI assistance across discovery, requirements, architecture, design, implementation, testing, validation, and documentation, while retaining human review and engineering ownership.

## 4. Primary User

The primary user is an **Employer Administrator**: an authorized representative who needs to understand their employer organization's account, contacts, and enrollment information.

For this MVP, the user is a viewer of existing information. Detailed personas, authorization roles, and delegated administration rules remain discovery topics.

## 5. Primary Use Case — Employer Account 360

An Employer Administrator accesses an external portal and views a consolidated representation of their employer organization, including:

- an account overview with basic employer information;
- contacts associated with the employer; and
- enrollment records with a useful summary.

The experience is read-only. Salesforce supplies the underlying Account, Contact, and Enrollment child-record data and remains the authoritative source.

## 6. Current-State Problem

The assumed current state has one or more of the following characteristics, subject to validation:

- Employer information is available in Salesforce but is not presented through a focused external experience.
- External access may depend on manual assistance, fragmented channels, or an experience shaped by the internal system rather than employer needs.
- Directly exposing Salesforce concepts could couple the user experience to objects, queries, and platform-specific interfaces.
- Modernization may be perceived as requiring replacement of the system of record, making change appear larger and riskier than necessary.

The exact current journey, pain points, volumes, and service impacts have not yet been validated with business stakeholders or users.

## 7. Target-State Experience

An authenticated and authorized Employer Administrator can open a modern external application and quickly understand their organization's current information in one coherent, read-only experience.

At a high level, the interaction is:

```text
Employer Administrator
        → Modern Digital Application
        → Enterprise Application / Integration Layer
        → Trusted System of Record (Salesforce)
```

The application presents business concepts such as employer profile, contacts, and enrollment. It does not expose Salesforce objects, query language, or platform APIs to the frontend. Information remains governed and mastered in Salesforce.

## 8. Business Outcomes

The MVP is intended to provide evidence that the organization can:

- improve access to essential employer information through a focused digital experience;
- modernize incrementally while preserving Salesforce as the trusted source;
- reduce direct coupling between the external experience and the enterprise platform;
- establish a reusable modernization pattern for other systems of record;
- demonstrate disciplined, AI-assisted delivery across the engineering lifecycle; and
- create reusable architecture, documentation, validation evidence, and engineering knowledge.

Quantified operational outcomes are not claimed at discovery. Suitable measures—such as task completion, reduced assisted-service demand, data freshness, reliability, and delivery cycle time—require stakeholder baselines and later validation.

## 9. Scope

### In scope for the MVP

- A read-only Employer Account 360 experience for one authorized employer context.
- Account overview using basic employer/account information supplied by Salesforce.
- A list or presentation of Contacts associated with the employer.
- Enrollment child records and a useful enrollment summary.
- A modern application separated from Salesforce by a business-oriented application/integration layer.
- Engineering artifacts and validation evidence required to explain and assess the modernization approach.

### Scope constraints

- The showcase remains intentionally small.
- Salesforce retains ownership of account-level source data.
- The exact fields, summary measures, data volumes, freshness expectations, and access rules will be defined in later approved phases.
- Each major lifecycle phase requires review before work advances.

## 10. Explicit Non-Goals

The MVP will not include:

- enrollment submission, updates, or other transactional enrollment workflows;
- claims processing;
- billing, invoices, or payments;
- document processing;
- full case management;
- autonomous agents;
- a general-purpose AI chatbot;
- replacement or migration of Salesforce as the system of record;
- broad employer self-service beyond Employer Account 360;
- direct frontend use of Salesforce objects, SOQL, or Salesforce APIs; or
- technology selection, API design, detailed architecture, or implementation during this phase.

Application-level AI is not assumed. It may be considered only if a later, approved business need justifies it.

## 11. Key Assumptions

- Salesforce contains sufficiently reliable Account, Contact, and Enrollment data for the MVP.
- Enrollment is represented as a Salesforce child record related to the employer Account; its final business definition and schema remain to be confirmed.
- Employer Administrators may view only information belonging to employer organizations they are authorized to access.
- The MVP is read-only and does not write data back to Salesforce.
- A single employer context is sufficient for the initial showcase; multi-employer access is unconfirmed.
- The portal will obtain data through an application/integration boundary rather than directly from Salesforce.
- Near-real-time data may be desirable, but required freshness, availability, and performance targets are not yet agreed.
- Representative, non-sensitive test data and a suitable Salesforce environment will be available for implementation and validation.
- AI-generated artifacts will receive human review, testing, validation, and documented ownership.

## 12. Modernization Principles

- **Preserve trusted ownership:** Salesforce remains authoritative for employer account-level data.
- **Modernize incrementally:** Improve the experience without requiring system-of-record replacement.
- **Design around business capabilities:** Present employer-oriented concepts rather than Salesforce implementation details.
- **Create a boundary around the platform:** Keep the frontend independent of Salesforce objects, SOQL, and platform APIs.
- **Remain technology-agnostic:** Select technologies in later phases based on business and quality needs.
- **Control scope:** Prove one coherent use case before considering broader portal capabilities.
- **Engineer for trust:** Treat security, testing, validation, accessibility, observability, and documentation as delivery requirements.
- **Use AI with accountability:** Use AI to accelerate engineering work while preserving human judgment and verification.
- **Produce reusable assets:** Capture decisions, trade-offs, evidence, and lessons that apply beyond Salesforce.

## 13. Risks

| Risk | Potential impact | Discovery response |
|---|---|---|
| Unclear employer-to-user authorization rules | Inappropriate data exposure or rework | Confirm identity, employer association, roles, and access boundaries before security and implementation design. |
| Incomplete or inconsistent Salesforce data | Misleading Account 360 experience | Profile representative data and agree how missing or stale values should appear. |
| Ambiguous enrollment meaning or summary | A technically correct but unhelpful experience | Validate the enrollment record definition and decision-useful summary with business stakeholders. |
| Scope growth into a full portal | Delayed delivery and diluted showcase thesis | Maintain explicit non-goals and require approval for added use cases. |
| Platform-specific leakage into the application | Reduced portability and higher change cost | Preserve a business-oriented boundary and validate architecture against coupling criteria. |
| Unspecified non-functional expectations | Late changes to design or infrastructure | Establish measurable security, privacy, accessibility, performance, reliability, and freshness requirements in later phases. |
| AI-generated errors or unsupported assumptions | Defects and loss of engineering credibility | Require human review, traceability, automated checks, and validation evidence. |
| Showcase value is judged only by UI breadth | Pressure to add low-value features | Evaluate the reference implementation on the modernization pattern and lifecycle evidence as well as the user experience. |

## 14. Discovery Questions / Open Questions

1. Which concrete tasks or pain points currently cause Employer Administrators to seek account, contact, or enrollment information?
2. Which Account and Contact fields are essential for the MVP, and which fields must not be exposed?
3. What does an Enrollment record represent, and which statuses, dates, counts, or groupings make its summary useful?
4. How is an Employer Administrator identified and associated with an employer Account?
5. Can a user administer more than one employer, and if so, is account switching required in the MVP?
6. What authentication, authorization, consent, privacy, audit, and regulatory requirements apply?
7. What data freshness, response-time, availability, and expected-volume targets should guide later design?
8. How should missing, stale, duplicate, or unavailable Salesforce data be communicated to the user?
9. Which Salesforce environment, integration capabilities, and representative test data will be available?
10. Who are the business owner, data owner, security approver, and final MVP acceptance authority?
11. Which baseline and target measures will demonstrate business and engineering value?
12. Are there branding, accessibility, device, browser, or localization constraints for the target experience?

## 15. Phase Exit Criteria

Business Discovery is complete when stakeholders have:

- confirmed the business and showcase theses;
- validated the Employer Administrator as the primary user and Employer Account 360 as the sole MVP use case;
- approved the in-scope capabilities, constraints, and explicit non-goals;
- confirmed Salesforce's role as the trusted system of record;
- reviewed and accepted or corrected the key assumptions;
- assigned owners and next actions for material open questions and risks;
- agreed that technology selection, detailed architecture, API design, and implementation remain deferred; and
- approved progression to Phase 2 — Functional Requirements.

Until these criteria are met, this document remains a discovery draft and no subsequent major phase should begin.
