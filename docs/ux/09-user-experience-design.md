# User Experience Design — Employer Account Portal

**Showcase:** WorkflowFox Showcase \#2<br> **Phase:** 9 — User
Experience Design<br> **Status:** Approved<br> **Authoritative
baselines:** [Business
Discovery](../discovery/01-business-discovery.md), [Functional
Requirements](../requirements/02-functional-requirements.md), [Domain
Model](../domain-model/03-domain-model.md), [Solution
Architecture](../architecture/04-solution-architecture.md),
[Implementation Design](../design/05-implementation-design.md), [API
Specification](../api/06-api-specification.md),
[`contracts/openapi.yaml`](../../contracts/openapi.yaml), [Security
Design](../security/07-security-design.md), and [Data
Model](../data/08-data-model.md)<br> **Scope:** Login, read-only
Employer Account 360, and logout

## 1. Executive Summary

The Employer Account Portal provides one short, credible enterprise
journey: an Employer Administrator signs in, reviews the one employer
associated with the portal session, and signs out. The experience
contains no employer selector, application navigation, Salesforce
terminology, transactional actions, or runtime AI.

The primary Account 360 page answers four questions in order:

1.  Which employer am I viewing?
2.  What is the enrollment situation?
3.  Who are the employer contacts?
4.  What are the detailed enrollment records?

The page therefore presents Employer Overview, Enrollment Summary,
Employer Contacts, and Enrollment Records in that sequence. Contacts and
Enrollment preserve the API's explicit `available`, `empty`, and
`unavailable` meanings. Employer Overview is required; if it cannot be
established, no partial Account 360 is rendered.

Desktop is the primary showcase experience. Tables provide efficient
comparison on desktop and tablet. On narrow screens, records become
labeled stacked layouts rather than forcing users to interpret
compressed columns. The complete Enrollment collection is still
retrieved once through the approved API, but the frontend presents it in
local pages—50 records on desktop/tablet and 25 on narrow screens—to
avoid placing approximately 1,000 rows in the document at once. This is
presentation behavior only: it introduces no API pagination, search,
filtering, sorting, or new business operation.

The visual direction belongs to fictional **Workflow Insurance**. It is
restrained, accessible, information-focused, and intentionally distinct
from WorkflowFox showcase framing, Salesforce Lightning, and AI-demo
styling.

This phase creates no React code, CSS, images, high-fidelity mockups,
routes, or new API behavior.

## 2. UX Goals

| ID      | Goal                                  | Design response                                                                                                                                          |
|---------|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| UXG-001 | Clarity                               | Use one primary page, business terminology, explicit headings, and labeled values.                                                                       |
| UXG-002 | Employer-context confidence           | Lead with Employer Name, Employer/Group ID, Status, and Industry; never ask the user to select an employer.                                              |
| UXG-003 | Predictable information states        | Give available, empty, and unavailable data visibly and semantically different treatments.                                                               |
| UXG-004 | Enterprise credibility                | Favor restrained typography, cards, tables, whitespace, and precise status language over dashboard theatrics.                                            |
| UXG-005 | Accessibility                         | Design and validate toward WCAG 2.2 AA with semantic HTML, keyboard operation, visible focus, sufficient contrast, reflow, and announced status changes. |
| UXG-006 | Responsible bounded-list presentation | Present the already-retrieved Enrollment collection through local paging without changing the API or summary semantics.                                  |
| UXG-007 | Security alignment                    | Derive employer context from the session, clear protected content on session loss/logout, and expose no source-system or internal identifiers.           |
| UXG-008 | Simple implementation                 | Use only the screens, components, and state transitions required by login, Account 360, and logout.                                                      |
| UXG-009 | Showcase readability                  | Make the complete modernization outcome understandable in one screen and representative screenshots.                                                     |

## 3. Primary User

The sole primary user is an **Employer Administrator** viewing one
Employer Account.

For the reference experience:

- the fictional customer application is **Workflow Insurance Employer
  Portal**;
- the fictional employer is **Acme Manufacturing**;
- authentication uses portal-managed username/password credentials;
- employer context comes from the authenticated server-side session; and
- the user has view-only access to the approved Employer Overview,
  Contacts, Enrollment Summary, and Enrollment Records.

The user does not select or switch employers, provide any employer or
Salesforce identifier, authenticate with Salesforce, edit business data,
or navigate to additional portal capabilities.

The approved API returns no signed-in user profile. The application
header therefore does not fabricate or retain a personal display
identity from the submitted username. It shows Workflow Insurance,
Employer Portal, and Logout. The Employer Overview supplies the trusted
employer context after Account 360 loads.

## 4. User Journey

``` text
Open Employer Portal
        ↓
Login
        ├── invalid credentials ──> generic inline error; remain on Login
        └── success
              ↓
      Load Employer Account 360
              ├── session ended ──> Login with session-expired notice
              ├── Account unavailable ──> safe page-level error
              └── Account available
                    ↓
          Employer Account 360
              ├── Employer Overview
              ├── Enrollment Summary
              ├── Employer Contacts
              └── Enrollment Records
                    ↓
                  Logout
                    ├── success ──> Login
                    └── failure ──> protected data hidden; safe retry state
```

This is the complete journey. There is no dashboard home, sidebar,
breadcrumb, account picker, profile page, settings page, or secondary
workflow.

## 5. Information Architecture

### 5.1 Page hierarchy

``` text
Workflow Insurance Employer Portal
│
├── Login
│
└── Employer Account 360
    ├── Application Header
    ├── Employer Overview
    ├── Enrollment Summary
    ├── Employer Contacts
    └── Enrollment Records
```

### 5.2 Account 360 ordering

| Order | Section            | User question answered                      | Reason                                                                    |
|------:|--------------------|---------------------------------------------|---------------------------------------------------------------------------|
|     1 | Employer Overview  | Which employer am I viewing?                | Establishes the authorized business context before any child information. |
|     2 | Enrollment Summary | What is the enrollment situation?           | Provides the fastest meaningful overview of the primary child data.       |
|     3 | Employer Contacts  | Who are the employer contacts?              | Presents the smaller relationship set before the long record collection.  |
|     4 | Enrollment Records | What are the individual enrollment details? | Supports detailed review after the summary and context are understood.    |

Everything remains on one vertically flowing page. Section headings
support scanning and direct assistive-technology navigation without
introducing application navigation.

## 6. Login Experience

### 6.1 Purpose and layout

The Login screen presents a centered, modest-width authentication panel
against a light neutral background. A text identity for Workflow
Insurance appears above the Employer Portal title. No marketing content
competes with the task.

Required elements, in reading and tab order:

1.  Workflow Insurance identity;
2.  `Employer Portal` page heading;
3.  concise instruction: `Sign in to view your employer information.`;
4.  Username label and text input;
5.  Password label and password input;
6.  generic error region when needed; and
7.  primary `Sign In` button.

Inputs use visible persistent labels rather than placeholder-only
labeling. Browser autocomplete purposes are `username` and
`current-password`. Password visibility toggles, registration,
forgot-password links, social login, Salesforce login, MFA, and employer
selection are not included.

### 6.2 Validation and authentication failure

- Empty required fields receive local field-level messages before
  submission: `Enter your username.` and `Enter your password.`
- The error text is programmatically associated with the affected input,
  and the field has an invalid state.
- A server authentication failure uses the same message for unknown
  username, wrong password, disabled user, or throttling:
  `The username or password is incorrect.`
- The generic server message appears in an alert region above the form
  controls and receives programmatic focus or announcement without
  revealing which value failed.
- The username remains available for correction; the password is cleared
  after every completed attempt.
- The form does not display technical codes, attempt counts, lockout
  timing, or user-existence information.

### 6.3 Submitting state

After submission:

- button text becomes `Signing in…`;
- the button is disabled to prevent duplicate submission;
- inputs remain visually stable and the form is marked busy;
- a polite status announcement says `Signing in.`; and
- no fake success state or employer data appears before Account 360 is
  returned.

Successful login moves immediately to the coherent Account 360 loading
state; there is no intermediate success page.

## 7. Employer Account 360 Experience

The authenticated experience uses a restrained application shell:

- a compact header containing the Workflow Insurance text identity,
  `Employer Portal`, and `Logout`;
- one centered content column with a comfortable enterprise desktop
  width;
- one page heading, `Employer Account 360`;
- four ordered content sections; and
- no side navigation, tabs, breadcrumbs, promotional banner, or
  unrelated actions.

The page is read-only. Text must not look editable, and tables contain
no selection checkboxes, menus, row actions, links to nonexistent
details, export controls, or enrollment actions.

Employer Overview is the gate for the page. Contacts and Enrollment
render independently only after the employer context succeeds.
Section-level degradation does not remove valid sibling information.

The header does not show the submitted username as a trusted identity
because the approved API returns no user profile. It may show the
employer name only after the Account 360 response is trusted, but the
primary employer identification remains in Employer Overview to avoid
hiding context in chrome.

## 8. Employer Overview

Employer Overview appears directly under the page heading in one simple
card or bordered section.

| Label               | API property               | Presentation                                                              |
|---------------------|----------------------------|---------------------------------------------------------------------------|
| Employer Name       | `employer.employerName`    | Most prominent value within the section.                                  |
| Employer / Group ID | `employer.employerGroupId` | Labeled business identifier; never described as a record ID.              |
| Status              | `employer.status`          | Plain text or restrained text badge containing the source-approved value. |
| Industry            | `employer.industry`        | Plain text.                                                               |

Desktop/tablet uses a two-column definition layout below the Employer
Name. Narrow widths use one label/value pair per row. Status is never
communicated through color alone and receives no invented interpretation
because the API defines no Employer Status enum.

There is no edit control, Salesforce link, account selector, or hidden
source identifier.

## 9. Enrollment Summary

When `enrollmentSummary.state = available`, the section displays four
equal summary metrics:

1.  Total
2.  Active
3.  Pending
4.  Terminated

Each metric contains a visible label and integer value. Active, Pending,
and Terminated may use restrained supporting color or iconography, but
the text labels remain the authoritative meaning. Total is visually
primary without overwhelming the other metrics.

No chart is used. Four exact counts are faster to read, easier to
reconcile, and easier to make accessible than a decorative donut, gauge,
or trend visualization. No percentage, trend, comparison, or date range
is invented.

For confirmed empty Enrollment, the four metrics remain visible with
zero values. For unavailable Enrollment, the metric cards and all counts
are replaced by one summary-level unavailable panel. Zero values must
never appear in that state.

## 10. Employer Contacts

### 10.1 Available presentation

At desktop and tablet widths, Contacts use a compact semantic table with
caption `Employer Contacts` and columns:

- First Name
- Last Name
- Email
- Phone
- Role / Title

Column headers remain visible and use proper header semantics. Email,
Phone, and Role/Title display `Not provided` when their API value is
`null`; a blank cell is not used because absence should be
understandable to all users.

The complete bounded Contact collection is shown without pagination.
Approximately 50 rows remains manageable, and adding controls for the
smaller section would add more interaction than value.

### 10.2 Narrow presentation

At narrow widths, each Contact becomes a labeled record block with the
person's full name as the record heading and Email, Phone, and
Role/Title as explicit label/value pairs. The underlying information and
reading order do not change. This avoids horizontal compression and does
not create a different mobile capability.

There are no Contact detail links, edit actions, search, sort controls,
or selection checkboxes.

## 11. Enrollment Records

### 11.1 Available presentation

At desktop and tablet widths, Enrollment uses a semantic table with
caption `Enrollment Records` and columns:

- Enrollment ID
- Employee / Member
- Plan Name
- Status
- Effective Date

Enrollment Status always includes its text value. Effective Date is
presented in an unambiguous human-readable format such as `Jan 1, 2026`,
while retaining the API's date-only meaning for assistive technology and
testing.

### 11.2 Local presentation paging

The API returns the complete collection and the server-derived Summary.
The frontend then divides the in-memory array into presentation pages:

- 50 records per page on desktop and tablet;
- 25 records per page on narrow screens;
- `Previous` and `Next` buttons plus `Page X of Y`;
- a visible range statement such as
  `Showing 51–100 of 1,000 enrollment records`; and
- focus moves to the Enrollment Records heading after a page change,
  followed by a polite announcement of the new range.

All records were already retrieved and authorized. Page controls do not
send a page, filter, search, employer, or record identifier to the
backend. Changing viewport can recalculate local pages while preserving
the first currently visible record where practical.

The 50/25 page sizes are approved showcase presentation defaults, not
business-contract values. Validation may tune those client-side sizes if
accessibility or rendering evidence requires it, provided the change
does not alter the API, Summary semantics, authorization boundary, or
introduce new business behavior.

No search, sorting, filtering, page-size selector, infinite scroll,
virtualization, or URL query state is added. Local paging is chosen
because it reduces rendered rows and provides predictable
keyboard/screen-reader position without changing the contract.

### 11.3 Narrow presentation

Each Enrollment record becomes a labeled block with Employee / Member as
the record heading and the remaining four fields as label/value pairs.
Local paging limits the stacked presentation to 25 records at a time. No
field is hidden merely because the viewport is narrow.

## 12. Loading States

| Operation                     | Visual behavior                                                                                                                               | Accessibility behavior                                                                          | Data protection                                                                          |
|-------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| Authentication                | Stable Login form; `Signing in…` button state; minimal progress indicator if used.                                                            | Form `aria-busy`; polite `Signing in` status; focus remains predictable.                        | Password cleared when the attempt completes.                                             |
| Initial Account 360 retrieval | Application header plus one coherent page-level `Loading employer information…` state. Do not show section values or populated skeleton text. | Main region marked busy; one polite status announcement; page title identifies Employer Portal. | No stale, sample, or prior-employer business values remain visible.                      |
| Logout                        | Immediately replace protected content with `Signing out…`; disable repeated action.                                                           | Polite status message; focus remains in the neutral status region.                              | Clear Account 360 data from rendered and application state before awaiting the response. |

Animation is limited to a subtle progress indicator and respects
reduced-motion preferences. The application does not rotate through
source-operation messages or imply progress it cannot know.

## 13. Empty States

Empty means the trusted response confirmed zero records. Empty is not an
error and does not use warning styling.

| API state                  | UX treatment                                                                                                                                                                       |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `contacts.state = empty`   | Employer Contacts heading plus neutral message: `This employer has no contacts to display.` No table header is shown.                                                              |
| `enrollment.state = empty` | Enrollment Summary remains visible with four zero counts. Enrollment Records shows: `This employer has no enrollment records to display.` No table header or local pager is shown. |

Empty messages are normal text within labeled sections. Screen readers
encounter the section heading followed by the message. No retry control
is shown because the result is valid and complete.

## 14. Unavailable States

Unavailable means complete trusted section data could not be obtained.
It uses a visible status panel with an icon plus text; color is
secondary.

| API state                        | UX treatment                                                                                                                                                                 | Preserved sibling content                          |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| `contacts.state = unavailable`   | Employer Contacts heading and `Contact information is temporarily unavailable.` No records or table are shown.                                                               | Employer Overview and available Enrollment remain. |
| `enrollment.state = unavailable` | Enrollment Summary shows one unavailable panel with no metrics. Enrollment Records shows `Enrollment information is temporarily unavailable.` No records or pager are shown. | Employer Overview and available Contacts remain.   |
| Both child sections unavailable  | Render the independent Contacts and Enrollment unavailable treatments in their normal page positions.                                                                        | Employer Overview remains fully visible.           |

The frontend may display the contract's safe section `message`; it uses
the approved fallback above if the safe message is absent because of an
unexpected client condition. It never appends source, HTTP, exception,
or troubleshooting detail.

Section-unavailable panels are announced as status information when
inserted. They do not steal focus, behave as modal dialogs, or replace
the complete page.

## 15. Error Experience

### 15.1 Error treatments

| Condition                           | User-facing treatment                                                                           | Actions                                                                          |
|-------------------------------------|-------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| Invalid credentials                 | `The username or password is incorrect.` within Login.                                          | Correct credentials and submit again.                                            |
| Invalid login request               | `Check the information entered and try again.` with field messages where applicable.            | Correct and resubmit.                                                            |
| Session required/expired            | Return to Login with `Your session has expired. Sign in again.`                                 | Sign In.                                                                         |
| Authorized context unavailable      | Page-level error: `We can't access your employer information.`                                  | Logout; show request reference when supplied.                                    |
| Account 360 temporarily unavailable | Page-level error: `Employer information is temporarily unavailable. Try again.`                 | `Try Again` repeats the same approved GET; Logout remains available.             |
| Unexpected application failure      | Page-level error: `Something went wrong. Try again.`                                            | `Try Again` when safe; Logout.                                                   |
| Network response unavailable        | Page-level error: `We couldn't load employer information. Check your connection and try again.` | `Try Again`; Logout if a session may exist.                                      |
| Logout failure                      | Protected content stays hidden. Show `We couldn't complete sign out. Try again.`                | `Try Again`. Do not claim that closing the browser completes server-side logout. |

### 15.2 Page-level error rules

- Do not render Employer Overview, Contacts, Enrollment, or Summary when
  required Account context fails.
- Keep the Workflow Insurance application header and Logout available
  when a session may still exist.
- Display `Reference: {requestId}` only when the API supplies a request
  ID. Explain: `Use this reference if you contact support.` Do not
  invent a support channel.
- Place focus on the page-error heading after the state transition and
  announce the error once.
- Do not show HTTP status codes, Salesforce, SOQL, object/field API
  names, stack traces, exception classes, credentials, internal IDs,
  retry counts, or source-system advice.

`Try Again` is not a new business capability; it repeats the existing
read or logout operation without changing inputs or authorization
context.

## 16. Session Expiration

When Employer Account 360 returns `SESSION_REQUIRED`:

1.  immediately remove Account 360 data from rendered and in-memory
    frontend state;
2.  return to Login;
3.  display a one-time notice:
    `Your session has expired. Sign in again.`;
4.  place focus on the notice or Login heading according to the
    implementation's tested focus pattern; and
5.  do not preserve a requested employer, source identifier, or
    post-login destination.

The message describes the portal session, not Salesforce authentication.
The same safe experience applies to an expired, revoked, replaced,
malformed, or otherwise invalid portal session because the API
intentionally does not distinguish those cases.

Refreshing or directly opening the protected experience without a valid
session returns to Login without showing protected content. A first
visit with no prior session does not show an expiration warning.

## 17. Responsive Design

### 17.1 Target behavior

| Viewport                                 | Primary layout                                                                                                                                                |
|------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Desktop, approximately 1280 px and above | Centered content; four summary metrics in one row; two-column overview details; semantic tables; 50 Enrollment rows per local page.                           |
| Tablet, approximately 768–1279 px        | Reduced margins; summary remains four columns where readable or becomes two-by-two; tables remain semantic; 50 Enrollment rows per local page.                |
| Narrow/mobile, approximately 320–767 px  | Single-column layout; summary two-by-two or one column at extreme zoom; Contacts and Enrollment use labeled record blocks; 25 Enrollment rows per local page. |

The design supports reflow at 320 CSS pixels and text zoom without
losing data or actions. No separate mobile application or mobile-only
feature exists.

### 17.2 Responsive rules

- Header identity and Logout remain visible without a menu.
- Summary labels and values never truncate.
- Employer labels remain paired with values.
- No business field is removed at narrow widths.
- Table-to-record-layout change preserves order, labels, status text,
  and empty/unavailable semantics.
- Local pager controls wrap as a group and maintain large, separated
  targets.
- Sticky headers or controls must not obscure keyboard focus.

## 18. Accessibility

The implementation is designed and validated toward [WCAG 2.2 Level
AA](https://www.w3.org/TR/WCAG22/). Accessibility is an acceptance
concern, not a visual annotation.

### 18.1 Structure and navigation

- Use semantic `header` and `main` landmarks and one page-level heading.
- Use a logical heading hierarchy for Overview, Summary, Contacts, and
  Enrollment.
- Provide a keyboard-reachable skip link from the application header to
  main content.
- Keep DOM and visual order aligned; no positive tab indices or keyboard
  traps.
- On state/page changes, move focus only when needed to establish new
  context; status messages otherwise use live regions without stealing
  focus.

### 18.2 Forms and errors

- Associate visible labels, instructions, errors, and required state
  programmatically with each input.
- Use native input and button semantics and appropriate autocomplete
  purposes.
- Do not rely on placeholder text or color for labels/errors.
- Announce authentication and validation errors once, and preserve a
  predictable correction order.

### 18.3 Focus, controls, and motion

- Every interactive element has a persistent visible focus indicator
  with at least 3:1 contrast; a two-pixel perimeter is the preferred
  design target.
- Focus is not hidden by sticky content, aligning with WCAG 2.2's Focus
  Not Obscured requirement.
- Primary buttons use comfortably sized targets (approximately 44 CSS
  pixels high); all controls meet or exceed the WCAG 2.2 AA 24-by-24
  CSS-pixel target minimum or its spacing exception.
- No function requires pointer hover, drag, or timed interaction.
- Respect reduced-motion preferences and avoid nonessential animation.

### 18.4 Color and content

- Normal text meets at least 4.5:1 contrast; large text and meaningful
  graphical/UI boundaries meet the applicable 3:1 requirements.
- Available, empty, unavailable, and status values use text, not color
  alone.
- Language is concise and avoids unexplained abbreviations or technical
  terminology.
- At 200% text resize and narrow reflow, no content or operation is
  lost.

### 18.5 Tables, records, and status changes

- Desktop/tablet tables use captions, column headers, and appropriate
  header scope; layout tables are prohibited.
- Narrow record blocks retain explicit programmatic labels for every
  value.
- Local paging controls have descriptive names, current-page text,
  disabled states, and announced result ranges.
- Loading, empty, unavailable, session, and result-count updates are
  exposed as screen-reader status messages where they appear
  dynamically.
- `Not provided` is announced as text rather than represented by an
  unlabeled dash or empty cell.

Automated checks supplement but do not replace keyboard and
screen-reader testing.

## 19. Visual Direction

### 19.1 Brand and tone

The application belongs to **Workflow Insurance**. Use a text-only
identity in this phase; no logo asset is created. WorkflowFox branding
is excluded from the application shell and belongs in repository,
website, video, and showcase framing outside the fictional customer
experience.

The visual character is:

- clean, restrained, professional, and information-led;
- a light neutral page background with white or subtly bordered content
  surfaces;
- a calm navy primary color with a restrained blue/teal accent;
- dark neutral text with accessible muted secondary text;
- moderate corner radius, light borders, and minimal shadow;
- strong typographic hierarchy using a system font stack; and
- consistent spacing rather than decorative density.

Status colors may support meaning but always accompany visible text.
Final color values require measured contrast validation.

### 19.2 Explicit visual exclusions

Do not use AI gradients, glow effects, chat bubbles, decorative charts,
animated counters, excessive dashboard tiles, hero marketing copy,
consumer-app styling, Salesforce Lightning imitation, WorkflowFox
marketing marks, external web fonts, or third-party scripts/assets.

## 20. Low-Fidelity Wireframes

### 20.1 Login

``` text
+--------------------------------------------------------------+
|                                                              |
|                 WORKFLOW INSURANCE                           |
|                                                              |
|                 Employer Portal                              |
|        Sign in to view your employer information.            |
|                                                              |
|        Username                                              |
|        [__________________________________________]            |
|                                                              |
|        Password                                              |
|        [__________________________________________]            |
|                                                              |
|        [ Error: The username or password is incorrect. ]      |
|                                                              |
|        [ Sign In                                  ]           |
|                                                              |
+--------------------------------------------------------------+
```

The error region is absent before an error. During submission, the
button label becomes `Signing in…`.

### 20.2 Complete Employer Account 360

``` text
+--------------------------------------------------------------------------+
| WORKFLOW INSURANCE   Employer Portal                         [ Logout ]   |
+--------------------------------------------------------------------------+
| Employer Account 360                                                     |
|                                                                          |
| EMPLOYER OVERVIEW                                                        |
| +----------------------------------------------------------------------+ |
| | Acme Manufacturing                                                   | |
| | Employer / Group ID  ACM-GRP-1001    Status   Active                 | |
| | Industry             Manufacturing                                   | |
| +----------------------------------------------------------------------+ |
|                                                                          |
| ENROLLMENT SUMMARY                                                       |
| +--------------+ +--------------+ +--------------+ +------------------+ |
| | Total        | | Active       | | Pending      | | Terminated       | |
| | 8            | | 5            | | 2            | | 1                | |
| +--------------+ +--------------+ +--------------+ +------------------+ |
|                                                                          |
| EMPLOYER CONTACTS                                                        |
| +------------+------------+----------------------+-------------+--------+ |
| | First Name | Last Name  | Email                | Phone       | Title  | |
| | Dana       | Cole       | dana...@example.com  | 555-...     | ...    | |
| | Luis       | Ortega     | luis...@example.com  | Not provided| ...    | |
| +------------+------------+----------------------+-------------+--------+ |
|                                                                          |
| ENROLLMENT RECORDS                         Showing 1–8 of 8 records       |
| +------------+--------------------+---------------+------------+---------+ |
| | Enroll. ID | Employee / Member  | Plan Name     | Status     | Date    | |
| | ENR-00001  | Jordan Lee         | Essential PPO | Active     | Jan 1   | |
| | ENR-00002  | Priya Shah         | Essential PPO | Active     | Jan 1   | |
| +------------+--------------------+---------------+------------+---------+ |
|                         [ Previous ] Page 1 of 1 [ Next ]                 |
+--------------------------------------------------------------------------+
```

Disabled local paging controls may be omitted when the collection fits
on one page.

### 20.3 Contacts unavailable

``` text
| EMPLOYER CONTACTS                                                        |
| +----------------------------------------------------------------------+ |
| | [Status icon] Contact information is temporarily unavailable.        | |
| +----------------------------------------------------------------------+ |
|                                                                          |
| ENROLLMENT RECORDS                                                       |
| [Available Enrollment table remains usable]                              |
```

### 20.4 Enrollment unavailable

``` text
| ENROLLMENT SUMMARY                                                       |
| +----------------------------------------------------------------------+ |
| | [Status icon] Enrollment summary is temporarily unavailable.         | |
| +----------------------------------------------------------------------+ |
|                                                                          |
| EMPLOYER CONTACTS                                                        |
| [Available Contacts table remains usable]                                |
|                                                                          |
| ENROLLMENT RECORDS                                                       |
| +----------------------------------------------------------------------+ |
| | [Status icon] Enrollment information is temporarily unavailable.     | |
| +----------------------------------------------------------------------+ |
```

No zero summary metrics appear.

### 20.5 Page-level Account 360 failure

``` text
+--------------------------------------------------------------------------+
| WORKFLOW INSURANCE   Employer Portal                         [ Logout ]   |
+--------------------------------------------------------------------------+
|                                                                          |
| Employer information is temporarily unavailable.                         |
| Try again.                                                               |
|                                                                          |
| Reference: req-c84620da                                                  |
|                                                                          |
| [ Try Again ]                                                            |
|                                                                          |
+--------------------------------------------------------------------------+
```

No Employer Overview, Contacts, Enrollment, or Summary content appears
behind or below the page error.

## 21. Component Inventory

The minimum reusable frontend components are:

| Component              | Responsibility                                                                                           | Explicitly not responsible for                                       |
|------------------------|----------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| `ApplicationHeader`    | Workflow Insurance identity, Employer Portal title, Logout state/action.                                 | Navigation, employer selection, user-profile retrieval.              |
| `LoginForm`            | Labeled credential fields, local validation, generic authentication error, submitting state.             | Registration, recovery, MFA, Salesforce login.                       |
| `Account360Page`       | Order required sections and choose page-level loading/error/success state.                               | Source queries, employer selection, business calculations.           |
| `EmployerOverview`     | Present four approved Employer values.                                                                   | Editing, source identifiers, status interpretation.                  |
| `EnrollmentSummary`    | Render four metrics or one unavailable state.                                                            | Calculating counts, charting, showing zeros for unavailable data.    |
| `SummaryMetric`        | Present one accessible label/value pair.                                                                 | Trend or percentage logic.                                           |
| `ContactCollection`    | Render semantic table or narrow labeled records for `available`; delegate empty/unavailable states.      | Search, sort, edit, detail navigation.                               |
| `EnrollmentCollection` | Render semantic table or narrow records and local presentation paging.                                   | Backend pagination, search, filtering, sorting, summary calculation. |
| `ClientPager`          | Page the already-loaded Enrollment array and announce current range.                                     | API requests or business filtering.                                  |
| `EmptyState`           | Render neutral confirmed-empty language within a labeled section.                                        | Retry or error semantics.                                            |
| `SectionUnavailable`   | Render safe section-level unavailable status.                                                            | Technical details or page-level failure.                             |
| `PageError`            | Render safe Account 360/logout failure, optional request reference, and permitted retry/logout controls. | Partial employer data.                                               |
| `LoadingState`         | Render coherent authentication, Account 360, or logout progress and live status.                         | Fake business data or source-operation progress.                     |
| `SessionNotice`        | Communicate session expiration on Login once.                                                            | Salesforce-authentication messaging.                                 |

This inventory is not a generic design system. Shared low-level
button/input/table primitives may exist during implementation, but no
standalone component library is a deliverable.

## 22. Frontend State Model

### 22.1 Authentication and page state

| API/application condition          | Frontend state              | UX result                                                 |
|------------------------------------|-----------------------------|-----------------------------------------------------------|
| First visit / no session           | `unauthenticated`           | Login without expiration notice.                          |
| Login request in progress          | `authenticating`            | Login submitting state; no Account data.                  |
| `AUTHENTICATION_FAILED`            | `authenticationFailed`      | Generic Login error; clear password.                      |
| Login `204`, Account 360 pending   | `loadingAccount360`         | Coherent page-level loading state.                        |
| Account 360 `200`                  | `account360Ready`           | Render Employer Overview and each typed child state.      |
| `SESSION_REQUIRED`                 | `sessionExpired`            | Clear protected state; Login with expiration notice.      |
| `ACCESS_UNAVAILABLE`               | `employerAccessUnavailable` | PageError; no Account 360; request reference if supplied. |
| `ACCOUNT_360_UNAVAILABLE`          | `account360Unavailable`     | Retryable PageError; no partial Account 360.              |
| `INTERNAL_ERROR` / network failure | `unexpectedFailure`         | Safe retryable PageError; no technical detail.            |
| Logout pending                     | `loggingOut`                | Protected content removed; signing-out status.            |
| Logout `204`                       | `unauthenticated`           | Login without session-expired notice.                     |
| Logout failure                     | `logoutFailure`             | Protected content remains hidden; retry logout.           |

### 22.2 Child-section state mapping

| Approved API state                                                       | Required UX state                                                                           |
|--------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `contacts.state = available`                                             | Render Contact table or narrow labeled records from `contacts.items`.                       |
| `contacts.state = empty`                                                 | Render neutral Contacts empty state; no table.                                              |
| `contacts.state = unavailable`                                           | Render Contacts unavailable panel using safe message; no records.                           |
| `enrollment.state = available` and `enrollmentSummary.state = available` | Render four Summary metrics plus locally paged Enrollment records.                          |
| `enrollment.state = empty` and available zero Summary                    | Render four zero metrics plus neutral Enrollment empty state; no pager.                     |
| `enrollment.state = unavailable` and Summary unavailable                 | Render Summary unavailable with no counts and Enrollment unavailable with no records/pager. |
| Contacts and Enrollment unavailable                                      | Keep Employer Overview; render both independent unavailable states.                         |
| Any impossible combination                                               | Treat as an unexpected client/contract failure; do not guess or render misleading data.     |

The property name is `state`, matching the approved contract. The
frontend never infers section state from `null`, missing properties, or
item length alone.

### 22.3 Local Enrollment presentation state

Local state contains only the current presentation-page index and
responsive page size. It does not contain employer identity, source IDs,
filtering criteria, or a server cursor. New Account 360 data resets the
local page to the first page. A section becoming empty/unavailable
removes pager state.

## 23. Content and Terminology

### 23.1 Preferred application language

Use:

- Workflow Insurance
- Employer Portal
- Employer Account 360
- Employer Overview
- Employer / Group ID
- Employer Contacts
- Enrollment Summary
- Enrollment Records
- Employee / Member
- Sign In
- Logout
- temporarily unavailable
- no records to display
- Reference

`Logout` is selected consistently because the approved API operation and
required header element use that term. Do not alternate between
`Logout`, `Log out`, and `Sign Out` within the same experience.

### 23.2 Prohibited application language

Do not expose or describe:

- Salesforce or a Salesforce Account/Contact object;
- `Enrollment__c` or any source field API name;
- SOQL, adapter, service account, OAuth, API, database, or HTTP status;
- Contact correlation UUID, portal-user UUID, source record ID, or
  session identifier;
- stack trace, exception class, timeout, rate limit, or credential
  detail; or
- WorkflowFox, AI-assisted engineering, or showcase messaging inside the
  fictional customer application.

WorkflowFox explains the engineering story around the application;
Workflow Insurance owns the application experience.

## 24. Showcase Data Fixtures

All fixtures are fictional and use reserved example domains/numbers.

### 24.1 Demo fixture

**Employer**

| Field               | Value              |
|---------------------|--------------------|
| Employer Name       | Acme Manufacturing |
| Employer / Group ID | ACM-GRP-1001       |
| Status              | Active             |
| Industry            | Manufacturing      |

**Contacts**

| First Name | Last Name | Email                     | Phone           | Role / Title            |
|------------|-----------|---------------------------|-----------------|-------------------------|
| Dana       | Cole      | <dana.cole@example.com>   | +1-202-555-0101 | Benefits Administrator  |
| Luis       | Ortega    | <luis.ortega@example.com> | Not provided    | Human Resources Manager |
| Priya      | Nair      | <priya.nair@example.com>  | +1-202-555-0103 | Payroll Coordinator     |

**Enrollment**

| Enrollment ID | Employee / Member | Plan Name     | Status     | Effective Date |
|---------------|-------------------|---------------|------------|----------------|
| ENR-00001     | Jordan Lee        | Essential PPO | Active     | 2026-01-01     |
| ENR-00002     | Priya Shah        | Essential PPO | Active     | 2026-01-01     |
| ENR-00003     | Marcus Green      | Choice HMO    | Pending    | 2026-09-01     |
| ENR-00004     | Elena Ruiz        | Essential PPO | Active     | 2026-02-01     |
| ENR-00005     | Owen Brooks       | Choice HMO    | Terminated | 2025-01-01     |
| ENR-00006     | Amina Yusuf       | Essential PPO | Active     | 2026-03-01     |
| ENR-00007     | Daniel Kim        | Choice HMO    | Pending    | 2026-09-01     |
| ENR-00008     | Sofia Martinez    | Essential PPO | Active     | 2026-04-01     |

Summary: Total 8, Active 5, Pending 2, Terminated 1.

This small fixture is intended for ordinary screenshots, walkthroughs,
and complete-state demonstrations. Separate variants represent Contacts
empty, Contacts unavailable, Enrollment empty, Enrollment unavailable,
both children unavailable, Account 360 unavailable, and expired session.

### 24.2 Volume-validation fixture

The volume fixture is synthetic and intended for engineering validation
rather than screenshots:

- one Employer Account;
- approximately 50 Contacts; and
- approximately 1,000 Enrollment records distributed across all three
  approved statuses.

It validates payload handling, initial loading, local paging, range
announcements, responsive rendering, keyboard traversal, and Summary
reconciliation. It does not imply that the showcase is validated for
enterprise-scale volumes beyond the approved bounds.

## 25. UX Validation Strategy

### 25.1 Functional UX

- Login accepts the approved fields and exposes no unapproved path.
- Successful authentication progresses through loading to Account 360.
- Employer Overview displays exactly four approved values.
- Enrollment Summary reconciles to available/empty Enrollment data.
- Logout clears protected content and returns to Login.
- Expired/invalid session clears protected content and returns to Login
  with the correct notice.

### 25.2 State UX

Validate every contract combination:

- Contacts available, empty, and unavailable;
- Enrollment available with Summary available;
- Enrollment empty with zero Summary;
- Enrollment unavailable with Summary unavailable and no counts;
- both child sections unavailable while Employer Overview remains;
- Account context unavailable with no partial Account 360; and
- impossible client state fails safely rather than being inferred.

Tests assert exact state-to-component mapping, absence of stale/partial
records, and safe messages.

### 25.3 Accessibility

- Complete all functionality keyboard-only in logical order with no
  trap.
- Confirm visible, unobscured focus and sufficient focus contrast.
- Inspect page landmarks, headings, form names/descriptions/errors,
  table captions/headers, record labels, button states, and live
  announcements with accessibility tooling.
- Test Login errors, loading, section state changes, local page changes,
  PageError, and session expiration with at least one desktop screen
  reader/browser combination.
- Measure text, non-text, focus, and status contrast in every state.
- Test 200% text resize, browser zoom, reduced motion, and narrow
  reflow.
- Confirm status and unavailable meaning remains clear without color.

Automated accessibility scanning is required but is not sufficient
evidence by itself.

### 25.4 Responsive behavior

Validate at representative 1440 px desktop, 768 px tablet, 360 px
mobile, and 320 px reflow widths, including long names and maximum
approved field lengths. Confirm that no field, action, focus indicator,
unavailable message, pager status, or error reference is clipped or
obscured.

### 25.5 Contract alignment and source isolation

- Map every displayed field to `contracts/openapi.yaml`.
- Generate/test frontend types from the approved contract and reject
  unrecognized section variants.
- Confirm the frontend sends no employer, Contact, Account, correlation,
  query, filter, search, sort, or paging input.
- Scan UI text, fixtures, state names intended for presentation, and
  rendered output for Salesforce identifiers and terminology.
- Confirm page-level errors display only approved messages and optional
  request ID.

### 25.6 Bounded-list validation

With approximately 1,000 Enrollment records:

- only the selected local page is rendered;
- ranges and page totals are mathematically correct;
- first/last and disabled Previous/Next behavior is correct;
- changing pages preserves keyboard and screen-reader context;
- changing responsive page size does not duplicate or omit records; and
- the displayed server-derived Summary continues to represent the full
  collection, not the current local page.

## 26. Decisions and Trade-offs

| Decision                                                             | Reason                                                                                                                          | Trade-off                                                                                | Future evolution                                                                                 |
|----------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| One Account 360 page, not multiple pages                             | The approved journey is one coherent business view with four closely related sections.                                          | A long Enrollment collection creates vertical depth.                                     | Split views only if later approved workflows or volumes justify navigation and contract changes. |
| Semantic tables on larger screens; labeled records on narrow screens | Tables support comparison; labeled records preserve all fields without cramped columns.                                         | Two responsive presentations require shared mapping and duplicate accessibility testing. | Reconsider a dedicated accessible data-grid only for approved richer interaction.                |
| Local Enrollment paging after one complete API response              | Limits rendered rows and makes position predictable without changing Summary or the API.                                        | The full payload is still transferred and paging state is frontend-only.                 | Add server pagination only with an approved API/Summary design.                                  |
| No client-side search, sort, or filtering                            | None is required; avoiding controls preserves source order and reduces implied capabilities.                                    | Locating one record in 1,000 can require paging.                                         | Add local or server discovery only after a validated user need and contract decision.            |
| Section-level unavailable states after Account success               | Preserves useful sibling information and matches the approved partial-failure contract.                                         | Users must understand mixed availability on one page.                                    | Add richer recovery guidance only with approved support requirements.                            |
| Page-level failure when Account context fails                        | Prevents an unauthorized or contextless partial page.                                                                           | No child information remains visible even if independently retrievable.                  | This fail-closed boundary should remain unless authorization architecture changes.               |
| Four summary metrics, no chart                                       | Exact counts are accessible, compact, and sufficient for the approved question.                                                 | No visual trend or proportion analysis.                                                  | Add visualization only if new business questions justify it.                                     |
| Responsive record layouts instead of horizontal scrolling            | Preserves labels/readability on narrow screens and supports touch/zoom.                                                         | Long mobile pages require local 25-record paging.                                        | Reassess with validated device usage and data density.                                           |
| Workflow Insurance branding inside the portal; WorkflowFox outside   | Maintains a credible fictional customer application and keeps technology/consulting messaging out of the user task.             | Showcase screenshots need external framing to identify WorkflowFox.                      | Add a clearly separate showcase frame in publishing assets, not application chrome.              |
| No signed-in personal identity in the header                         | The approved API returns no user profile; retaining submitted username would not be a reliable authenticated identity contract. | The header cannot personalize the session.                                               | Add identity display only through a later approved contract requirement.                         |

## 27. Future Evolution

The experience can evolve after new discovery and approval to support
enterprise identity, multiple employers, additional business
capabilities, server-side pagination, richer support guidance, or
application-level Enterprise AI. The current design preserves those
possibilities through clear components and business-oriented state
mapping.

Future possibilities do not authorize profile pages, employer switching,
search, filters, charts, enrollment actions, notifications, case
management, or AI in this MVP. Each requires requirements, architecture,
API, security, data, and UX review as applicable.

## 28. Resolved UX Decisions and Environment Validation

### 28.1 Resolved UX decisions

Screen count, hierarchy, component inventory, state treatments,
user-facing language, local Enrollment paging, responsive
transformations, accessibility intent, branding boundary, and demo
fixture are resolved in this artifact.

### 28.2 Environment validation items

These items require implementation or visual-validation evidence and do
not block approval of the UX design:

1.  Verify the final Workflow Insurance navy/accent/neutral palette
    meets WCAG 2.2 AA contrast across default, hover, focus, disabled,
    empty, unavailable, and error states.
2.  Verify the system font stack and actual longest approved data values
    remain readable at desktop, tablet, 360 px mobile, 320 px reflow,
    and 200% text resize.
3.  Confirm local 50/25-row presentation paging meets performance and
    screen-reader expectations with the approximately 1,000-record
    validation fixture.
4.  Confirm the selected screen-reader/browser test combination and
    document results during Validation.
5.  Confirm production security headers and Content Security Policy
    allow only the self-hosted application assets assumed by this visual
    direction.

### 28.3 Remaining design questions

No unresolved business or UX design question remains for the approved
MVP. A material accessibility, performance, or contract problem found
during implementation requires a controlled UX/API/design review rather
than an unrecorded workaround.

## 29. Phase Exit Criteria

User Experience Design is complete when reviewers have:

- approved Login and Employer Account 360 as the only screens;
- approved the single Account 360 page and section order;
- approved Employer Overview, Summary, Contacts, and Enrollment field
  presentations;
- approved local Enrollment presentation paging as frontend-only
  behavior with no API change;
- approved available, empty, unavailable, session-expired, and
  page-level failure treatments;
- confirmed that unavailable Enrollment never displays zero Summary
  counts;
- approved loading, logout, retry, and protected-content-clearing
  behavior;
- approved responsive table/record behavior for desktop, tablet, and
  reasonable mobile widths;
- approved the WCAG 2.2 AA design and validation criteria;
- approved the Workflow Insurance visual direction and separation from
  WorkflowFox showcase branding;
- approved all low-fidelity wireframes, component responsibilities,
  frontend state mappings, terminology, and fictional fixtures;
- confirmed every displayed value maps to the approved OpenAPI contract;
- confirmed that no employer selector, source identifier, Salesforce
  concept, backend pagination/filtering, enrollment action, runtime AI,
  or unapproved navigation has been introduced;
- confirmed that no React code, CSS, image, high-fidelity mockup, API
  change, security change, or data-model change has been created; and
- approved progression to the next planned lifecycle phase.

The Phase 9 User Experience Design satisfies these criteria and is
approved as the UX baseline for the Employer Account Portal MVP. The
environment-validation items above remain mandatory implementation and
validation evidence. Any material accessibility, performance, security,
or contract issue discovered later must be handled through a controlled
design review rather than an unrecorded workaround.
