# Work Unit 1 — Repository Foundation

## Objective

Create the approved repository foundation: top-level structure, frontend
and backend toolchains, dependency manifests/lock files, ignore rules,
placeholder environment configuration, repeatable root-level build/lint/
type-check/test commands, baseline test runners, and secret-scanning
configuration. No business logic, authentication, Salesforce integration,
Account 360, API endpoints, UI screens, or runtime AI were added.

## Approved Inputs

- [Implementation Design](../docs/design/05-implementation-design.md) §§3–4 (technology stack), §17 (proposed repository structure), §18 (local development experience)
- [AI-Assisted Engineering Plan](../docs/ai/10-ai-assisted-engineering-plan.md) §9 (Work Unit 1 row), §13 (validation commands)
- [Security Design](../docs/security/07-security-design.md) §12 (secret management), §16 (dependency/supply-chain security)

## Traceability

| Trace ID | Requirement / rule | Design authority | Work unit | Implementation files | Validation evidence | Status |
|---|---|---|---|---|---|---|
| WU1-STRUCT | Approved top-level folders | Implementation Design §17 | 1 | repo root | `ls` (see Implementation Notes) | Complete |
| WU1-FE-TOOLCHAIN | React + TypeScript (strict) + Vite + ESLint + Prettier + Vitest | Implementation Design §3.1, §4 | 1 | `frontend/` | `make lint-frontend format-check-frontend typecheck-frontend build-frontend test-frontend` | Complete |
| WU1-BE-TOOLCHAIN | Python + FastAPI + pytest + Ruff + mypy | Implementation Design §3.2, §4 | 1 | `backend/` | `make lint-backend format-check-backend typecheck-backend test-backend` | Complete |
| WU1-SECRETS | No secrets committed; placeholder config only | Security Design §12, §16 | 1 | `.env.example`, `.gitignore`, `.gitleaks.toml` | `make secret-scan` | Complete |

## AI Contribution

- Classification: AI Generated, AI Assisted
- AI tool/model: Claude Code (Claude Sonnet 5)
- Candidate work produced: full repository scaffold — top-level folders,
  Vite React-TS frontend with ESLint/Prettier/Vitest substituted for the
  template's default `oxlint`, FastAPI backend managed with `uv`
  (pyproject.toml, lock file, Ruff, mypy strict), root `Makefile` task
  interface, `.gitignore`, `.env.example`, `.gitleaks.toml`, and this
  journal entry.

## Human Engineering Decisions

- Classification: Human Designed (via approved specifications)
- Decisions and rejected alternatives:
  - Kept only the top-level directories named in the work order
    (`frontend/`, `backend/`, `contracts/`, `docs/`, `tests/`, `scripts/`,
    `engineering-journal/`, `prompts/`, `assets/`). Deferred the deeper
    `backend/app/{api,application,domain,ports,adapters,core}` module
    boundaries to Work Unit 2 ("Backend Skeleton"), which explicitly owns
    "application/domain/ports/adapters/core module boundaries" per the
    AI-Assisted Engineering Plan §9. `backend/app/` currently holds only
    a bare `FastAPI()` instance.
  - Replaced Vite's current default template content: its scaffold now
    ships `oxlint` instead of ESLint, and its `tsconfig.app.json` does
    not enable `strict` by default. Both were corrected to match the
    approved stack (ESLint + Prettier, TypeScript strict mode).
  - Removed the Vite template's marketing homepage (hero image, social
    links, counter demo) and replaced it with a one-line placeholder,
    since implementing UI screens is out of scope for this work unit.
  - Deferred Playwright and React Testing Library's use in real
    component tests until UI exists (Work Units 9–11); added
    `@testing-library/react` now since it is already an approved
    technology (Implementation Design §3, "Frontend testing" row) and is
    exercised by the WU1 smoke test.
  - Did not add `pydantic-settings` or any configuration-loading code in
    WU1; `.env.example` documents anticipated non-secret variable names
    only, matching "placeholder environment configuration" — wiring
    belongs to the Configuration responsibility in Work Unit 2's `core`
    module.
  - `uv` was chosen as the backend package/lock-file manager (produces
    `uv.lock`, integrates Ruff/mypy/pytest cleanly, fast clean installs);
    it is a build tool, not an application dependency.

## Implementation Notes

- Files/modules affected:
  - Root: `Makefile`, `.gitignore`, `.env.example`, `.gitleaks.toml`,
    `README.md`, `engineering-journal/01-repository-foundation.md`,
    placeholder `README.md` files in `scripts/`, `assets/`, `prompts/`,
    `tests/e2e/`, `tests/fixtures/salesforce/`.
  - `frontend/`: Vite React-TS scaffold with `eslint.config.js`,
    `.prettierrc.json`, `.prettierignore`, `vite.config.ts` (Vitest
    config merged in), `src/test/setup.ts`, `src/App.test.tsx`, strict
    `tsconfig.app.json`/`tsconfig.node.json`, minimal `src/App.tsx`.
  - `backend/`: `pyproject.toml`, `uv.lock`, `.python-version`,
    `app/__init__.py`, `app/main.py` (bare `FastAPI()` instance, no
    custom routes), `tests/test_main.py` (smoke test against the
    framework's own `/openapi.json`).
- Dependency changes and approvals — all newly added, each justified
  against an approved technology-stack row or an explicit WU1 exit
  requirement:
  - Frontend: `react`, `react-dom` (approved stack); `typescript`,
    `vite`, `@vitejs/plugin-react` (approved stack); `eslint`,
    `@eslint/js`, `typescript-eslint`, `eslint-plugin-react-hooks`,
    `eslint-plugin-react-refresh`, `eslint-config-prettier`, `globals`
    (approved: ESLint); `prettier` (approved: Prettier); `vitest`,
    `jsdom`, `@testing-library/react`, `@testing-library/jest-dom`,
    `@testing-library/dom` (approved: Vitest, React Testing Library).
  - Backend: `fastapi` (approved stack); `uvicorn[standard]` — required
    to start the ASGI application locally/in CI ("backend imports/startup
    succeeds", "baseline starts" exit evidence); `pytest` (approved
    stack); `httpx2` — required by Starlette's `TestClient` (the
    predecessor `httpx` integration is deprecated by the installed
    Starlette release); `ruff`, `mypy` (approved stack).
  - No dependency outside the approved lists in Implementation Design §4
    was added.

## Problems / AI Mistakes

- Observed issue: `create-vite`'s current `react-ts` template ships
  `oxlint` (not ESLint) and does not set `"strict": true` in
  `tsconfig.app.json`, silently diverging from the approved "ESLint" and
  "strict TypeScript" decisions if left unexamined.
- Observed issue: the initial ESLint flat config used
  `reactHooks.configs['recommended-latest']`, which is the legacy
  eslintrc-shaped export in `eslint-plugin-react-hooks@7`; ESLint failed
  at startup ("plugins key defined as an array of strings"). The correct
  flat-config export is `reactHooks.configs.flat['recommended-latest']`.
- Observed issue: `uv init --package .` scaffolds a `src/<name>/` layout
  with a `uv_build` backend that requires an installable package; this
  does not match the approved `backend/app/` structure and is unnecessary
  for an application (not a library). Corrected by setting
  `[tool.uv] package = false` and placing the app directly under
  `backend/app/`.
- Observed issue: `pytest` initially reported a `StarletteDeprecationWarning`
  recommending `httpx2` over `httpx` for `TestClient`. Corrected by
  depending on `httpx2` directly, which resolved the warning.

## Corrections

- Swapped `oxlint` for ESLint + `typescript-eslint` + `eslint-config-prettier`;
  removed `.oxlintrc.json`.
- Added `"strict": true` (plus `noUncheckedIndexedAccess`,
  `exactOptionalPropertyTypes`) to both `tsconfig.app.json` and
  `tsconfig.node.json`.
- Fixed the ESLint config to use `reactHooks.configs.flat['recommended-latest']`.
- Reset the backend to a flat `app/` package with `[tool.uv] package = false`
  instead of the generated `src/backend/` library layout.
- Replaced `httpx` with `httpx2` in backend dev dependencies.

## Validation

- Command: `make install` — Result: pass (clean `npm install` and `uv sync`
  from a clean checkout).
- Command: `make lint` (`eslint .` + `ruff check .`) — Result: pass, no findings.
- Command: `make format-check` (`prettier --check .` + `ruff format --check .`)
  — Result: pass, all files already formatted.
- Command: `make typecheck` (`tsc -b` + `mypy`, both strict) — Result: pass,
  no issues found.
- Command: `make build-frontend` (`tsc -b && vite build`) — Result: pass,
  production bundle produced.
- Command: `make test` (`vitest run` + `pytest`) — Result: pass, 1/1
  frontend test and 1/1 backend test.
- Command: backend startup smoke check
  (`uv run python -c "from app.main import app"` plus the pytest smoke
  test hitting FastAPI's own `/openapi.json`) — Result: pass, app imports
  and serves its schema.
- Command: `make secret-scan` (`gitleaks detect --source . --config .gitleaks.toml --redact -v`)
  — Result: pass, "no leaks found" across the full commit history.
- Classification: Human Validated — all checks above reviewed and
  accepted for this work unit.

## Effort Observations

- Not measured: no elapsed-time instrumentation was used for this
  session; no defensible non-AI baseline exists for this work unit.
- Qualitative: AI-assisted scaffolding surfaced two toolchain drifts
  (default `oxlint`, non-strict `tsconfig`) that a human would otherwise
  have had to notice and correct manually; the API-shape errors (ESLint
  plugin export, `uv` package layout, `httpx`/`httpx2`) were caught
  immediately by running the actual validation commands rather than
  trusting generated config.

## Lessons Learned

- Scaffolding tools' current defaults must not be assumed to match an
  approved technology decision; each generated config was checked
  against Implementation Design §3–§4 line by line.
- Running every validation command immediately after generating config
  (rather than after the whole work unit) caught three toolchain
  mismatches early, before they could compound.

## Reusable Assets

- Root `Makefile` pattern wrapping two independent toolchains (`npm`,
  `uv`) behind one command surface (`make install|lint|format|typecheck|test|secret-scan|validate`).
- `.gitleaks.toml` allowlist pattern for lock files and non-secret
  placeholder/fixture paths.

## Post-Approval Housekeeping (pre–Work Unit 2)

Two conditions attached to WU1's conditional approval, addressed before
starting Work Unit 2.

### 1. Untracked `.DS_Store` files

- Observed issue: `.DS_Store` was already listed in `.gitignore`, but
  `.DS_Store`, `docs/.DS_Store`, and `docs/security/.DS_Store` had been
  committed in earlier phase commits (before WU1), so the ignore rule did
  not retroactively untrack them.
- Correction: `git rm --cached .DS_Store docs/.DS_Store docs/security/.DS_Store`
  — removes them from Git tracking without touching file content on disk
  or any unrelated file.
- Validation: `git ls-files | grep -i DS_Store` returns nothing after the
  change; `grep -n DS_Store .gitignore` confirms the existing bare
  `.DS_Store` rule (matches at any depth) still covers future occurrences.
  No other tracked `.DS_Store` files exist in the repository.
- Classification: Human Validated.

### 2. `httpx2` dependency verification

Verified against Security Design §16 ("pin direct and transitive
dependencies in committed lock files; review every newly introduced
dependency for maintainer, ... necessity").

- Exact installed package: `httpx2`, resolved/locked version `2.12.0`
  (`backend/uv.lock`).
- Why required: `starlette.testclient.TestClient` (which
  `fastapi.testclient.TestClient` re-exports directly —
  `TestClient.__module__ == 'starlette.testclient'`) requires an HTTP
  transport library at import time. The installed Starlette release
  (`1.6.0`) prefers `httpx2` and only falls back to the legacy `httpx`
  package with a `StarletteDeprecationWarning` if `httpx2` is absent; if
  neither is installed, `TestClient` raises `RuntimeError` at import.
  Without `httpx2`, `tests/test_main.py` cannot run.
- Directly declared or transitive: **directly declared**, in
  `backend/pyproject.toml` under `[dependency-groups] dev`. Confirmed via
  `importlib.metadata.requires('starlette')`: Starlette lists `httpx2` and
  `httpx` only as optional `extra == "full"` markers, not as an
  unconditional dependency — installing `starlette` or `fastapi` alone
  does **not** pull in `httpx2` transitively. The explicit dev dependency
  is necessary, not redundant.
- Confirmed in active use: ran
  `uv run python -W error::DeprecationWarning -c "from fastapi.testclient import TestClient; from app.main import app; TestClient(app).get('/openapi.json')"`
  — no `DeprecationWarning` raised and the request returned `200`,
  proving `httpx2` (not the deprecated `httpx` path) is what actually
  services the test client at runtime.
- Finding requiring a change: the declared constraint (`httpx2>=1`, no
  upper bound) was the only dependency in `backend/pyproject.toml`
  without an upper bound — inconsistent with the pinning style used for
  every sibling dependency (`fastapi>=0.121,<1`, `uvicorn[standard]>=0.38,<1`,
  `pytest>=8.4,<9`, `ruff>=0.14,<1`, `mypy>=1.19,<2`) and with Security
  Design §16's dependency-pinning expectation. Not a functional defect —
  the lock file already pinned the resolved version exactly — but a
  consistency gap worth closing while re-verifying.
- Smallest compliant change: tightened `backend/pyproject.toml` from
  `"httpx2>=1"` to `"httpx2>=2,<3"` (matches the currently resolved major
  version, same bounding style as its siblings), then ran `uv sync` to
  regenerate `backend/uv.lock`. Resolved/locked version is unchanged at
  `2.12.0`.
- Validation after the change: `uv run ruff check .` (pass), `uv run ruff
  format --check .` (pass, 4 files formatted), `uv run mypy` (pass, no
  issues in 4 source files), `uv run pytest -v` (pass, 1/1). Full root
  `make validate` rerun — see Work Unit 2 journal for the combined
  post-housekeeping result.
- Classification: Human Validated.
