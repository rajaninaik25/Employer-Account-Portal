# Security Design — Employer Account Portal

**Showcase:** WorkflowFox Showcase #2<br>
**Phase:** 7 — Security Design<br>
**Status:** Draft for review<br>
**Authoritative baselines:** [Business Discovery](../discovery/01-business-discovery.md), [Functional Requirements](../requirements/02-functional-requirements.md), [Domain Model](../domain-model/03-domain-model.md), [Solution Architecture](../architecture/04-solution-architecture.md), [Implementation Design](../design/05-implementation-design.md), [API Specification](../api/06-api-specification.md), and [`contracts/openapi.yaml`](../../contracts/openapi.yaml)<br>
**Scope:** Login, logout, server-side sessions, authorization, and read-only Employer Account 360

## 1. Executive Summary

The Employer Account Portal uses a small, layered security model appropriate for a read-only showcase. The portal authenticates its own fixed sample users; those users are not Salesforce Users. A successful login creates an opaque, server-managed session. Each Account 360 request reloads the enabled portal user and follows the protected correlation relationship to exactly one Salesforce Contact and then exactly one Salesforce Account. The browser cannot select or override any part of that authorization context.

Portal passwords are protected with Argon2id. Session identifiers are high-entropy random values stored only as one-way digests in SQLite and sent in an `HttpOnly`, `Secure`, `SameSite=Strict` cookie named `portal_session`. The frontend and API operate on the same origin. Strict cookie behavior, exact-origin checks, Fetch Metadata, JSON-only state-changing requests, and no credentialed cross-origin access provide proportionate CSRF protection without adding a client-visible CSRF token.

The backend connects to Salesforce through an OAuth 2.0 client credentials flow configured in a Salesforce External Client App and bound to one dedicated, API-only integration user. That identity receives only the read access required for approved Account, Contact, Enrollment, relationship, and correlation fields. Employer Administrator credentials are never sent to Salesforce.

All controls preserve the approved architecture: business data remains read-only and authoritative in Salesforce, source-system details remain isolated in the adapter, errors remain user-safe, and Contacts or Enrollment may degrade only after the required employer context has been established. This phase adds no business capability, application code, cloud service, or Salesforce redesign.

Security parameters are informed by current [OWASP password-storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), [OWASP session-management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html), [OWASP CSRF](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html), [RFC 9106](https://www.rfc-editor.org/rfc/rfc9106.html), and [Salesforce client-credentials](https://help.salesforce.com/s/articleView?id=configure_client_credentials_flow_for_external_client_apps.htm&language=en_US&type=5) guidance. These references calibrate controls; the approved project artifacts remain the only source of business scope and behavior.

## 2. Security Scope

This design covers:

- portal username/password authentication for the fixed sample users;
- password hashing and seed-user credential handling;
- opaque server-side session creation, use, expiry, rotation, and revocation;
- authorization from portal user to one Contact and one Employer Account;
- CSRF, input, browser, API, and injection controls;
- dedicated Salesforce integration identity and OAuth token handling;
- secrets, logging, dependencies, and AI-assisted engineering controls; and
- security validation for the three approved API operations.

The showcase does not include self-service registration, invitations, password reset, MFA, enterprise SSO, user administration, cross-origin clients, public APIs, Salesforce delegated identity, write operations, a WAF, API gateway, SIEM, managed vault, cloud-specific controls, or runtime AI. Those controls or capabilities require later approval and are not implied by this design.

## 3. Security Objectives

| ID | Objective | Required outcome |
|---|---|---|
| SEC-001 | Credential confidentiality | Plaintext passwords, reusable hashes, Salesforce secrets, and access tokens never enter source control, responses, or logs. |
| SEC-002 | Strong authentication | Only an enabled portal user with a verified password receives a session; failures do not enumerate usernames. |
| SEC-003 | Session protection | Sessions are unpredictable, server-controlled, time-bounded, rotated after login, revocable, and inaccessible to browser scripts. |
| SEC-004 | Employer authorization | Employer context is derived exclusively from the authenticated portal user and exact Salesforce relationships; any ambiguity fails closed. |
| SEC-005 | Least privilege | The Salesforce identity can read only the approved source objects and fields and cannot mutate business data or administer the org. |
| SEC-006 | Source isolation | Salesforce identifiers, queries, tokens, errors, and payloads do not cross the Portal API boundary. |
| SEC-007 | Input and output integrity | Closed schemas, parameterized persistence, static source-query templates, source validation, and encoded rendering prevent injection and unsafe output. |
| SEC-008 | Safe failure | Authentication, authorization, integration, and unexpected failures return approved generic outcomes without sensitive detail. |
| SEC-009 | Operational accountability | Security-relevant events carry request IDs and useful categories without recording credentials or unnecessary business data. |
| SEC-010 | Verifiable engineering | Automated and environment-specific tests demonstrate the controls before implementation is approved. |

## 4. Trust Boundaries

```text
Employer Administrator
        ↓ credentials and user actions
Browser
        ↓ same-origin HTTPS; opaque session cookie
Portal API
        ↓ authenticated user and request context
Application Services
        ↓ business-oriented gateway calls
Salesforce Adapter
        ↓ OAuth access token and allow-listed source requests
Salesforce
```

| Boundary | Trust change | Required controls |
|---|---|---|
| Administrator → Browser | Human input enters an untrusted client environment. | Password field handling, no credential persistence, generic errors, XSS protections. |
| Browser → Portal API | Every request is untrusted even when it carries a cookie. | HTTPS, cookie validation, origin/Fetch Metadata checks, closed schemas, size limits, authentication throttling. |
| Portal API → Application Services | Transport input becomes an application command. | Approved operation allow-list, request ID, authenticated context, business error translation. |
| Application Services → Salesforce Adapter | Business intent crosses into source-specific behavior. | Inward-facing interface, server-derived correlation, static mappings, no client query criteria. |
| Salesforce Adapter → Salesforce | The application exercises a privileged machine identity against the system of record. | External Client App, dedicated integration user, OAuth client credentials, TLS, least privilege, bounded tokens and timeouts. |
| Any component → Logs/configuration | Operational data could become a secondary disclosure path. | Field allow-lists, redaction, restricted access, secrets outside source, no raw payload logging. |

No response crossing back toward the browser may contain Salesforce credentials, record IDs, field names, queries, source errors, the portal-to-Contact correlation UUID, or internal session identifiers.

## 5. Authentication Design

### 5.1 Login flow

1. Accept only `POST /api/v1/auth/login` with an `application/json` body conforming to the closed `LoginRequest` schema.
2. Normalize the username by trimming surrounding whitespace, applying Unicode NFKC normalization, and performing a case-insensitive lookup. The password is never trimmed or normalized.
3. Apply the login-abuse limits before expensive password verification.
4. Look up the portal user through a parameterized repository query. If no user exists, verify the submitted password against a fixed valid dummy Argon2id encoding.
5. Verify the password through the approved Argon2id library. Check the enabled state only within the same generic authentication decision.
6. For an unknown username, wrong password, disabled user, or throttled attempt, return `401 AUTHENTICATION_FAILED` with the same user-safe message and no user-existence signal.
7. On success, atomically revoke existing sessions for the user, create a new session, and return the approved `204 No Content` with `Set-Cookie`.

The application does not send portal credentials to Salesforce, include user or employer data in the login response, or disclose which authentication check failed.

### 5.2 Login abuse protection

The MVP uses SQLite-backed local counters, not a distributed anti-fraud service:

- maximum five failed attempts for one normalized username in a rolling 15-minute window;
- maximum 20 login attempts from one client IP in a rolling five-minute window;
- successful authentication clears the username counter but not the IP window;
- expired counter entries are removed during normal cleanup;
- unknown usernames still receive one dummy password verification until the applicable limit is reached; and
- throttled requests retain the generic `401 AUTHENTICATION_FAILED` response rather than introduce a username-sensitive branch.

The application trusts a forwarded client IP only when it arrives through an explicitly configured trusted proxy; otherwise it uses the direct peer address. Raw usernames and IP addresses are not required in ordinary authentication logs. This local limiter is appropriate to one application instance; distributed enforcement is a future production concern.

## 6. Password Storage Design

### 6.1 Selected algorithm and parameters

| Property | Decision |
|---|---|
| Algorithm | Argon2id, version 1.3 (`v=19`). |
| Memory cost | 65,536 KiB (64 MiB). |
| Time cost | 3 iterations. |
| Parallelism | 1 lane. |
| Salt | 16 random bytes generated independently for every password by the approved library and embedded in the standard encoded value. |
| Output | 32-byte tag stored in the standard self-describing Argon2 encoded string. |
| Comparison | The library's verification function; no hand-written comparison. |

The selected work factor exceeds OWASP's current Argon2id minimum and uses the 64 MiB/three-pass profile described by RFC 9106, with one lane to keep resource use predictable in the small backend. Implementation validation must measure the chosen runtime. The parameters may be increased when the target environment supports it; they must not be reduced below OWASP's current minimum without a recorded security decision.

### 6.2 Storage and lifecycle

- Store only the encoded Argon2id value in the runtime SQLite user record. Never commit a runtime database, password hash, or password to Git.
- Use a unique library-generated salt; do not maintain a shared or application-defined salt.
- Do not add a pepper for this MVP. A pepper would create another centrally managed secret and recovery/rotation dependency without an approved managed-secret capability. Reconsider it with production secret management.
- After successful verification, inspect the encoded version and parameters. Rehash immediately when the approved library reports that an upgrade is required.
- Generate the dummy hash once at process startup from random input, keep it in memory at the same approved parameters, and never treat it as a reusable user credential.
- Passwords, hashes, salts, and verification exceptions never appear in application logs or API responses.

### 6.3 Seed-user setup

Seed tooling will accept each sample password through a protected interactive prompt or a transient environment input, hash it at seed time, and persist only the encoded hash in the ignored runtime database. Sample passwords must be independently generated, at least 16 characters, unique to the showcase environment, and changed before any public or shared demonstration environment is used. Documentation may explain how to create local credentials but must not publish a functioning shared credential.

Plaintext storage, reversible encryption, unsalted hashes, shared salts, and direct use of fast general-purpose hashes such as SHA-256 for passwords are prohibited.

## 7. Session Security Design

### 7.1 Session identifier and server-side record

- Generate 32 random bytes (256 bits) from the operating system CSPRNG and encode them as an unpadded base64url value.
- Return the opaque value only in the `portal_session` cookie. It contains no user, employer, Salesforce, authorization, or expiry claims.
- Store only a SHA-256 digest of the high-entropy session value in SQLite. SHA-256 is appropriate here for lookup of a random 256-bit token; it is not used for passwords.
- Associate the server record with the internal portal-user identifier, creation time, last-seen time, absolute expiry, and revocation state. This is a conceptual security requirement, not a physical schema definition.
- Reload the portal user for every authenticated operation and verify that the user remains present and enabled. The session does not store the correlation UUID or Salesforce Account context.

### 7.2 Cookie contract

The production cookie is:

```text
portal_session=<opaque-value>; Path=/api/v1; HttpOnly; Secure; SameSite=Strict
```

The cookie has no `Domain` attribute and no client-controlled `Expires` or `Max-Age`; it is therefore a browser-session cookie. Server-side expiry remains authoritative. All login, logout, and Employer Account 360 responses use `Cache-Control: no-store`. The browser must not copy the session value into JavaScript storage.

`Secure` is mandatory outside localhost. A development-only localhost profile may relax it solely when local HTTPS is unavailable; startup must reject that profile on non-loopback hosts.

### 7.3 Lifetime, rotation, and concurrency

| Control | Decision |
|---|---|
| Absolute lifetime | Eight hours from successful login; never extended by activity. |
| Idle timeout | 30 minutes since last accepted authenticated use. |
| Last-seen write | Update at most once every five minutes to limit SQLite write contention without extending the 30-minute rule. |
| Login rotation | Always create a new session value after password verification; revoke any session supplied on the login request. |
| Privilege/state rotation | Create a new value after any future security-sensitive identity-state change; no such user-facing operation exists in the MVP. |
| Periodic rotation | Not used mid-session in the MVP; idle and absolute limits bound exposure without multi-tab rotation races. |
| Concurrent sessions | One active session per portal user. A successful new login atomically revokes all prior sessions for that user. |
| Logout | Atomically revoke the presented session and expire the cookie with the same name and path; remain externally idempotent with `204`. |

Expired, revoked, malformed, or unknown session values produce `401 SESSION_REQUIRED` on Employer Account 360 and cause the cookie to be cleared. Session lookup compares the digest through the persistence layer and never logs the supplied value. Expired and revoked rows are removed during startup and periodic in-process maintenance; no separate service is required.

The session is not bound to a fixed IP address or User-Agent because legitimate network and browser changes would create unreliable authorization failures. The short idle limit, one-session policy, cookie controls, and revocation provide the proportional protection.

## 8. Authorization Design

Authorization follows one immutable server-side chain:

```text
Authenticated Portal User
        ↓ portal-owned correlation UUID
Salesforce Contact
        ↓ exactly one Account relationship
Salesforce Account
        ↓ approved read-only business data
Employer Account 360
```

The session identifies only the internal portal user. Application Services reload that user, require `enabled = true`, obtain the protected correlation UUID, and pass it to the Salesforce gateway. The frontend supplies no Contact, Account, employer, correlation, query, filter, or paging identifier. Query parameters or bodies on the Account 360 operation are rejected rather than ignored.

| Condition | Authorization result |
|---|---|
| Missing or malformed correlation UUID | Fail closed with `403 ACCESS_UNAVAILABLE`; return no employer data. |
| No Contact matches | Fail closed with `403 ACCESS_UNAVAILABLE`. |
| More than one Contact matches | Fail closed as a correlation-integrity violation. |
| Contact has no Account | Fail closed with `403 ACCESS_UNAVAILABLE`. |
| Contact relationship is ambiguous or resolves to multiple Accounts | Fail closed as a relationship-integrity violation. |
| Account cannot be retrieved or validated | Fail the complete Account 360 operation; use `403` for invalid context or `503` for temporary trusted-dependency unavailability. |
| Portal user is disabled, absent, or session invalid | Revoke/reject the session and return `401 SESSION_REQUIRED`. |

Only after this gate succeeds may Contacts and Enrollment degrade independently according to the approved API. An unavailable child section never weakens employer authorization and never exposes partial source records. Enrollment Summary is withheld when Enrollment is incomplete or unavailable.

No client-supplied value may be used to widen Salesforce selection. Internal Salesforce record identifiers needed to traverse relationships remain within the adapter and are never returned.

## 9. CSRF Protection

The MVP adopts a same-origin deployment and does not enable credentialed CORS. `POST /api/v1/auth/login` and `POST /api/v1/auth/logout` use the following combined CSRF controls:

1. Require `Content-Type: application/json` for login; reject form-encoded, multipart, text, or missing login content types. Logout accepts no body and rejects a non-empty body.
2. Require the `Origin` header to exactly match the configured public portal origin. If `Origin` is absent, accept only an exact same-origin `Referer`; reject `null`, malformed, missing, or mismatched values.
3. When `Sec-Fetch-Site` is present, require `same-origin`; treat `same-site`, `cross-site`, and unexpected values as untrusted for the POST operations.
4. Set `portal_session` with `SameSite=Strict`, `Secure`, and no `Domain` attribute.
5. Do not emit CORS allow-origin or allow-credentials headers.

`GET /api/v1/employer-account-360` is read-only and performs no state change. It still requires a valid session and must never derive a request from attacker-controlled URL fragments or client-supplied source identifiers.

No synchronizer or double-submit CSRF token is required while all five same-origin assumptions remain true. This removes unnecessary frontend token choreography while providing layered protection for both login CSRF and logout CSRF. If a cross-origin frontend is later approved, this decision must be replaced with an explicit token mechanism and a revised, validated API contract.

**API impact:** no new CSRF header or operation is required. The approved methods, paths, cookie name, responses, and business models remain unchanged.

## 10. Input Validation and Injection Protection

### 10.1 Portal API input

- Accept JSON only for login; cap the body at 8 KiB before parsing.
- Require `username` and `password` only; reject unknown properties, arrays, objects, nulls, and empty strings.
- Limit username to 128 Unicode characters and password to 256 Unicode characters to bound parser, lookup, and password-hashing work.
- Normalize only the username as defined in Section 5. Password bytes remain exact.
- Reject request bodies and query parameters on logout and Account 360.
- Normalize or replace externally supplied request IDs; permit only a bounded printable identifier and generate a server value when invalid.

### 10.2 Persistence and source queries

- Use parameterized SQLite statements through the persistence library. Never concatenate username, session, or correlation values into SQL.
- Validate the stored correlation value as a UUID before adapter use.
- Build Salesforce requests from static, reviewed query templates and allow-listed object and field mappings owned by the adapter.
- Treat source object names and field API names as validated startup configuration, never runtime client input.
- Bind or safely escape the correlation value through the adapter's query mechanism; never accept user-supplied SOQL, clauses, field lists, sort expressions, or source paging values.
- Apply bounded connection/read timeouts and source response-size safeguards. Never truncate a collection and present it as complete.

### 10.3 Source and output validation

Salesforce responses first enter closed adapter-private models. Required values, allowed Enrollment statuses, relationship cardinality, paging completeness, string types, and date formats are validated before mapping to domain models. Invalid required Account data fails the parent operation; invalid child data makes that complete child section unavailable.

The frontend renders all business values as text through React's normal encoding. Raw HTML, dynamic script execution, and `dangerouslySetInnerHTML` are prohibited. No Salesforce content is treated as trusted markup.

## 11. Salesforce Integration Security

### 11.1 Selected authentication mechanism

Use OAuth 2.0 Client Credentials through a local Salesforce **External Client App**, configured to run as one dedicated non-human integration user. External Client Apps are selected for new work because Salesforce recommends them for new integrations and restricts creation of legacy Connected Apps as of Spring '26.

The flow fits the approved architecture: it is server-to-server, always runs as the same trusted integration identity, and requires the backend—not the browser—to protect client credentials. It produces no refresh token. Employer Administrator usernames, passwords, sessions, or Salesforce user licenses are not involved.

### 11.2 Integration identity and authorization

- Use one External Client App and one dedicated integration user for this portal integration only.
- Where the target org supports it, assign the Salesforce Integration user license and Minimum Access — API Only Integrations profile.
- Pre-authorize only the dedicated integration user for the External Client App.
- Request only the OAuth `api` scope.
- Grant API access and `Read` permission only for the approved Account, Contact, and Enrollment objects and the exact business, relationship, identifier, and correlation fields required by the adapter.
- Do not grant create, edit, delete, View All Data, Modify All Data, administrative Setup, broad application customization, or unrelated object/field access.
- Enforce field-level and object-level access in Salesforce; the application allow-list is an additional boundary, not a substitute.

### 11.3 Credentials and tokens

- Supply the client ID, client secret, login/token endpoint, and org configuration to the backend through protected runtime configuration. Never expose them to the frontend or commit them.
- Require certificate-validated TLS and an allow-listed Salesforce host. Redirects to an unexpected host are rejected.
- Cache the access token only in backend process memory until the earlier of its reported expiry minus 60 seconds or ten percent of its lifetime.
- Never persist the token in SQLite, disk caches, exception messages, traces, or logs.
- On one Salesforce `401`, invalidate the cached token, reacquire it once, and retry the failed read once. Do not perform general automatic source retries.
- If acquisition or reacquisition fails, translate the result into the approved Account 360 or child-section unavailable outcome based on the point of failure. Never expose OAuth or Salesforce errors.
- Rotate the client secret at least every 90 days and immediately after suspected exposure. Use External Client App staged credential rotation where the target org supports it, validate the new credential, then retire the old credential.

Portal logout invalidates only the portal session. It does not log out or revoke the shared Salesforce integration identity; service-token lifecycle is backend-owned and independent.

## 12. Secret Management

| Material | Classification | Handling |
|---|---|---|
| Sample plaintext passwords | Secret | Transient seed input only; never stored, logged, documented as working credentials, or committed. |
| Argon2id password encodings | Sensitive authentication data | Runtime SQLite only; excluded from Git and fixtures; restricted file access. |
| Portal session cookie | Secret bearer value | Browser cookie only; digest at rest; never logged or placed in JavaScript storage. |
| Salesforce client secret | Secret | Runtime environment/CI secret injection; never in frontend, repository, examples, or logs. |
| Salesforce access token | Secret | Process memory only; short-lived cache; redacted everywhere. |
| Salesforce client ID and endpoints | Restricted configuration | Backend configuration; not exposed unnecessarily even though not equivalent to the client secret. |
| Correlation UUID and source mappings | Sensitive internal configuration/data | Portal database or backend-only validated configuration; never returned or logged with business data. |
| Timeouts, cookie name, logging level | Ordinary configuration | May appear in typed configuration and placeholder examples when no secret is embedded. |

Local development uses an ignored `.env`-style file with owner-only permissions or protected shell inputs. The repository may include `.env.example` containing variable names and non-sensitive placeholders only. CI supplies secrets through its protected secret mechanism and must not echo environment values. Runtime databases, logs, token caches, and credential exports are ignored.

The opaque session design requires no application signing key. Cryptographic randomness comes from the operating system through maintained libraries. Salesforce credentials are rotated on the schedule above; sample user passwords are rotated before shared use and immediately after exposure. A secret exposure triggers revocation/rotation first, then history review and validation. Git history is treated as compromised even if a secret is later deleted from the current tree.

## 13. Logging and Audit Security

Security logs use structured, allow-listed fields. Each request receives an application-generated request ID carried through API, application, persistence, and adapter events.

Allowed events and fields include:

- authentication succeeded, failed, or throttled;
- session created, expired, revoked, or logged out;
- authorization/correlation cardinality succeeded or failed;
- logical Salesforce operation category, duration, result category, and bounded record count;
- Account 360 duration and available/empty/unavailable section states;
- validation, dependency, and unexpected error categories; and
- timestamp, severity, route template, HTTP status, and request ID.

Prohibited log content includes:

- passwords, password hashes, salts, dummy hashes, and seed inputs;
- cookies, session values, session digests, authorization headers, and Salesforce tokens;
- Salesforce client credentials or raw OAuth responses;
- raw usernames, email addresses, phone numbers, member names, business identifiers, or correlation UUIDs unless a separately approved diagnostic procedure requires a protected temporary record;
- full Contact, Enrollment, Account, request, or Salesforce response payloads;
- raw SOQL, database statements, source URLs containing values, or exception locals; and
- secrets or configuration dumps at startup.

Logging middleware redacts security-sensitive header and field names before serialization, escapes control characters to prevent log injection, and never logs request/response bodies. Unexpected stack traces may remain in restricted server logs only after sensitive locals and source payloads are excluded; they never enter API responses. Security validation uses canary values to prove redaction.

## 14. Browser Security

- Serve all non-local traffic over HTTPS and emit `Strict-Transport-Security: max-age=31536000`. Do not add `includeSubDomains` or preload until the deployment domain is approved.
- Apply a production Content Security Policy equivalent to `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'`. Development-only tooling exceptions must not reach a production build.
- Emit `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, `X-Frame-Options: DENY`, and `Permissions-Policy: camera=(), microphone=(), geolocation=()`.
- Apply `Cache-Control: no-store` to authenticated API data and authentication responses.
- Use React's default text escaping; prohibit raw HTML rendering and inline executable content.
- Store neither credentials nor sessions in local storage, session storage, IndexedDB, service-worker caches, URLs, or frontend state beyond the in-memory password field required to submit login.
- Clear the password field after the login result and prevent browser-controlled response content from rendering as HTML.
- Keep third-party scripts and external browser assets out of the MVP. Any later addition requires CSP and supply-chain review.

These controls reduce XSS, clickjacking, content-type confusion, referrer leakage, and browser cache exposure without adding a frontend security framework.

## 15. API Security

| Operation | Security behavior |
|---|---|
| `POST /api/v1/auth/login` | Unauthenticated; same-origin JSON only; size-limited; throttled; generic failure; successful response creates a rotated opaque session. |
| `POST /api/v1/auth/logout` | Session-aware but externally idempotent; same-origin JSON-capable POST with no body; revokes any supplied session and clears the cookie. |
| `GET /api/v1/employer-account-360` | Requires a current session and enabled user; accepts no body, identifier, filter, query, or paging input; employer context is server-derived. |

The API uses only the approved generic error taxonomy and never returns source errors, internal exceptions, credentials, session data, or unapproved identifiers. Framework-native validation errors are translated to `400 INVALID_REQUEST`. Account 360 is read-only; partial child-section unavailability remains a typed `200` only after required employer authorization succeeds.

No credentialed CORS configuration is present. Unexpected methods return the standard unsupported-method outcome without invoking business logic. Request bodies are capped before parsing, response content types are explicit, and all sensitive responses are non-cacheable.

## 16. Dependency and Supply-Chain Security

- Pin direct and transitive Python and Node.js dependencies in committed lock files.
- Prefer maintained, narrowly scoped libraries with active security support; avoid abandoned, typo-similar, or unnecessary packages.
- Review every newly introduced dependency for maintainer, license, transitive footprint, install scripts, and necessity.
- Run `pip-audit` for Python, the package manager's audit for Node.js, Bandit for Python security checks, and an open-source secret scanner such as Gitleaks in CI.
- Run type checks, linting, tests, OpenAPI validation, and production builds before merge.
- Fail CI for known high or critical vulnerabilities unless an owner records applicability, compensating controls, and an expiry for the exception.
- Apply security updates in small reviewed changes and rerun the full validation suite. Do not use unconstrained automated major-version upgrades.
- Generate artifacts from clean, reproducible dependency installs; do not commit package caches, virtual environments, build outputs, or downloaded credentials.

No commercial supply-chain platform is required for the MVP.

## 17. AI-Assisted Engineering Security

> AI accelerates engineering but does not approve security.

AI-assisted work must follow these controls:

- do not place credentials, session values, Salesforce tokens, client data, private source payloads, or production logs in prompts;
- use fictional, sanitized fixtures and placeholder configuration;
- review generated authentication, authorization, query, cookie, logging, and error-handling changes line by line;
- validate generated code with type checks, static analysis, dependency review, secret scanning, contract tests, negative tests, and real security test cases;
- reject generated dependencies unless their necessity and maintenance posture are reviewed;
- compare generated behavior to the approved architecture, API, and this security design;
- preserve sanitized prompt/decision records only when they contain no secrets or sensitive data; and
- require human approval for security exceptions, parameter changes, permission changes, and Salesforce integration settings.

AI output cannot waive a failed test, authorize broader Salesforce access, change a security parameter silently, or serve as validation evidence by itself.

## 18. Threat Model

| # | Threat | Impact | Primary controls | Residual risk | Validation |
|---:|---|---|---|---|---|
| 1 | Attacker guesses portal credentials. | Unauthorized employer access. | Argon2id, generic failures, dummy verification, username/IP rate limits, unique sample passwords. | Low-volume distributed guessing remains possible. | Wrong/unknown credential, throttling, timing-class, and successful-login tests. |
| 2 | Attacker steals a session cookie. | Session impersonation until revocation/expiry. | HTTPS, HttpOnly, Secure, Strict SameSite, no browser storage, 30-minute idle, eight-hour absolute lifetime, one session. | An active XSS or compromised endpoint can still act as the user. | Cookie-flag, expiry, revocation, XSS, and no-storage tests. |
| 3 | Attacker attempts session fixation. | Victim authenticates into attacker-known session. | Ignore/revoke pre-login cookie and generate a new 256-bit value after verification. | Endpoint compromise can bypass application controls. | Pre-set cookie login test proves identifier changes and old value fails. |
| 4 | Authenticated user attempts another employer. | Cross-account disclosure. | No employer input; session resolves current enabled user; exact UUID → Contact → Account cardinality; fail closed. | Incorrect Salesforce source relationships could mis-authorize. | Alternate-ID/query/body and relationship-integrity tests. |
| 5 | User tampers with request parameters. | Authorization bypass or query manipulation. | Closed schemas; reject Account 360 query/body; static adapter requests. | Framework configuration drift could ignore extras. | Negative contract tests for every unapproved input. |
| 6 | Attacker submits malicious login input. | SQL injection, resource exhaustion, or log injection. | Length/body caps, Unicode policy, parameterized SQL, no body logs, control-character escaping. | Pathological parser/library defects remain. | SQL-style, oversized, Unicode, and log-forging tests. |
| 7 | Salesforce service credentials leak. | Broad source access as the integration user. | External secret injection, no logs/source, secret scanning, 90-day/immediate rotation, token memory only. | Credential holder can act until revocation. | Canary redaction, repository scan, rotation rehearsal, config review. |
| 8 | Salesforce service account is over-privileged. | Excessive data access or source mutation. | Dedicated API-only identity, exact object/field read permission set, no mutation/admin rights. | Approved read access still spans all accessible matching records. | Permission matrix and denied field/object/mutation tests in the dev org. |
| 9 | Salesforce returns malformed or unexpected data. | Incorrect display, unsafe output, or misleading summary. | Closed source models, cardinality/type/status/paging validation, encoded output, fail/section degradation. | New source shapes may reduce availability. | Malformed source fixtures and representative org validation. |
| 10 | Sensitive values appear in logs. | Secondary disclosure and credential compromise. | Allow-listed events, body/header exclusions, redaction, no raw payloads, restricted stack traces. | Future logging changes can regress. | Canary secret, session, token, PII, and exception tests. |
| 11 | Cross-site request forgery. | Forced login/logout or session action. | Same origin, Strict cookie, exact Origin/Referer, Fetch Metadata, JSON-only login, bodyless logout, no CORS. | Compromised same-origin script bypasses CSRF controls. | Cross-site, same-site sibling, missing-origin, and valid-origin tests. |
| 12 | Cross-site scripting. | Data theft or actions through the victim browser. | React encoding, no raw HTML, CSP, no third-party scripts, validated source strings, HttpOnly cookie. | A dependency or future unsafe rendering can introduce XSS. | Stored/reflected payload fixtures, CSP, and DOM rendering tests. |
| 13 | Dependency vulnerability. | Code execution, data leak, or control bypass. | Lock files, minimal packages, audit/static scans, review, timely updates. | Zero-days and compromised maintainers remain. | CI audits, clean install, dependency review evidence. |
| 14 | AI-generated code introduces unsafe behavior. | Silent authorization, secret, or validation defect. | Human review, architecture conformance, tests, scanners, no AI approval authority. | Reviewers may over-trust plausible output. | Security checklist and adversarial tests for generated changes. |
| 15 | Secrets are accidentally committed to Git. | Persistent credential exposure through history. | Ignored secret/runtime files, placeholder examples, secret scanning, protected CI inputs, immediate rotation. | Developer bypass or scanner gaps. | Full-history secret scan and fixture/document review. |

## 19. Security Validation Strategy

### 19.1 Authentication tests

- valid enabled user receives `204` and a new session;
- wrong password, unknown user, disabled user, and throttled request all return the approved generic failure;
- unknown user invokes dummy Argon2id verification;
- username normalization is deterministic while password input is preserved exactly;
- Argon2id encodings contain the approved parameters and rehash-on-upgrade works; and
- username/IP windows enforce and expire the selected thresholds.

### 19.2 Session tests

- valid session permits Account 360 and never exposes its server record;
- idle-expired, absolute-expired, revoked, malformed, and unknown sessions return `401 SESSION_REQUIRED`;
- logout revokes the server record, clears the correctly scoped cookie, and remains idempotent;
- a pre-login attacker cookie is not retained after authentication;
- a second login revokes the first session; and
- cookie name, Path, HttpOnly, Secure, SameSite, no-Domain, and non-persistent behavior match this design.

### 19.3 Authorization tests

- query, body, header, or path attempts to select another Account are rejected or ignored only at the transport boundary without changing context;
- missing/malformed UUID, zero/multiple Contact matches, missing Account, ambiguous Account relationship, and disabled user all fail closed;
- the returned Account, Contacts, and Enrollment are all constrained to the resolved Account; and
- Contacts/Enrollment degradation begins only after the required Account context succeeds.

### 19.4 CSRF tests

- valid same-origin login and logout succeed;
- mismatched, `null`, absent, same-site sibling, and cross-site origins fail for POST operations;
- `Sec-Fetch-Site: cross-site` and untrusted `same-site` fail;
- non-JSON login requests fail;
- no credentialed CORS response is emitted; and
- GET Account 360 remains read-only and does not accept state-changing input.

### 19.5 Injection and validation tests

- malicious usernames, SQL injection-style input, control characters, oversized bodies, extra properties, wrong types, and unsupported content types are rejected safely;
- no client input can change a Salesforce field, object, clause, identifier, or paging value;
- malformed Salesforce payloads and incomplete paging fail safely; and
- XSS payloads from source fixtures render as text and do not execute.

### 19.6 Logging tests

Canary passwords, hashes, cookies, session digests, authorization headers, OAuth tokens, client secrets, correlation UUIDs, Contact data, Enrollment data, raw SQL/SOQL, and control characters are introduced in test paths. Captured logs must contain none of the prohibited values and must retain the correct request ID and safe event category.

### 19.7 Salesforce validation

- obtain a token through the selected External Client App and dedicated integration user;
- verify only the `api` scope and expected run-as identity;
- prove approved objects and fields are readable and unapproved fields/objects are inaccessible;
- prove create, edit, delete, administrative, View All Data, and Modify All Data operations are unavailable;
- validate token expiry, one-time reacquisition, invalid credential, timeout, and source-unavailable translation; and
- verify representative fictional Account, Contact, correlation, relationship, and Enrollment data without exposing source details in the Portal API.

### 19.8 Browser, dependency, and secret validation

- inspect production security headers, CSP, HTTPS/HSTS behavior, cookie flags, response caching, and framing prevention;
- run reflected/stored XSS payload tests and confirm no unsafe HTML path exists;
- run dependency, static-security, and secret scans from a clean checkout;
- review `.gitignore`, placeholder environment files, fixtures, documentation, Git history, build artifacts, and generated AI material for secrets; and
- run the approved OpenAPI lint and backend conformance suite after the limited contract amendment in Section 23.

Validation evidence must record tool versions, environment, date, result, exceptions, and reviewer. Real Salesforce checks run separately from the ordinary automated suite; ordinary tests remain fully executable with the mock adapter.

## 20. Security Decisions and Trade-offs

| Decision | Selected approach | Reason | Trade-off | Future evolution |
|---|---|---|---|---|
| Local identity | Fixed portal-managed SQLite users. | Matches the approved showcase and avoids external identity infrastructure. | No MFA, federation, recovery, or lifecycle administration. | Replace the identity adapter with enterprise SSO/OIDC when approved. |
| Password hashing | Argon2id at 64 MiB, three iterations, one lane. | Modern memory-hard protection with explicit, testable parameters. | Higher login CPU/memory cost than bcrypt or PBKDF2. | Benchmark and raise work factors; add managed pepper only with secret lifecycle support. |
| Session representation | Opaque server-side session, not JWT. | Immediate revocation, no browser business claims, simple authorization. | Requires stateful storage and shared storage for multiple instances. | Move the repository to a managed/distributed session store if scale requires. |
| Origin model | Same-origin frontend and API. | Simplest secure cookie boundary and no approved external client. | Constrains independent cross-origin hosting. | Approve explicit origins and credentialed CORS only with a revised threat model. |
| CSRF | Strict cookie plus exact-origin, Fetch Metadata, and JSON-only checks; no token. | Strong layered fit for the narrow same-origin contract. | Assumptions must remain true; older/non-browser clients without origin evidence are rejected. | Add a synchronizer/double-submit token if cross-origin or broader clients are approved. |
| Salesforce identity | Dedicated service account via External Client App client credentials. | Headless access, clear audit identity, no employer Salesforce license or delegated credential. | Compromise has the service account's shared read blast radius. | Consider certificate-based or managed workload identity when the platform and deployment justify it. |
| Source permissions | Exact object/field read permissions. | Enforces least privilege at the trusted system, not only in application code. | More setup and field-mapping discipline than broad development permissions. | Automate permission verification; never broaden only to ease a demo. |
| Session store | SQLite with one-session-per-user policy. | Transactional revocation without extra infrastructure at MVP scale. | Single-node concurrency and availability constraints. | Use production relational/distributed storage for multi-instance operation. |

## 21. Security Risks

| Risk | Current mitigation | Residual / trigger |
|---|---|---|
| Sample credentials are copied or reused. | Generate environment-specific passwords, never publish working credentials, rotate before shared use. | Any exposure requires immediate replacement of the sample user database/passwords. |
| SQLite is not production-scale. | Small fixed users, bounded sessions, repository abstraction, one instance. | Multiple instances or higher concurrency requires a different session/user store. |
| Salesforce service account blast radius. | Dedicated identity, exact read permissions, app allow-list, credential rotation. | Periodically review all accessible records/fields; production data sensitivity may require further segmentation. |
| Session theft. | Secure opaque cookie, short idle/absolute limits, one-session revocation, XSS controls. | Endpoint or same-origin compromise remains capable of acting during a live session. |
| Dependency or build compromise. | Minimal pinned dependencies, reviews, audits, static and secret scans. | Zero-days and maintainer compromise require monitoring and rapid update. |
| Source business data is sensitive. | Read-only least privilege, no caching/logging/persistence outside response handling, TLS. | Formal privacy, retention, and classification controls are deferred until real production data is approved. |
| Environment is misconfigured. | Typed startup validation; fail outside localhost when Secure/same-origin/secret requirements are absent. | Deployment topology and proxy trust require later validation. |
| Demo convenience weakens controls. | No hard-coded secrets, mock mode by default, CI security checks, security checklist. | Reviewers must reject bypass flags in shared or production-like modes. |
| Local rate limits can be bypassed across instances. | One-instance MVP and username/IP limits. | Multiple instances require shared counters and edge controls. |
| Target Salesforce org lacks the selected ECA entitlement/configuration. | Confirm in the development org before real-integration implementation. | Use an existing supported Connected App only as a recorded compatibility exception; do not weaken the identity or permission model. |

## 22. Future Production Enhancements

The following are possible production evolutions, not MVP commitments:

- enterprise SSO through OIDC/SAML, MFA, conditional access, and governed user lifecycle;
- managed secret storage, automated rotation, certificate-based client authentication, or managed workload identity;
- production relational/distributed session and rate-limit storage with high availability;
- edge rate limiting, WAF controls, denial-of-service protection, and API gateway policy where justified;
- centralized immutable audit, alerting, SIEM integration, and incident-response workflows;
- formal privacy classification, retention, consent, data-loss prevention, and regulated-data review;
- deployment-specific network restrictions, private connectivity, egress allow-lists, backup, and disaster recovery;
- stronger session risk signals and administrator-driven revocation;
- continuous dependency provenance, signed build artifacts, and software-bill-of-materials controls; and
- separately approved Enterprise AI security controls if a genuine application-level AI use case is later introduced.

None is required to implement or validate the current read-only showcase.

## 23. Open Questions and API Amendment

### 23.1 Environmental confirmations

No business or API-design question remains open. Two environment-dependent confirmations remain before real Salesforce validation:

1. Does the target Salesforce development org permit a local External Client App with OAuth client credentials and provide the appropriate dedicated integration-user entitlement?
2. Do the final source field mappings permit the required read-only permission set without any broad profile permission? This must be proven after the approved Data Model identifies exact source fields.

If the org cannot create the selected External Client App, an existing supported Connected App may be used only as a documented compatibility exception with the same client-credentials, dedicated-user, and least-privilege controls. It does not change the portal architecture or API.

### 23.2 Required contract hardening

Security review identifies one limited OpenAPI amendment before implementation:

- add `maxLength: 128` to `LoginRequest.username`; and
- add `maxLength: 256` to `LoginRequest.password`.

These bounds protect parsing and password-hashing resources and do not change the approved operation, request properties, success/failure behavior, or business scope. The 8 KiB whole-request limit is an implementation control and does not require another API property. No CSRF token/header, authentication response body, new error code, new endpoint, or cookie-name change is required.

This phase does not modify `contracts/openapi.yaml`; the contract owner must apply and revalidate the two schema constraints before implementation begins.

## 24. Phase Exit Criteria

Security Design is complete when reviewers have:

- approved Argon2id, its parameters, unique salts, seeding, verification, and rehash behavior;
- approved opaque SQLite-backed sessions, `portal_session` attributes, lifetime, idle timeout, rotation, concurrency, and revocation;
- approved the server-derived portal user → correlation UUID → Contact → Account authorization chain and every fail-closed condition;
- approved the same-origin CSRF strategy and confirmed that no CSRF token is required for the MVP;
- approved the External Client App client-credentials flow, dedicated integration identity, least-privilege permissions, token handling, and rotation;
- approved secret classification, local/CI handling, logging allow-lists, and redaction prohibitions;
- approved browser, API, input, injection, dependency, and supply-chain protections;
- reviewed all 15 threat scenarios and residual risks;
- approved the authentication, session, authorization, CSRF, injection, logging, Salesforce, browser, dependency, and secret validation plan;
- approved the AI-assisted engineering security controls and the principle that AI does not approve security;
- approved the two LoginRequest length constraints for controlled incorporation into the authoritative OpenAPI contract;
- confirmed that no new business capability, runtime AI, cloud-specific infrastructure, or Salesforce redesign has been introduced; and
- approved progression to Data Model.

Until these criteria are met, this artifact remains a draft and implementation must not treat it as approved.
