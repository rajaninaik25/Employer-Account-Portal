# AI-Assisted Engineering Plan — Employer Account Portal

**Showcase:** WorkflowFox Showcase \#2<br> **Phase:** 10 — AI-Assisted
Engineering Plan<br> **Status:** Approved<br> **Authoritative
baselines:** [Business
Discovery](../discovery/01-business-discovery.md), [Functional
Requirements](../requirements/02-functional-requirements.md), [Domain
Model](../domain-model/03-domain-model.md), [Solution
Architecture](../architecture/04-solution-architecture.md),
[Implementation Design](../design/05-implementation-design.md), [API
Specification](../api/06-api-specification.md),
[`contracts/openapi.yaml`](../../contracts/openapi.yaml), [Security
Design](../security/07-security-design.md), [Data
Model](../data/08-data-model.md), and [User Experience
Design](../ux/09-user-experience-design.md)<br> **Scope:** AI assistance
during implementation, testing, validation, and documentation; no
runtime AI

## 1. Executive Summary

WorkflowFox Showcase \#2 will use AI as a bounded engineering
accelerator while human engineers retain authority for scope,
architecture, security, contracts, source-system access, acceptance, and
production-readiness judgment.

AI may interpret approved specifications, propose work plans, generate
candidate code and tests, review changes, analyze failures, and draft
documentation. Each contribution is constrained to a small work unit,
traced to approved artifacts, reviewed by a human, and validated through
deterministic tools and representative environments. AI output is never
self-approving.

The implementation sequence begins with reproducible repository
foundations, proceeds through domain, contract, persistence, security,
integration, application, frontend, and accessibility work, and connects
to the Salesforce development environment only after the isolated
adapter passes against test doubles. Full validation completes the
sequence.

The plan also defines the evidence needed to answer the showcase's
enterprise question:

> Can AI-assisted engineering materially accelerate delivery of a modern
> enterprise application integrated with an existing system of record
> without sacrificing engineering quality?

The answer will come from work-unit journals, accepted/rejected AI
contributions, corrections, elapsed effort observations, traceability,
and executed validation—not from promotional estimates.

The Employer Account Portal contains no runtime AI feature, AI Agent,
chatbot, model call, or AI dependency.

## 2. AI-Assisted Engineering Thesis

> AI can significantly accelerate enterprise application development
> when engineers provide strong specifications, architecture boundaries,
> contracts, validation criteria, and human review.

``` text
Specification
     ↓
Implementation Planning
     ↓
Candidate Code and Tests
     ↓
Human Review
     ↓
Validation
     ↓
Accepted Implementation and Evidence
```

AI can accelerate interpretation, drafting, repetition, test-case
expansion, failure analysis, traceability, and documentation. It does
not replace:

``` text
Business Judgment
Architecture
Security Ownership
Engineering Decisions
Validation
Approval
```

> AI accelerates engineering but does not become the engineering
> authority.

The AI system proposes. Human engineers decide. Automated and
environment-specific validation provide evidence.

## 3. Objectives

| ID      | Objective                                               | Evidence of achievement                                                                                             |
|---------|---------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| AIO-001 | Accelerate implementation from approved specifications. | Small work units reach validated completion with recorded AI and human contributions.                               |
| AIO-002 | Preserve architecture discipline.                       | Dependency boundaries, adapter isolation, and source ownership pass review and architecture-conformance checks.     |
| AIO-003 | Maintain specification-to-code traceability.            | Requirements/design references connect work units, files, tests, and validation evidence.                           |
| AIO-004 | Improve test breadth without circular validation.       | Tests are derived from requirements, threats, contracts, data rules, and UX states—not merely generated from code.  |
| AIO-005 | Protect security and sensitive information.             | No secrets or real client data enter prompts; scanning, tests, and human security review pass.                      |
| AIO-006 | Produce honest engineering evidence.                    | Journals record AI mistakes, rework, validation failures, and observed effort alongside successes.                  |
| AIO-007 | Keep implementation understandable.                     | Code can be maintained from repository artifacts without access to AI conversation history.                         |
| AIO-008 | Create reusable WorkflowFox methods.                    | Prompt, review, change-control, journal, validation, and traceability patterns are identified for later extraction. |
| AIO-009 | Prevent scope expansion.                                | No capability beyond login, logout, and read-only Employer Account 360 appears in code or tests.                    |

## 4. Scope

### 4.1 Permitted AI-assisted work

| Area                      | Permitted assistance                                                                                                          | Governing baselines                                                        |
|---------------------------|-------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| Repository foundation     | Draft approved folders, manifests, quality tasks, and minimal application/test scaffolds.                                     | Implementation Design.                                                     |
| Frontend                  | Draft Login, Account 360, responsive state components, local Enrollment presentation paging, and tests.                       | UX Design, OpenAPI, relevant security rules, Functional Requirements.      |
| Backend                   | Draft API delivery, application services, domain models, persistence adapters, configuration, logging, and error translation. | Implementation Design, OpenAPI, Domain Model, Data Model, Security Design. |
| Portal persistence        | Draft models/migrations for Portal User, Portal Session, and approved login-attempt state.                                    | Data Model and Security Design.                                            |
| Authentication/session    | Draft password verification, session lifecycle, throttling, CSRF/origin controls, and tests.                                  | Security Design and OpenAPI.                                               |
| Salesforce adapter        | Draft source-private models, OAuth boundary, queries, paging, mapping, and error translation behind the approved port.        | Architecture, Implementation Design, Data Model, Security Design.          |
| Account 360 orchestration | Draft the fail-closed authorization chain, child retrieval, Summary derivation, and partial-failure behavior.                 | Requirements, Domain Model, Implementation Design, API Specification.      |
| Tests                     | Generate candidate unit, integration, contract, security, frontend-state, accessibility, end-to-end, and adapter tests.       | The specification that defines each expected result.                       |
| Debugging/review          | Analyze sanitized failures and diffs; propose bounded corrections and review findings.                                        | Approved artifacts plus executed evidence.                                 |
| Documentation             | Draft implementation guides, validation reports, README updates, traceability, and journal entries.                           | Implemented behavior and executed evidence.                                |

### 4.2 Prohibited work

AI must not:

- invent or approve business requirements;
- change architecture, security, data ownership, UX behavior, or OpenAPI
  without controlled review;
- add runtime AI, AI Agents, chatbots, or model dependencies;
- create Account, Contact, or Enrollment mutation behavior;
- replicate Salesforce business data into portal persistence;
- expose Salesforce concepts outside the adapter;
- broaden Salesforce permissions or use Employer Administrator
  credentials;
- add infrastructure, navigation, objects, APIs, or dependencies for
  appearance;
- use real credentials, secrets, client data, production payloads, or
  personal information; or
- declare work complete based only on code generation, compilation, or
  AI review.

## 5. AI Roles

| Role                      | Permitted behavior                                                                                               | Required boundary                                                                        |
|---------------------------|------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| Specification Interpreter | Extract task-specific requirements, invariants, exclusions, and acceptance criteria from approved artifacts.     | Cite the governing sections; identify ambiguity rather than resolving it by invention.   |
| Implementation Planner    | Break one approved work unit into ordered, reviewable changes and validations.                                   | Stay inside the work unit and approved repository boundaries.                            |
| Code Generator            | Produce candidate code, configuration, migration, fixture, or test changes.                                      | Use approved technologies and interfaces; preserve unrelated work; generate no secret.   |
| Test Generator            | Derive positive, negative, boundary, partial-failure, security, and accessibility tests from specifications.     | Expected behavior comes from the specification, not from observing generated code.       |
| Code Reviewer             | Review diffs for correctness, architecture, scope, security, contract, data, accessibility, and maintainability. | Findings assist human review; AI cannot approve its own or another AI's change.          |
| Documentation Assistant   | Draft module guides, traceability, journal entries, and validation summaries.                                    | Claims must link to implemented behavior and executed evidence.                          |
| Debugging Assistant       | Analyze sanitized failures, propose root causes, and recommend the smallest compliant fix.                       | Do not suppress failures, weaken controls, or change specifications to make checks pass. |
| Refactoring Assistant     | Propose local simplification after behavior is protected by tests.                                               | No architecture, contract, or behavior change without explicit approval.                 |

AI is not assigned the roles of product owner, architect, security
approver, Salesforce administrator, release approver, or production
operator.

## 6. Human Engineering Ownership

| Human-owned responsibility          | Required human action                                                                                                       |
|-------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| Business scope and requirements     | Approve the use case, fields, outcomes, exclusions, and any change to them.                                                 |
| Architecture                        | Own component boundaries, dependency direction, source-system isolation, and deviations.                                    |
| Technology and dependency selection | Approve material packages, versions, licenses, and platform coupling.                                                       |
| API contract                        | Approve `contracts/openapi.yaml`, compatibility, and any amendment.                                                         |
| Security                            | Approve password/session controls, authorization, Salesforce identity/permissions, secrets, exceptions, and residual risks. |
| Data ownership/model                | Approve portal persistence, Salesforce mappings, correlation, and no-replication boundary.                                  |
| UX/accessibility                    | Approve information hierarchy, state semantics, content, responsive behavior, and accessibility acceptance.                 |
| Salesforce environment              | Configure and validate the External Client App, integration user, permissions, metadata, sharing, and representative data.  |
| Code acceptance                     | Review changes, resolve findings, and decide whether the implementation is understandable and correct.                      |
| Validation acceptance               | Examine executed evidence, failures, exceptions, and environment coverage.                                                  |
| Production-readiness judgment       | Decide whether the reference implementation is suitable for any environment beyond the showcase.                            |
| Publishing claims                   | Approve every claim about quality, security, performance, accessibility, and AI effectiveness.                              |

AI output is never self-approving. A human owns every accepted decision
and every exception.

## 7. Specification-Driven Implementation

### 7.1 Authority chain

``` text
Business Discovery
        ↓
Functional Requirements
        ↓
Domain Model
        ↓
Solution Architecture
        ↓
Implementation Design
        ↓
Approved OpenAPI Contract
        ↓
Security Design
        ↓
Data Model
        ↓
User Experience Design
        ↓
Implementation Work Unit
        ↓
Code + Tests + Validation Evidence
```

Lower artifacts implement higher approved intent; they do not silently
redefine it. `contracts/openapi.yaml` is authoritative for the
frontend/backend boundary even when FastAPI generates a different
description.

### 7.2 Work-unit readiness

A work unit is ready only when:

- its governing artifacts are approved;
- task scope and allowed files are explicit;
- dependencies on prior work units pass validation;
- acceptance criteria and stop conditions are written;
- relevant test fixtures contain only fictional/sanitized data; and
- the exact validation tasks to run are known.

### 7.3 Specification conflict workflow

``` text
STOP implementation
        ↓
Record the observed conflict and evidence
        ↓
Identify the authoritative artifact and affected work units
        ↓
Propose a controlled artifact change or clarification
        ↓
Human review and approval
        ↓
Update traceability and validation expectations
        ↓
Resume implementation
```

The known Security Design requirement to add `maxLength: 128` to
`LoginRequest.username` and `maxLength: 256` to `LoginRequest.password`
is a controlled pre-implementation contract prerequisite. This plan does
not modify OpenAPI. The contract owner must apply, review, and
revalidate those approved constraints before Work Unit 4 is accepted.

## 8. AI Context Strategy

AI receives the smallest complete context required for the current work
unit, plus the current relevant files and validation output. A short
context manifest records authoritative inputs, relevant sections,
current code paths, allowed files, and exclusions.

| Task type              | Primary context                                                                                                                          | Usually excluded                                                     |
|------------------------|------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| Backend module         | Implementation Design, Domain Model, OpenAPI, relevant Security/Data sections, applicable FR/BR rules, current backend interfaces/tests. | UX visual direction, publishing plans, unrelated source files.       |
| Frontend module        | UX Design, OpenAPI, applicable Functional Requirements, browser/session security rules, current frontend client/types/tests.             | Salesforce mappings, persistence internals, backend adapter code.    |
| Salesforce adapter     | Architecture, Implementation Design, Data Model mappings, Salesforce Security Design, adapter port/tests, sanitized fixtures.            | Frontend components and portal-persistence internals.                |
| Authentication/session | Security Design, OpenAPI authentication contract, Data Model persistence, relevant implementation modules/tests.                         | Salesforce business mappings and Account 360 presentation.           |
| Contract work          | OpenAPI, API Specification, approved security amendment, frontend/backend generated representations and contract checks.                 | Source-system queries and UI styling.                                |
| Test generation        | Requirement/design rule first, then public interface and existing tests; implementation only after expected behavior is stated.          | Unrelated implementation details that could bias expected outcomes.  |
| Debugging              | Failed command, minimal sanitized logs, relevant diff, governing rule, and nearby code/tests.                                            | Full logs, environment dumps, secrets, unrelated repository content. |
| Documentation/journal  | Approved inputs, accepted diff, human decisions, validation output, and effort notes.                                                    | Raw AI conversation transcript and unverified claims.                |

Focused context improves accuracy, boundary adherence, reviewability,
token efficiency, and detection of hallucinated assumptions. Broad
context can obscure the governing rule, expose unnecessary sensitive
material, and encourage cross-layer changes. Full-repository inspection
is appropriate only for explicit cross-cutting reviews such as
source-leakage, dependency, secret, or architecture-conformance scans.

### 8.1 AI tool and model selection

This plan intentionally does not make a specific AI vendor or model part
of the application architecture. AI engineering tools are selected per
work unit based on the task, available enterprise controls, context
needs, coding/review capability, and evidence quality.

Changing the engineering assistant or model does not change the approved
application architecture. However, any tool used with non-public
repository content must satisfy the project's security and data-handling
rules. Tool/model name and material configuration may be recorded in the
engineering journal when they affect reproducibility or the
interpretation of effectiveness evidence.

WorkflowFox should compare engineering outcomes rather than assume that
a newer or larger model is automatically better for every work unit.

## 9. Implementation Work Units

Each work unit ends with a reviewed diff, passing applicable validation,
updated traceability, and a concise engineering-journal entry. Failure
does not authorize moving ahead.

|  WU | Work unit                       | AI-assisted output                                                                                                                                                                     | Human gate                                                                                                        | Minimum exit evidence                                                                                                                                                          |
|----:|---------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   1 | Repository Foundation           | Approved folders, manifests, pinned toolchain/dependencies, ignore rules, repeatable build/lint/type/test/contract/security tasks, minimal frontend/backend test runners.              | Approve versions/dependencies and confirm no application behavior was added.                                      | Clean installs; frontend/backend builds or baseline starts; formatting, lint, type checks, and empty/smoke tests execute; secret scan passes.                                  |
|   2 | Backend Skeleton                | FastAPI delivery shell; application/domain/ports/adapters/core module boundaries; minimal startup and dependency wiring; no business behavior or additional API operation.             | Confirm modular-monolith dependency direction and absence of Salesforce/business implementation.                  | Import/startup smoke test, architecture/import checks, Ruff, mypy, pytest baseline.                                                                                            |
|   3 | Domain Models                   | Technology-neutral Employer Account, Contact, Enrollment, Summary, section-state, and domain-error models plus pure Summary rules.                                                     | Confirm no FastAPI, SQLite, Salesforce, or frontend dependency.                                                   | Unit tests from Domain/Data rules including empty, mixed statuses, invalid status, and reconciliation.                                                                         |
|   4 | API Models and Contract         | Delivery models/mappers for the three operations; approved frontend type generation; FastAPI error translation/conformance.                                                            | Contract owner confirms approved login-length amendment and that generated OpenAPI is not authoritative.          | OpenAPI 3.1/Spectral validation, examples/schema tests, generated-type check, backend contract comparison, no extra operation.                                                 |
|   5 | Portal Persistence              | SQLite migrations/repositories for `portal_users`, `portal_sessions`, and `login_attempts`; seed mechanism with protected password input.                                              | Approve physical conformance, uniqueness/indexes, no Salesforce business tables, no committed runtime data/hash.  | Migration/repository integration tests, constraint tests, clean seed test, data-ownership scan.                                                                                |
|   6 | Authentication and Session      | Argon2id verification/rehash, generic login, rate limits, opaque session lifecycle, cookie/CSRF/origin controls, logout, request-size/log redaction behavior.                          | Security owner reviews security-sensitive code and parameters line by line.                                       | Authentication/session/CSRF/injection/logging tests, cookie assertions, Bandit, dependency and secret scans, API conformance.                                                  |
|   7 | Salesforce Adapter              | Employer-information port implementation, OAuth boundary, allow-listed source requests, paging, timeout/token behavior, source-private models, mappings/errors; fixture gateway first. | Salesforce/security review confirms platform code stays in adapter and permissions remain read-only.              | HTTP-stub and mapping tests for correlation, Account, Contacts, Enrollment, paging, malformed data, timeouts, token reacquisition, safe errors; no live secret.                |
|   8 | Account 360 Application Service | Session-derived user context, Contact→Account authorization, required Account gate, independent child retrieval, Summary derivation, typed partial failure, request correlation.       | Confirm fail-closed authorization and exact partial-failure matrix.                                               | Application integration tests for success, empty states, every degradation combination, invalid correlation/context, unavailable parent, and Summary reconciliation.           |
|   9 | Frontend Foundation             | React/Vite shell, typed Portal API client, Login, session transition, application header, initial loading/logout foundation.                                                           | Approve no source terminology, no client token/business claims, no unapproved navigation/dependency.              | Type check, lint/format, build, Login tests, cookie-credential request behavior, generic errors, cleared password/protected state.                                             |
|  10 | Account 360 UI                  | Employer Overview, four-metric Summary, Contacts, Enrollment, responsive presentations, local 50/25-row paging.                                                                        | UX owner confirms fields, order, no actions/search/filter/backend paging, Workflow Insurance branding.            | Component/state tests, full/empty data rendering, paging range/math tests, 1,000-record render check, contract-field scan.                                                     |
|  11 | UX States                       | Loading, empty, section unavailable, both unavailable, Account page error, session expiration, network/logout failures, request reference.                                             | Confirm empty/unavailable distinction and no misleading zero Summary.                                             | Exact API-to-UX state tests, focus/status behavior, safe-text/source-leakage assertions, Playwright state scenarios.                                                           |
|  12 | Accessibility                   | Semantic structure, labels/errors, keyboard/focus, table/record semantics, live status, contrast/reflow/reduced-motion support and test scaffolding.                                   | Human accessibility review; automated scan alone is insufficient.                                                 | Automated accessibility checks, keyboard walkthrough, representative screen-reader results, contrast evidence, 320/360/768/1440 and 200% resize checks.                        |
|  13 | Live Salesforce Integration     | Environment configuration and explicitly enabled real-adapter validation using fictional representative data.                                                                          | Salesforce administrator/security owner approves identity, metadata, sharing, field access, and denied mutations. | OAuth success/failure, exact field/record permissions, correlation cardinality, Account 360 reconciliation, 50/1,000 bounds, latency/request count, no credential/log leakage. |
|  14 | Full Validation                 | Orchestrated clean validation run, evidence collection, scope/architecture/security/accessibility/contract reviews, documentation reconciliation.                                      | Humans accept results, exceptions, residual risks, and showcase readiness.                                        | Clean builds; all automated/manual checks; validation report; traceability complete; journal complete; no unresolved critical/high issue or unapproved deviation.              |

Mock Salesforce mode remains the default through Work Unit 12. Work Unit
13 is the first point at which protected development-org credentials and
real connectivity are required, and those values never enter AI context.

## 10. Standard AI Implementation Prompt Pattern

Every implementation request uses a bounded structure:

``` text
Task
- Implement Work Unit [N]: [specific outcome].

Approved Inputs
- [artifact path and relevant sections]
- [contract/schema path]
- [current interfaces/tests]

Traceability
- Requirements/rules: [FR/BR/SEC/API/UX/Data references]

Scope and Allowed Files
- [exact modules/files allowed]
- Preserve unrelated user changes.

Constraints
- Do not change architecture or approved specifications.
- Do not modify OpenAPI unless this task is an approved contract change.
- Do not add business capabilities or runtime AI.
- Do not add a dependency without documented human approval.
- Do not expose or replicate Salesforce data.
- Stop on specification conflict.

Acceptance Criteria
- [observable, testable outcomes]

Validation
- [exact repository commands/checks that must pass]
- [required manual/environment review]

Output
- Files created/changed.
- Traceability completed.
- Validation results and failures.
- Assumptions, deviations, and remaining risks.
- Stop after this work unit.
```

The prompt also includes the current relevant diff/status and any known
failing baseline check so AI cannot claim responsibility for, overwrite,
or conceal unrelated work.

`Build the employer portal` is not an acceptable prompt. It provides no
boundary, authority chain, review surface, stop condition, or definition
of done; it encourages invented behavior and makes correction evidence
difficult to isolate.

## 11. AI Change Control

AI must stop and report rather than improvise when:

- implementation and OpenAPI disagree;
- two approved artifacts conflict;
- expected behavior is absent or ambiguous;
- the architecture cannot implement a requirement without boundary
  change;
- Salesforce metadata, relationship, permission, or behavior materially
  differs from the Data/Security Design;
- a security control cannot be implemented as approved;
- a new dependency or platform-specific coupling appears necessary;
- a test exposes a specification inconsistency rather than an
  implementation defect; or
- existing user changes overlap the work unit and cannot be preserved
  safely.

Required report:

``` text
Specification conflict detected

Observed evidence:
[file, test, environment result]

Affected authority:
[artifact and section]

Why implementation cannot continue safely:
[impact]

Controlled options:
[smallest compliant alternatives and trade-offs]

Required human decision:
[owner/approval]
```

After approval, update the authoritative artifact first, revalidate it,
update the work-unit context/traceability, and then resume code. AI must
not hide a design change inside a refactor or test fix.

## 12. AI-Generated Code Review

Every AI-assisted change is reviewed against this checklist:

| Dimension       | Review questions                                                                                                       |
|-----------------|------------------------------------------------------------------------------------------------------------------------|
| Correctness     | Which approved requirement does the change implement? Are happy, negative, boundary, and failure paths correct?        |
| Scope           | Does it add an operation, field, screen, entity, workflow, or infrastructure item that was not approved?               |
| Architecture    | Do dependencies point inward? Is Salesforce isolated? Is business logic outside delivery/persistence/UI?               |
| Security        | Are authentication, session, CSRF, authorization, secrets, logging, input/output, and least-privilege controls exact?  |
| Contract        | Does behavior conform to the authoritative OpenAPI, including errors, states, nullability, and identifiers?            |
| Data            | Does SQLite contain only portal-owned operational data? Are correlation and source IDs handled correctly?              |
| Error handling  | Does required context fail closed? Do child sections degrade independently without turning unavailable into empty?     |
| Accessibility   | For frontend changes, are semantics, focus, labels, status announcements, responsive behavior, and contrast preserved? |
| Dependencies    | Is every addition approved, pinned, maintained, licensed appropriately, and necessary?                                 |
| Maintainability | Is the code typed, cohesive, comprehensible, and testable without the originating prompt?                              |
| Evidence        | Do tests and checks prove the behavior, or merely execute the generated path?                                          |

AI may produce a fresh-context review to reduce authoring bias, but a
human still owns disposition of every material finding.
Security-sensitive changes, Salesforce permission/mapping changes,
contract changes, and validation exceptions require the appropriate
specialist owner.

## 13. Validation-First Engineering

> Generated is not complete. Validated is complete.

Applicable validation must include:

- reproducible dependency installation and production builds;
- formatting and linting (`Prettier`, `ESLint`, `Ruff`);
- static type checking (TypeScript strict mode and `mypy`);
- backend unit/integration tests (`pytest`);
- frontend unit/component tests (`Vitest` and React Testing Library);
- end-to-end tests (`Playwright`);
- OpenAPI 3.1/Spectral validation, frontend type generation, and FastAPI
  contract conformance;
- authentication, session, CSRF, authorization, injection, redaction,
  permission, and source-leakage tests;
- dependency/static/secret checks (`pip-audit`, Node package audit,
  Bandit, Gitleaks, and approved equivalents);
- automated and human accessibility validation;
- architecture/data-ownership conformance review; and
- explicitly enabled Salesforce development-environment validation.

Work Unit 1 defines stable repository tasks that wrap the exact commands
and versions. A work unit records each applicable check as passed,
failed, not run with reason, or not applicable with justification.
Compilation alone is never sufficient.

Validation evidence must be reproducible from a clean checkout and must
not contain credentials, session values, sensitive configuration, or
real personal data.

## 14. Test Generation Strategy

Tests begin from approved behavior:

``` text
Functional Requirement / Business Rule
        ↓ expected outcome and forbidden outcome
Test case
```

``` text
Security threat / control
        ↓ attack or misuse condition
Security test
```

``` text
OpenAPI schema / invariant
        ↓ valid and invalid contract examples
Contract test
```

``` text
UX state model
        ↓ rendered content, absence, focus, announcement
Frontend test
```

Process:

1.  Cite the authoritative rule and write expected behavior without
    reading implementation internals where practical.
2.  Include success, empty, unavailable, unauthorized, malformed,
    boundary, and partial-failure cases applicable to the unit.
3.  Have a human review test intent and forbidden outcomes.
4.  Implement candidate code and tests; do not weaken the expectation to
    match the implementation.
5.  Run the test against a deliberately wrong or missing behavior when
    practical to prove it can fail meaningfully.
6.  Record gaps that require environment/manual evidence rather than
    fabricating an automated assertion.

Examples include deriving Summary reconciliation tests from BR/API
rules, session fixation tests from Security Design, state rendering from
UX §22, and adapter mapping tests from Data Model—not generating
assertions by echoing function branches.

## 15. AI-Assisted Debugging

``` text
Failure
   ↓
Capture minimal reproducible evidence
   ↓
Sanitize logs and identify governing specification
   ↓
AI proposes likely cause and smallest bounded correction
   ↓
Engineer reviews the diagnosis and diff
   ↓
Apply approved correction
   ↓
Rerun the failed check and applicable regression suite
   ↓
Record cause, correction, and evidence
```

Evidence supplied to AI should include the exact command, failure
output, relevant code/test diff, environment mode, and expected
rule—never full environment dumps or secrets.

Debugging must not succeed by disabling/skipping tests, loosening
type/lint rules, deleting negative cases, broadening Salesforce
permissions, leaking source errors, weakening security controls,
increasing timeouts without evidence, or changing the
contract/specification without approval.

## 16. Dependency Governance

AI may recommend a dependency but may not add or install it as an
incidental change. A dependency proposal answers:

1.  What approved requirement cannot be met reasonably without it?
2.  Can the selected framework, standard library, browser, or existing
    dependency solve the problem?
3.  Is the package actively maintained and compatible with pinned
    toolchains?
4.  What license, security, install-script, transitive, and supply-chain
    risks exist?
5.  Does it introduce vendor/platform coupling or leak across an
    architecture boundary?
6.  What testing, upgrade, removal, and replacement burden does it
    create?
7.  Is it proportionate to this small showcase?

Material dependency additions require human approval before the manifest
changes. Approved dependencies are pinned in lock files and pass clean
install, license review where applicable, audit, build, and regression
validation. AI convenience is not sufficient justification.

## 17. AI Security Rules

Never provide an AI system with:

- Salesforce client ID/secret, OAuth token, login endpoint credentials,
  or integration-user credentials;
- portal passwords, password hashes, raw/digested sessions, `.env`
  content, or CI secrets;
- real client or production data;
- real names, emails, phone numbers, Enrollment payloads, or operational
  logs containing them;
- unsanitized Salesforce responses, queries containing sensitive values,
  or database exports; or
- private keys, certificates, browser cookies, authorization headers, or
  credential screenshots.

Use fictional Workflow Insurance/Acme Manufacturing data and sanitized
failure evidence. Prompt records intended for publication are reviewed
and scanned like source files.

AI-generated work undergoes human security review plus secret scanning,
dependency scanning, static analysis, negative/security tests,
source-leakage checks, and applicable environment validation. AI cannot
authorize a security exception, reduce a control parameter, expand
Salesforce access, or approve a residual risk.

## 18. Engineering Journal Strategy

Each work unit eventually creates one concise Markdown entry under
`engineering-journal/`, named by work-unit number and subject. The
journal records engineering evidence, not a transcript.

Required content:

- objective and approved inputs;
- AI contribution and contribution classification;
- human decisions and approvals;
- files/modules affected at a useful summary level;
- problems, including AI mistakes and rejected proposals;
- corrections and why they were chosen;
- validation commands/checks and results;
- elapsed effort observations and significant manual rework;
- lessons learned; and
- reusable patterns/assets identified.

Raw prompt history, chain-of-thought, repetitive tool output, secrets,
sensitive payloads, and unreviewed claims are excluded. A small number
of sanitized reusable prompts may be retained separately under
`prompts/` when they teach a repeatable method.

The journal entry is completed with the work unit, not reconstructed at
the end of the project.

## 19. AI Contribution Classification

| Classification      | Meaning                                                                                        | Evidence expected                                        |
|---------------------|------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| **AI Generated**    | AI produced the initial candidate artifact or code for a defined portion.                      | Prompt/task reference and reviewed resulting files/diff. |
| **AI Assisted**     | Human and AI iteratively developed or corrected the result.                                    | Summary of contributions and material human changes.     |
| **Human Designed**  | Human-approved specifications or engineering judgment established the decision and boundaries. | Governing artifact/decision reference and owner.         |
| **Human Validated** | A human reviewed executed automated/manual evidence and accepted the result.                   | Validation result, reviewer, date, and exceptions.       |

A work unit can carry multiple classifications. For example, a component
can be Human Designed, AI Generated initially, AI Assisted during
correction, and Human Validated at acceptance. Classification describes
contribution; it is not a quality score.

## 20. Effectiveness Evidence

### 20.1 Engineering output

- work units started/completed and their cycle states;
- files/modules generated, modified, or rejected;
- candidate versus accepted AI contributions;
- tests added by category and specification source;
- documentation/journal/traceability artifacts created; and
- reusable prompts/checklists/patterns identified.

### 20.2 Validation

- clean build, format, lint, and type-check results;
- unit, integration, component, contract, security, accessibility,
  end-to-end, and Salesforce test counts/results;
- OpenAPI conformance and source-leakage results;
- dependency/static/secret scan results;
- manual accessibility and Salesforce permission evidence;
- defects found before work-unit acceptance; and
- unresolved exceptions with owner and expiry.

### 20.3 AI corrections and failures

Record meaningful examples where AI:

- invented or misunderstood a requirement;
- violated a layer or data-ownership boundary;
- hallucinated a framework/Salesforce/API behavior;
- introduced unnecessary abstraction or dependency;
- produced insecure or overly permissive code;
- leaked technical/source wording into the frontend;
- generated tests that agreed with an incorrect implementation; or
- proposed suppressing a symptom rather than correcting the cause.

The correction, reviewer reasoning, and validation outcome are as
valuable as the initial acceleration. They must not be hidden from the
engineering journal.

## 21. Effort Measurement

For each work unit record, approximately:

- ready/start/completion timestamps or elapsed engineering time;
- focused AI interaction time when it can be observed without burden;
- human planning/review time;
- significant manual correction/rework time;
- validation and environment-setup time;
- blocking time caused by specifications, dependencies, or external
  environments; and
- whether a comparable non-AI baseline exists.

Do not use lines of code, prompt count, or generated file count as a
proxy for value. Do not manufacture a baseline or claim `10x`
acceleration.

If no defensible baseline exists, report qualitative observations such
as faster scaffold drafting, broader initial test enumeration, or
reduced documentation effort, paired with the review/rework and
validation needed. Any quantitative comparison states its measurement
method, scope, and limitations.

### 21.1 Evidence interpretation

Effectiveness evidence should distinguish:

- **Observed:** directly measured during the work unit, such as elapsed
  time, validation results, accepted/rejected changes, or defect counts.
- **Derived:** calculated from observed evidence using a documented
  method.
- **Qualitative:** engineering observations that are useful but do not
  support a numerical productivity claim.
- **Not measured:** information that was not captured and must not be
  reconstructed later as if it were measured.

This prevents repository statistics, AI-generated line counts, or
retrospective estimates from being presented as productivity evidence.

## 22. Traceability

The showcase uses a lightweight Markdown table, not a
requirements-management platform:

| Trace ID | Requirement / rule            | Design authority      | Work unit | Implementation files | Test IDs/files | Validation evidence | Status / approver |
|----------|-------------------------------|-----------------------|----------:|----------------------|----------------|---------------------|-------------------|
| Example  | `FR-008` empty vs unavailable | API §§8–9; UX §§13–14 |     8, 11 | To be recorded       | To be recorded | To be recorded      | Planned           |

Traceability flow:

``` text
Requirement / Risk / Contract Rule
        ↓
Approved Design Artifact
        ↓
Implementation Work Unit
        ↓
Code or Configuration
        ↓
Specification-Derived Test
        ↓
Executed Validation Evidence
        ↓
Human Acceptance
```

Work units update their rows as paths and tests become real. A code path
without an approved trace is a scope warning; an approved rule without
implementation/test/evidence remains incomplete.

## 23. Engineering Journal Template

``` text
# Work Unit [N] — [Name]

## Objective

## Approved Inputs
- [artifact and section]

## Traceability
- [requirement/rule IDs and trace rows]

## AI Contribution
- Classification: [AI Generated / AI Assisted]
- AI tool/model (record only when relevant to reproducibility/evidence):
- Candidate work produced:

## Human Engineering Decisions
- Classification: Human Designed
- Decisions, rejected alternatives, approvals:

## Implementation Notes
- Files/modules affected:
- Dependency changes and approvals:

## Problems / AI Mistakes
- Observed issue and evidence:

## Corrections
- Change and engineering rationale:

## Validation
- Command/check:
- Result:
- Evidence location:
- Classification: Human Validated (when accepted)

## Effort Observations
- Approximate elapsed engineering time:
- AI interaction time, if useful:
- Human review/correction time:
- Validation/environment time:
- Baseline/limitations:

## Lessons Learned

## Reusable Assets
```

This template is itself a candidate reusable WorkflowFox asset. It
captures enough evidence for engineering and publishing without
preserving conversation noise.

## 24. Showcase Evidence Strategy

### 24.1 GitHub

GitHub will be the technical source of truth. It should eventually show
approved specifications, implementation boundaries, code, contract,
tests, validation report, traceability, selected sanitized prompts, and
concise journal entries. A reader should understand the application and
AI-assisted method without watching a video.

### 24.2 WorkflowFox website

The later website derivative should explain the business problem,
modernization pattern, specification-driven AI workflow, representative
implementation, validation evidence, corrections, and lessons. It should
distinguish observed evidence from interpretation and link to GitHub.

### 24.3 LinkedIn

Later posts should extract specific engineering insights—such as why
bounded prompts, source isolation, or specification-derived tests
mattered—rather than claim generic AI transformation or unsupported
speedups.

### 24.4 YouTube

The later walkthrough should follow:

``` text
Problem
→ Architecture
→ Specifications and Work Units
→ AI-Assisted Engineering
→ Working Application
→ Validation Evidence
→ AI Mistakes and Corrections
→ Lessons Learned
```

This phase plans evidence collection only. It does not create publishing
content.

## 25. Reusable WorkflowFox Assets

The following should be considered for extraction after implementation
proves and refines them:

1.  AI-Assisted Engineering Workflow
2.  Specification-to-Code Prompt Template
3.  Focused AI Context Manifest
4.  Bounded Work-Unit Definition-of-Ready/Done Checklist
5.  AI Change-Control Pattern and Conflict Report
6.  AI Code Review Checklist
7.  AI Security Checklist
8.  Validation-First AI Engineering Checklist
9.  Specification-Derived Test Design Pattern
10. AI-Assisted Debugging Pattern
11. Dependency Justification Template
12. Engineering Journal Template
13. AI Contribution Classification
14. Specification Traceability Template
15. Enterprise Integration Adapter Pattern
16. AI Effectiveness Evidence Scorecard without unsupported productivity
    claims

These are candidates, not separate deliverables in this phase.
Extraction occurs only after real work-unit evidence identifies what is
reusable.

## 26. Decisions and Trade-offs

| Decision                                                               | Reason                                                                            | Trade-off                                                                   | Future evolution                                                                   |
|------------------------------------------------------------------------|-----------------------------------------------------------------------------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| Bounded work units instead of whole-application generation             | Creates clear authority, context, review, validation, and correction boundaries.  | More prompts/gates and less apparent one-shot speed.                        | Combine units only after evidence shows the larger boundary remains reviewable.    |
| Specification-driven AI instead of conversational coding               | Keeps behavior traceable and prevents chat momentum from redefining requirements. | Requires maintained artifacts and deliberate preparation.                   | Automate context manifests/trace links without weakening approval.                 |
| Specification-derived tests instead of tests generated from code alone | Tests can detect a shared implementation mistake.                                 | Requires separate test-intent review and more upfront work.                 | Add stronger coverage/mutation techniques if justified by implementation evidence. |
| AI review assists; humans approve                                      | AI can broaden review but cannot own risk, context, or accountability.            | Human review remains a delivery cost and bottleneck.                        | Improve checklists/tooling; never remove accountable approval.                     |
| Focused context instead of full repository by default                  | Reduces noise, hallucination, cross-layer edits, and sensitive exposure.          | Relevant dependency context can be omitted accidentally.                    | Maintain task-specific context manifests and use explicit cross-cutting reviews.   |
| Speed is subordinate to validation discipline                          | Enterprise credibility requires executed evidence, not fast generation.           | Short-term output may appear slower than unvalidated prototyping.           | Automate repeatable validation while preserving gates.                             |
| AI dependency suggestions require governance                           | Prevents package sprawl, supply-chain risk, and unnecessary coupling.             | Useful libraries require a justification/approval step.                     | Maintain a reviewed dependency policy after repeated evidence.                     |
| Productivity claims require evidence                                   | Protects WorkflowFox credibility and makes limitations visible.                   | The showcase may support qualitative rather than dramatic numerical claims. | Establish comparable baselines in future showcases when measurement is practical.  |
| Journals capture evidence, not transcripts                             | Makes lessons readable and publishable while limiting sensitive/noisy content.    | Loses low-value conversational detail.                                      | Retain only selected sanitized prompts that demonstrate reusable methods.          |

## 27. Risks

| Risk                                                   | Impact                                                           | Mitigation and detection                                                                                                       |
|--------------------------------------------------------|------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| AI invents requirements or scope.                      | Unapproved capabilities and misleading showcase.                 | Bounded prompts, cited authority, explicit exclusions, traceability, scope review, stop-on-ambiguity.                          |
| Architecture drift.                                    | Salesforce/framework coupling and poor testability.              | Module/port boundaries, allowed-file lists, import/conformance checks, architecture review.                                    |
| Insecure generated code.                               | Credential/session/data exposure or authorization bypass.        | Human security review, threat-derived tests, static/secret/dependency scans, least-privilege validation.                       |
| Hallucinated APIs or Salesforce behavior.              | Broken or unsafe integration.                                    | Approved contract/metadata, official implementation references when needed, stub tests, real-org validation, stop on mismatch. |
| Unnecessary dependencies.                              | Supply-chain, maintenance, and complexity risk.                  | Dependency proposal/approval, platform-first review, lock files, audits, removal path.                                         |
| Tests validate implementation instead of requirements. | Code and tests share the same defect.                            | Specification-derived expected outcomes, human test-intent review, negative/boundary cases, prove tests fail.                  |
| Specification/code drift.                              | Documentation and contract no longer describe behavior.          | Traceability, generated-type/conformance checks, work-unit artifact review, change control.                                    |
| Secret or personal-data leakage to AI/prompts.         | Security/privacy exposure and publishable-history contamination. | Synthetic data, minimal sanitized context, prompt review, secret scan, no environment dumps.                                   |
| Excessive trust in AI review.                          | Plausible defects pass acceptance.                               | Human approval, deterministic tools, specialist reviews, environment evidence, record AI misses.                               |
| Compilation is mistaken for completion.                | Untested failures and unsupported quality claims.                | Definition of done requires all applicable validation and human acceptance.                                                    |
| Productivity is overclaimed.                           | Loss of enterprise credibility.                                  | Lightweight measured effort, stated limitations, no fabricated baseline or multiplier.                                         |
| Engineering journal becomes transcript noise.          | Unusable evidence and possible sensitive disclosure.             | Structured template, concise summaries, exclude raw chats/tool logs, reviewer edit.                                            |
| Context is too broad or too narrow.                    | Cross-layer drift or omitted governing rule.                     | Context manifest, task-specific matrix, stop when dependency authority is missing.                                             |
| AI hides a design change inside a fix.                 | Approved baselines become unreliable.                            | Diff review against allowed files, conflict workflow, artifact-first changes, trace updates.                                   |

## 28. Resolved Decisions and Implementation Evidence

### 28.1 Resolved engineering-process decisions

AI roles, human ownership, context strategy, work-unit sequence,
prompting pattern, change control, review, validation, testing,
debugging, dependency governance, security, journaling, classification,
evidence, effort measurement, traceability, and publishing-evidence
strategy are resolved by this plan.

### 28.2 Implementation evidence to collect

The following are evidence items, not open process questions and do not
block plan approval:

1.  Exact pinned tool/runtime versions and repository validation
    commands established in Work Unit 1.
2.  Actual work-unit elapsed, review, correction, validation, and
    environment effort.
3.  Accepted, reworked, and rejected AI contributions and representative
    failure categories.
4.  Actual test counts/results and contract/security/accessibility
    evidence.
5.  Salesforce development-org metadata, permission, sharing, mapping,
    latency, and volume-validation results.
6.  The final screen-reader/browser combination and manual accessibility
    evidence.
7.  Whether any defensible comparable non-AI baseline exists; otherwise
    only qualitative observations will be published.
8.  Which candidate WorkflowFox assets remain useful after real
    implementation and correction experience.

### 28.3 Controlled prerequisite

The approved LoginRequest maximum-length amendment must be incorporated
into and validated against `contracts/openapi.yaml` before Work Unit 4
acceptance. The decision is already made in Security Design; it is not
an open design question and this phase does not alter the contract.

### 28.4 Remaining process questions

No AI-engineering-process question remains open for this showcase.
Tool/model choice is an implementation-level decision governed by §8.1
and the security rules; it does not require an architecture amendment
unless it changes application design, data handling, or an approved
engineering control.

Implementation evidence may refine later reusable assets, estimates, and
publishing claims but cannot silently change this plan or the approved
application design.

## 29. Phase Exit Criteria

The AI-Assisted Engineering Plan is complete when reviewers have:

- approved the thesis that AI accelerates engineering without becoming
  engineering authority;
- approved permitted/prohibited AI scope and confirmed that the
  application contains no runtime AI;
- approved AI roles and explicit human ownership;
- approved the specification authority chain, readiness criteria, and
  conflict workflow;
- approved focused context strategy and context by task type;
- approved all 14 bounded implementation work units, human gates, and
  exit evidence;
- approved the standard prompt pattern, stop conditions, and
  change-control report;
- approved AI-generated code-review dimensions;
- approved validation-first definition of complete and applicable
  validation layers;
- approved specification-derived test generation and bounded debugging
  workflows;
- approved dependency governance and AI security rules;
- approved the journal strategy, contribution classification, reusable
  template, and traceability model;
- approved effectiveness and lightweight effort evidence, including the
  prohibition on unsupported acceleration claims;
- approved the showcase evidence strategy and candidate reusable
  WorkflowFox assets;
- confirmed the known OpenAPI hardening is treated as a controlled
  prerequisite rather than silently implemented;
- confirmed that no application code, frontend code, Salesforce
  implementation, OpenAPI change, architecture change, runtime AI, AI
  Agent, new dependency, or business capability was created; and
- approved progression to implementation.

The Phase 10 AI-Assisted Engineering Plan satisfies these criteria and
is approved for progression to implementation. The approved LoginRequest
maximum-length amendment remains a controlled prerequisite that must be
incorporated into and revalidated against `contracts/openapi.yaml`
before Work Unit 4 is accepted.

Implementation evidence listed in §28.2 remains mandatory evidence to
collect, not unresolved design work. Any material conflict discovered
during implementation must follow the controlled change process in §11
rather than being resolved through an undocumented code change.
