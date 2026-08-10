# API Specification — Employer Account Portal

**Showcase:** WorkflowFox Showcase #2  
**Phase:** 6 — API Specification  
**Status:** Draft for review  
**Authoritative contract:** [`contracts/openapi.yaml`](../../contracts/openapi.yaml)  
**Authoritative baselines:** [Business Discovery](../discovery/01-business-discovery.md), [Functional Requirements](../requirements/02-functional-requirements.md), [Domain Model](../domain-model/03-domain-model.md), [Solution Architecture](../architecture/04-solution-architecture.md), and [Implementation Design](../design/05-implementation-design.md)  
**Scope:** Login, logout, and read-only Employer Account 360

## 1. Executive Summary

The Portal API is the external contract between the Employer Portal frontend and the Application API. It exposes exactly three operations:

1. authenticate a portal-managed Employer Administrator;
2. invalidate the portal session; and
3. retrieve the authenticated user's composite Employer Account 360.

The contract uses a server-managed session represented to the browser by an opaque cookie. Employer context is never accepted from the frontend. The backend derives it from the authenticated portal user, the protected correlation relationship, and the trusted system of record.

Employer Account 360 is returned through one composite operation. The Employer Account is required; Contacts and Enrollment are independently stateful child sections. A child section can be available, confirmed empty, or unavailable without making the parent response fail. Enrollment Summary is available only when the complete Enrollment collection is trusted; an unavailable collection produces an unavailable Summary rather than misleading zero counts.

The API is business-oriented. It exposes approved business identifiers and fields while hiding Salesforce records, identifiers, field names, queries, credentials, and errors. The versioned surface is intentionally small, read-only, and contract-first.

## 2. API Goals

| ID | Goal | Contract response |
|---|---|---|
| APIG-001 | Business-oriented contract | Use Employer Account 360, employer, contacts, enrollment, and summary terminology. |
| APIG-002 | Salesforce isolation | Expose no Salesforce identifiers, objects, field names, query details, payloads, or error categories. |
| APIG-003 | Strong typing | Define closed reusable schemas, explicit enums, required properties, and standards-based dates. |
| APIG-004 | Session-owned context | Derive the Employer Account exclusively from the authenticated server-side session. |
| APIG-005 | Partial child-section degradation | Return explicit state and data for each child section inside a successful parent response. |
| APIG-006 | Empty/unavailable distinction | Require clients to use section state rather than infer meaning from null or missing data. |
| APIG-007 | Contract-first validation | Treat the reviewed OpenAPI file as authoritative and validate frontend and backend conformance. |
| APIG-008 | Small MVP surface | Provide only login, logout, and one composite Account 360 retrieval operation. |
| APIG-009 | Read-only employer data | Define no Account, Contact, or Enrollment mutation operation. |
| APIG-010 | User-safe failures | Use a small platform-neutral error taxonomy with a correlation identifier. |

## 3. API Boundary

```text
Employer Portal Frontend
          ↓ portal session and business-oriented HTTP contract
Portal API
          ↓ authenticated application invocation
Application Services
          ↓ internal employer-information gateway
Trusted Enterprise Source
```

The Portal API is not a Salesforce passthrough:

- the frontend communicates only with the Portal API;
- the API accepts no Salesforce identifier or query input;
- delivery models are separate from Salesforce source models;
- the backend determines employer context from the session;
- Business Services calculate Enrollment Summary and compose section states; and
- source failures are translated to application outcomes before reaching the contract.

The API boundary does not define the backend's Salesforce-facing interface.

## 4. API Operations

All paths use the relative base path `/api/v1`. No deployment hostname is part of the contract.

| Operation | Method | Path | Session requirement | Purpose |
|---|---|---|---|---|
| Login | `POST` | `/api/v1/auth/login` | None | Validate portal-managed username/password credentials and establish a server-managed portal session. |
| Logout | `POST` | `/api/v1/auth/logout` | Optional | Invalidate the supplied portal session when present; remain successful when it is absent or already invalid. |
| Retrieve Employer Account 360 | `GET` | `/api/v1/employer-account-360` | Required | Return the composite read-only Account 360 for the employer derived from the authenticated portal user. |

There are no Account, Contact, Enrollment, user-management, search, filtering, or CRUD operations.

## 5. Authentication Contract

### 5.1 Login

The login request contains only:

- `username`: required non-empty string; and
- `password`: required non-empty string.

Unknown usernames, incorrect passwords, and disabled users have the same external outcome. The API does not confirm whether a username exists.

Successful login returns `204 No Content` and establishes the server-managed session through `Set-Cookie`. No response body is required because no approved user profile or token payload is needed. The response does not include password data, Salesforce credentials, Contact identifiers, Account identifiers, the correlation UUID, or service-account information.

Invalid credentials return `401 Unauthorized` with `AUTHENTICATION_FAILED`. Structurally invalid input returns `400 Bad Request` with `INVALID_REQUEST`.

### 5.2 Session contract

- The OpenAPI security scheme models an opaque cookie named `portal_session`.
- The cookie value is meaningful only to Portal User Management and contains no frontend-readable employer or Salesforce business context.
- The browser sends the cookie to the Portal API according to the later Security Design and deployment-origin policy.
- The frontend does not place a business token in local storage or construct authorization claims.
- Cookie protection, signing, rotation, expiry, `Secure`, `HttpOnly`, `SameSite`, CSRF controls, and session fixation defenses belong to Security Design.

If the Account 360 request has no valid current session, the API returns `401 Unauthorized` with `SESSION_REQUIRED`.

### 5.3 Logout

Logout invalidates the current server-side session when one is present and instructs the browser to expire its session cookie. It returns `204 No Content` when the session is valid, absent, expired, or already invalid. This idempotent external behavior avoids making the client diagnose session state before logout.

An unexpected inability to process logout returns `500 Internal Server Error` with `INTERNAL_ERROR`; implementation details remain hidden.

## 6. Employer Account 360 Contract

`GET /api/v1/employer-account-360` returns the complete business representation for the employer derived by the backend from the authenticated portal session. The request accepts no employer, Contact, Account, correlation, query, filtering, or pagination input.

A successful `200 OK` response contains four required properties:

| Property | Business meaning |
|---|---|
| `employer` | Required Employer Account overview: Employer Name, Employer/Group ID, Status, and Industry. |
| `contacts` | Explicitly stateful collection of Contacts associated with the authorized Employer Account. |
| `enrollment` | Explicitly stateful collection of Enrollment Records associated with the authorized Employer Account. |
| `enrollmentSummary` | Available approved counts when Enrollment is complete and trusted; otherwise explicitly unavailable. |

The Employer Account is the required parent context. If authentication, correlation, Contact resolution, Account resolution, or Account overview retrieval fails, the API does not return a partially constructed `EmployerAccount360`; it returns an error response.

Once the Employer Account is valid, Contacts and Enrollment may degrade independently inside a successful `200 OK` response. This makes the HTTP result truthful: the requested Account 360 representation exists, but one or more optional child sections are explicitly unavailable.

## 7. Response Models

### 7.1 `EmployerAccount360`

| Property | Type | Required | Nullable | Meaning |
|---|---|---|---|---|
| `employer` | `EmployerAccount` | Yes | No | The required parent Employer Account. |
| `contacts` | `ContactSection` | Yes | No | One of the three explicit Contact section variants. |
| `enrollment` | `EnrollmentSection` | Yes | No | One of the three explicit Enrollment section variants. |
| `enrollmentSummary` | `EnrollmentSummary` | Yes | No | Available counts or explicit unavailable state. |

### 7.2 `EmployerAccount`

| Property | Type | Required | Nullable | Meaning |
|---|---|---|---|---|
| `employerName` | string | Yes | No | Employer's approved display name. |
| `employerGroupId` | string | Yes | No | Approved Employer/Group business identifier. Not a Salesforce record ID. |
| `status` | string | Yes | No | Employer business status. No unapproved status taxonomy is imposed. |
| `industry` | string | Yes | No | Employer industry description. |

All four properties must be present and non-empty for a successful Account 360 response. If required Account information cannot be trusted, the parent request fails.

### 7.3 `ContactSection`

`ContactSection` is a discriminated union on `state`:

- `available`: `items` contains one or more `EmployerContact` records;
- `empty`: `items` is an empty array confirmed by the trusted source; or
- `unavailable`: `items` is empty and `message` contains the approved safe unavailable message.

### 7.4 `EmployerContact`

| Property | Type | Required | Nullable | Meaning |
|---|---|---|---|---|
| `firstName` | string | Yes | No | Contact first name. |
| `lastName` | string | Yes | No | Contact last name. |
| `email` | email string or null | Yes | Yes | Contact email when available. |
| `phone` | string or null | Yes | Yes | Contact phone when available. |
| `roleTitle` | string or null | Yes | Yes | Approved Role/Title value when available. |

The API exposes no Contact record identifier.

### 7.5 `EnrollmentSection`

`EnrollmentSection` is a discriminated union on `state`:

- `available`: `items` contains one or more `EnrollmentRecord` values;
- `empty`: `items` is an empty array confirmed by the trusted source; or
- `unavailable`: `items` is empty and `message` contains the approved safe unavailable message.

### 7.6 `EnrollmentRecord`

| Property | Type | Required | Nullable | Meaning |
|---|---|---|---|---|
| `enrollmentId` | string | Yes | No | Approved Enrollment business identifier. |
| `memberDisplayName` | string | Yes | No | Approved employee/member display name. |
| `planName` | string | Yes | No | Employer-sponsored plan display name. |
| `status` | enum | Yes | No | `Active`, `Pending`, or `Terminated`. |
| `effectiveDate` | ISO 8601 date | Yes | No | Date-only effective date in `YYYY-MM-DD` form. |

The API exposes no Salesforce record identifier.

### 7.7 `EnrollmentSummary`

`EnrollmentSummary` is a discriminated union:

- `available`: required non-negative integer properties `total`, `active`, `pending`, and `terminated`; or
- `unavailable`: no count properties and the approved safe message.

An empty Enrollment collection produces an `available` summary with all counts equal to zero. There is no separate Summary `empty` state because zero counts are a complete and trusted summary.

### 7.8 `ErrorResponse`

| Property | Type | Required | Nullable | Meaning |
|---|---|---|---|---|
| `code` | `ErrorCode` enum | Yes | No | Small platform-neutral application error code. |
| `message` | string | Yes | No | User-safe message suitable for the client experience. |
| `requestId` | string | Yes | No | Opaque operational correlation value for support and logs. |

No timestamp is included because the approved client behavior does not require it. Response headers also include `X-Request-ID` when a response is produced by the Application API.

## 8. Section-State Model

| State | Contract shape | Business meaning | Frontend rule |
|---|---|---|---|
| `available` | One or more `items` | Complete trusted records exist. | Render the records. Do not reinterpret as empty. |
| `empty` | Empty `items` array | The trusted source successfully confirmed zero associated records. | Render the approved empty state. |
| `unavailable` | Empty `items` plus safe `message` | Complete trusted section data could not be obtained. | Render unavailable; do not treat as empty or reuse stale/partial records. |

The OpenAPI schemas use `oneOf` discriminated variants and closed objects. A section cannot be `available` with zero items, cannot be `empty` with records, and cannot be `unavailable` with partial records.

No section is represented by `null`, an omitted property, or an untyped object. Field-level nulls are permitted only for the explicitly nullable Contact email, phone, and role/title values; they do not change the section state.

## 9. Partial Failure Contract

| Scenario | `employer` | `contacts.state` | `enrollment.state` | `enrollmentSummary.state` | HTTP outcome |
|---|---|---|---|---|---|
| Complete success | Present | `available` | `available` | `available` | `200 OK` |
| Contacts empty | Present | `empty` | `available` or `empty` | `available` | `200 OK` |
| Enrollment empty | Present | `available` or `empty` | `empty` | `available` with zero counts | `200 OK` |
| Contacts unavailable | Present | `unavailable` | `available` or `empty` | `available` | `200 OK` |
| Enrollment unavailable | Present | `available` or `empty` | `unavailable` | `unavailable` | `200 OK` |
| Both child sections unavailable | Present | `unavailable` | `unavailable` | `unavailable` | `200 OK` |
| Required Account context unavailable | Absent | Not returned | Not returned | Not returned | Error response, normally `403` or `503` according to cause |

Required cross-model invariants:

- `enrollment.state: unavailable` requires `enrollmentSummary.state: unavailable`.
- `enrollment.state: empty` requires `enrollmentSummary.state: available` with all counts zero.
- `enrollment.state: available` requires `enrollmentSummary.state: available` and count reconciliation.
- Contacts state does not control Enrollment or Enrollment Summary state.
- Partial child failure never changes the response to `206 Partial Content`; the composite application request succeeded and describes its child states explicitly.

## 10. Error Contract

### 10.1 Error codes

| Code | Meaning | Typical operation |
|---|---|---|
| `AUTHENTICATION_FAILED` | Portal credentials were not accepted; no username-existence distinction is exposed. | Login |
| `SESSION_REQUIRED` | A valid current portal session is required. | Employer Account 360 |
| `ACCESS_UNAVAILABLE` | The authorized employer context could not be established safely. | Employer Account 360 |
| `ACCOUNT_360_UNAVAILABLE` | The required Employer Account 360 parent information could not be obtained. | Employer Account 360 |
| `INVALID_REQUEST` | The request does not conform to the approved contract. | Login or other malformed portal request |
| `INTERNAL_ERROR` | An unexpected Application API failure occurred. | Any operation |

The taxonomy intentionally does not distinguish Salesforce authentication, query, timeout, rate-limit, field, object, or payload failures. Such conditions are logged internally and translated to the appropriate platform-neutral code.

### 10.2 Message and correlation behavior

- Messages are safe for client presentation and must not contain internal data.
- The same error category uses consistent wording regardless of source-specific cause.
- `requestId` is generated or normalized by the Application API and links the response to redacted operational logs.
- A request ID is not a portal-user identifier, Salesforce identifier, correlation UUID, session identifier, email, or member identifier.
- Clients may display or provide the request ID to support personnel but must not infer business meaning from it.

### 10.3 Prohibited error information

Error responses must never include stack traces, source-system errors, queries, source payloads, internal exception class names, database errors, credentials, tokens, password information, service-account details, source identifiers, or configuration values.

## 11. HTTP Status Semantics

| Outcome | Status | Error code / response | Reason |
|---|---|---|---|
| Successful login | `204 No Content` | No body; session cookie established | Authentication succeeded and no response resource is required. |
| Failed login | `401 Unauthorized` | `AUTHENTICATION_FAILED` | Credentials were not accepted without disclosing which value failed. |
| Successful or already-logged-out logout | `204 No Content` | No body; session cookie expired when applicable | Idempotent client behavior simplifies session cleanup. |
| Session absent, expired, or invalid for Account 360 | `401 Unauthorized` | `SESSION_REQUIRED` | Authentication is required before employer information is returned. |
| Successful Account 360, including child degradation | `200 OK` | `EmployerAccount360` | Parent Account context is valid; child availability is part of the representation. |
| Invalid request | `400 Bad Request` | `INVALID_REQUEST` | Input does not conform to the contract. FastAPI's default validation behavior must be adapted to this approved contract. |
| Authorization/correlation context failure | `403 Forbidden` | `ACCESS_UNAVAILABLE` | A session exists, but the one approved employer context cannot be established safely. |
| Required Account 360 unavailable because a trusted dependency cannot provide it | `503 Service Unavailable` | `ACCOUNT_360_UNAVAILABLE` | The business operation is temporarily unavailable; the source cause remains hidden. |
| Unexpected server failure | `500 Internal Server Error` | `INTERNAL_ERROR` | The API failed unexpectedly without exposing implementation detail. |

Section-level Contacts or Enrollment degradation is not a protocol error. Returning `200 OK` with explicit section states is preferred over `206`, multiple frontend calls, or source-specific status codes.

## 12. Validation Rules

### 12.1 General rules

- JSON request and response objects are closed: unapproved properties are rejected.
- Every property marked required must be present.
- Null is rejected unless the schema explicitly includes null.
- Enumerations are case-sensitive contract values.
- Strings that identify or display an approved required business value must contain at least one character.
- Arbitrary maximum string lengths are not imposed without an approved business or security basis. Security Design may introduce request-size controls without changing business semantics.
- No response includes a timestamp because none is required.

### 12.2 Login validation

- `username` and `password` are required non-empty strings.
- Additional request properties are invalid.
- Contract validation does not define password-complexity rules; credentials are seeded rather than registered through this API.
- Every authentication failure returns the same external code and message.

### 12.3 Account 360 validation

- `employer`, `contacts`, `enrollment`, and `enrollmentSummary` are always present in a `200` response.
- Employer fields are required, non-null, and non-empty.
- Contact first and last names are required and non-empty; email, phone, and role/title properties are always present but may be null.
- A non-null email uses the standard email format.
- Enrollment fields are required, non-null, and non-empty where strings.
- Enrollment status must be `Active`, `Pending`, or `Terminated`.
- Effective date uses ISO 8601 date-only form (`YYYY-MM-DD`) with no timestamp or timezone.
- Available child sections contain at least one item.
- Empty and unavailable child sections contain exactly zero items.
- Only unavailable sections contain the safe unavailable message.

### 12.4 Summary reconciliation

For an available Enrollment collection:

- all counts are integers greater than or equal to zero;
- `total` equals the number of Enrollment items;
- `total = active + pending + terminated`; and
- each status count equals the number of corresponding records.

For an empty Enrollment collection, all four counts equal zero. For unavailable Enrollment, count properties are absent and the Summary is unavailable. These cross-object rules require application and contract tests because OpenAPI schema keywords alone do not express every reconciliation invariant clearly.

## 13. Identifier and Data Exposure Rules

### 13.1 Allowed identifiers

| Identifier | Exposure | Reason |
|---|---|---|
| Employer/Group ID | Exposed as `employerGroupId` | Approved business identifier required by Employer Account overview. |
| Enrollment ID | Exposed as `enrollmentId` | Approved business identifier required by Enrollment display. |
| Error request/correlation ID | Exposed as `requestId` and `X-Request-ID` | Opaque operational value with no business or source identity meaning. |

### 13.2 Forbidden identifiers and details

The API must not expose or accept:

- Salesforce Account, Contact, Enrollment, User, or service-account record IDs;
- the portal-user UUID;
- the portal-user-to-Contact correlation UUID;
- internal SQLite user or session identifiers;
- session contents or employer claims;
- Salesforce object or field API names;
- SOQL or any source query criteria;
- Salesforce URLs, API versions, credentials, tokens, or source payload metadata; or
- internal adapter, exception, database, or configuration identifiers.

The frontend cannot request another employer by modifying a URL, query parameter, request body, or header because no employer-selection input exists.

## 14. Pagination Decision

The MVP does not paginate Contacts or Enrollment in the Portal API.

The decision is based on the approved showcase assumptions of approximately 50 Contacts and 1,000 Enrollment Records for one Employer Account, one current Account 360 load, no filtering or search use case, and a preference for one understandable composite response. The backend adapter remains responsible for completing any source-side paging before it produces the trusted collection.

Benefits:

- one request produces one internally consistent Account 360 snapshot;
- Enrollment Summary reconciles to the complete returned Enrollment collection;
- frontend state, contract schemas, examples, and demonstrations remain simple; and
- no cursor, page-size, filtering, or sorting behavior is invented.

Trade-off: response size and latency grow with Enrollment volume. Pagination must be reconsidered if measured representative payloads or latency do not satisfy the approved response target, if Account volumes materially exceed the showcase assumption, or if a later approved UX requires incremental navigation. Such a change requires a versioned contract decision; it is not predesigned here.

## 15. Versioning Strategy

The API uses one major version segment in the base path: `/api/v1`.

- Compatible additions within the approved scope may retain `v1` only when existing client behavior remains valid.
- Breaking changes require explicit review and a new major path version.
- The OpenAPI `info.version` tracks the contract artifact version separately from the path major version.
- No custom version header, date-based version, content negotiation scheme, or simultaneous version-management framework is introduced.

This strategy is visible, simple to route and test, and proportionate to one frontend client and three operations.

## 16. OpenAPI Ownership

[`contracts/openapi.yaml`](../../contracts/openapi.yaml) is the approved external API contract after this phase passes review.

- API Design owns changes to the contract.
- FastAPI's generated OpenAPI description must conform to this file.
- Framework-generated output is implementation evidence and is not automatically authoritative.
- Frontend TypeScript types may be generated from this approved file.
- Generated types and documentation must not be edited to introduce unapproved fields or operations.
- Any business-significant contract change requires traceability to an approved upstream artifact and review of compatibility.

## 17. Contract Validation

Validation will include:

- parse `contracts/openapi.yaml` as YAML and validate it as OpenAPI 3.1;
- lint operation identifiers, schema references, descriptions, examples, and versioned paths;
- confirm exactly three operations and no deployment hostname;
- generate frontend TypeScript types and require a clean generation result;
- compare FastAPI-generated OpenAPI with the approved contract and fail incompatible differences;
- validate representative login, complete Account 360, empty-section, Contacts-unavailable, Enrollment-unavailable, and both-unavailable examples;
- test every error code against its permitted operation and HTTP status;
- test closed-object, enum, date, required, nullability, and section-state rules;
- test Enrollment/Summary cross-object reconciliation;
- scan the contract for Salesforce object names, source identifiers, queries, credentials, framework details, and unapproved operations; and
- retain validation output as later Validation evidence.

Contract validation does not replace application, security, integration, or user-experience validation.

## 18. Security Considerations

At the API boundary:

- Account 360 requires a valid server-managed portal session.
- Login and logout are the only unauthenticated/optionally authenticated operations.
- Employer context is derived on the server and cannot be selected by the client.
- The frontend never receives the correlation UUID, internal identity, employer claim, Salesforce identifier, source credential, or service-account information.
- The session cookie is opaque; its protection and lifecycle belong to Security Design.
- Invalid authentication does not disclose username existence.
- Context resolution fails closed.
- Partial child failure begins only after the required Account context is established.
- Request validation rejects unapproved properties.
- Errors and section messages expose no source or implementation details.
- Account 360 is read-only and uses a safe retrieval method.

Security Design must confirm session-cookie attributes, CSRF treatment for session-changing operations, cross-origin policy, request-size controls, authentication throttling, and response headers. If a control requires a contract-visible header or cookie change, the OpenAPI contract must be revised and revalidated before implementation.

## 19. Alternatives and Trade-offs

| Decision | Selected approach | Reason | Trade-off / rejected alternative |
|---|---|---|---|
| Composite vs resource APIs | One composite Account 360 retrieval. | Authorization, source orchestration, Summary, and partial states remain consistent and backend-owned. | Separate Account, Contact, and Enrollment calls could reduce individual payloads but would duplicate context handling and create cross-call consistency problems. |
| Session vs client token | Opaque server-managed session cookie. | Matches approved portal-owned sessions and keeps employer/source information off the client. | A token-oriented client contract could ease some distributed deployments but would expose more security design to the frontend and is not required. |
| Explicit states vs nullable data | Discriminated section-state objects. | Prevents empty, unavailable, absent, and incomplete data from being conflated. | Nullable collections are shorter but force business inference into the frontend. |
| Pagination vs complete collections | No portal-API pagination at approved MVP scale. | Keeps one consistent response and Summary aligned with returned records. | Larger responses depend on bounded scale and must be measured. |
| Generic vs source errors | Small application error taxonomy. | Prevents platform coupling and information leakage. | Source-specific errors might aid developers but belong in redacted internal logs, not the external contract. |
| Login response body vs no content | `204 No Content` plus session cookie. | No approved user profile or client token is required. | A login response object could provide redundant authenticated flags or identifiers without business value. |
| Logout strictness vs idempotence | Return `204` even when the session is absent or invalid. | Client cleanup remains safe and simple. | Strict `401` logout would add a state branch without improving protection. |
| Partial response status | `200 OK` with typed child states. | The parent Account 360 representation is valid and complete about its known states. | `206 Partial Content` is intended for range semantics and would not express business-section availability. |

## 20. Risks

| ID | Risk | Impact | Contract mitigation |
|---|---|---|---|
| APIR-001 | Salesforce structure leaks into names or examples. | Frontend coupling and loss of platform neutrality. | Business schemas, closed objects, forbidden-name scan, and adapter-only source mapping. |
| APIR-002 | Frontend and backend drift from the approved contract. | Runtime failures and inconsistent partial-state behavior. | Contract authority, generated frontend types, backend comparison, and contract tests. |
| APIR-003 | Partial failure is ambiguous. | Unavailable data may appear empty or misleading. | Discriminated states, exact item-count rules, cross-model invariants, and examples. |
| APIR-004 | Enrollment response becomes oversized. | Latency, browser rendering, or transfer issues. | Approved bounded scale, payload measurement, no speculative pagination, and explicit reconsideration trigger. |
| APIR-005 | Internal or source identifiers are exposed. | Authorization bypass attempts, leakage, and coupling. | No identifier inputs, allow-listed business fields, schema review, examples, and automated forbidden-term scans. |
| APIR-006 | Error detail leaks source or credentials. | Security exposure and platform coupling. | Small enums, safe messages, closed ErrorResponse, and negative tests. |
| APIR-007 | API is over-versioned. | Maintenance overhead disproportionate to three operations. | One path major version and no additional version framework. |
| APIR-008 | FastAPI-generated OpenAPI becomes accidentally authoritative. | Framework defaults can silently alter statuses, validation, or schemas. | Approved file ownership and automated conformance comparison. |
| APIR-009 | Framework defaults return unapproved validation errors. | Contract inconsistency and technical-detail leakage. | Require `400 INVALID_REQUEST` translation and error-contract tests. |
| APIR-010 | Cookie-session security adds a later contract requirement. | The approved contract may need a CSRF header or origin-related update. | Security review before implementation and controlled contract revision with validation. |

## 21. Open Questions

Only API-visible security details remain unresolved:

1. Will Security Design require a client-supplied CSRF header or token for login/logout or other cookie-authenticated operations? If yes, its acquisition and submission contract must be added before implementation.
2. Will frontend and backend use the same origin or approved cross-origin credentials? This does not change business operations, but it affects cookie and CORS contract documentation.
3. Does Security Design approve the contract cookie name `portal_session`, or require an environment-neutral alternative? The cookie remains opaque either way.

Password hashing, Salesforce service authentication, source field mappings, and deployment infrastructure are important later decisions but are not external Portal API contract questions.

## 22. Phase Exit Criteria

API Specification is complete when reviewers have:

- approved the three operations and no others;
- approved `/api/v1` and the operation paths;
- approved login, logout, and session behavior;
- approved the composite Employer Account 360 response models;
- approved explicit Contact, Enrollment, and Summary states;
- approved the complete partial-failure matrix and parent Account fail-closed rule;
- approved the six-code application error taxonomy and HTTP status semantics;
- confirmed all required, nullable, enum, date, closed-object, collection, and Summary reconciliation rules;
- approved business-identifier exposure and prohibited internal/source identifiers;
- approved the no-pagination decision for the bounded MVP;
- confirmed `contracts/openapi.yaml` as the contract authority;
- validated the OpenAPI document and all examples with an OpenAPI 3.1-capable linter;
- confirmed that Salesforce concepts, queries, identifiers, errors, and credentials do not leak into the contract;
- confirmed that no backend code, frontend code, Salesforce API design, security algorithm, runtime AI, or additional use case has been created; and
- approved progression to Security Design.

Until these criteria are met, these artifacts remain API Specification drafts and implementation must not treat them as approved.
