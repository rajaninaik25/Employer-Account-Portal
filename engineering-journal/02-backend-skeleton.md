# Work Unit 2 — Backend Skeleton

## Objective

Establish the approved backend modular-monolith module boundaries
(`api/`, `application/`, `domain/`, `ports/`, `adapters/`, `core/`) with
minimal, startup-safe FastAPI wiring and automated architecture-boundary
checks — before any authentication, Salesforce, persistence, or
Employer Account 360 business behavior is implemented.

## Approved Inputs

- [Solution Architecture](../docs/architecture/04-solution-architecture.md) §§2–5 (architectural goals, principles, logical architecture, dependency direction, trust boundaries)
- [Implementation Design](../docs/design/05-implementation-design.md) §5 (implementation architecture, module dependency rules), §7 (backend module table), §17 (proposed repository structure)
- [AI-Assisted Engineering Plan](../docs/ai/10-ai-assisted-engineering-plan.md) §9 (Work Unit 2 row), §13 (validation commands)
- [Security Design](../docs/security/07-security-design.md) — reviewed; no security-sensitive behavior exists yet in this work unit

## Traceability

| Trace ID | Requirement / rule | Design authority | Work unit | Implementation files | Validation evidence | Status |
|---|---|---|---|---|---|---|
| WU2-STRUCT | Approved `backend/app/{api,application,domain,ports,adapters,core}` module boundaries | Implementation Design §7, §17 | 2 | `backend/app/**/__init__.py` | `find app -type f` (see Backend Module Structure) | Complete |
| WU2-DEPDIR | Inward dependency direction; domain is framework/adapter-free | Implementation Design §5.1; Solution Architecture §3 (principle 4), §4.1 | 2 | `backend/tests/test_architecture.py` | `uv run pytest tests/test_architecture.py -v` | Complete |
| WU2-STARTUP | FastAPI starts deterministically with no business routes, no secrets, no DB init | Implementation Design §5.2, §18.1; AI plan WU2 row | 2 | `backend/app/main.py`, `backend/app/api/router.py` | `uv run pytest tests/test_main.py -v`; manual `uvicorn` run (see Validation) | Complete |

## AI Contribution

- Classification: AI Generated, AI Assisted
- AI tool/model: Claude Code (Claude Sonnet 5)
- Candidate work produced: the six `app/` subpackages with one-line
  responsibility docstrings, `app/api/router.py` (empty `APIRouter`),
  `app/main.py` refactored into a `create_app()` composition function,
  `tests/test_architecture.py` (stdlib-`ast`-based import-boundary
  checks plus a circular-import walk), and an extra `test_main.py`
  assertion exercising `create_app()` directly.

## Human Engineering Decisions

- Classification: Human Designed (via approved specifications)
- Decisions and rejected alternatives:
  - Used a plain **stdlib `ast`-based static check** for import
    boundaries rather than a dependency-graph/architecture-testing
    library (e.g. `import-linter`, `pytest-archon`). The task explicitly
    called for "the simplest maintainable approach" and warned against
    "a heavy architecture framework solely for these checks"; `ast.walk`
    over each file's `Import`/`ImportFrom` nodes is enough to enforce
    the four required boundary rules without adding a dependency.
  - Verified the check is meaningful, not tautological: temporarily
    injected `import fastapi` into `app/domain/__init__.py`, confirmed
    `test_domain_has_no_framework_or_outer_layer_imports` failed with a
    clear message, then reverted and confirmed it passed again (see
    Validation). This follows the AI plan §14 guidance to "run the test
    against a deliberately wrong or missing behavior."
  - Added `application/authentication/` and
    `application/employer_account_360/` subpackages (not just a flat
    `application/`) because Implementation Design §17's proposed tree
    lists them explicitly as the two use cases in scope for the MVP.
  - Did **not** add abstract base classes to `ports/`, DTOs to `api/`,
    or entity stubs to `domain/`. The task allows placeholders "where
    needed to validate dependencies," but nothing in WU2 needs a concrete
    interface to exist yet — the architecture test validates the
    *absence* of forbidden imports, which requires no interface
    definitions. Finalizing port signatures now would risk conflicting
    with WU3 (Domain Models) or WU7/WU8, which own those decisions.
  - Left `core/` as an empty package with no configuration-loading code.
    The task allows structure "for future: configuration; logging;
    request IDs; error primitives" but explicitly caps scope at "no more
    than necessary for application startup" — and `create_app()`
    currently requires zero configuration, so adding
    `pydantic-settings` (or any config loader) now would be an
    unjustified dependency addition ahead of need, consistent with the
    WU1 decision to defer configuration wiring.
  - Did not forbid `pydantic` imports from `domain/` in the architecture
    test even though it forbids `fastapi`/`starlette`/`sqlalchemy`/etc.
    Implementation Design's module table lists domain's forbidden
    imports as "FastAPI, SQLAlchemy, frontend, or Salesforce types" —
    `pydantic` is not named, and forbidding it preemptively could
    conflict with a legitimate WU3 domain-modeling choice not yet made.
  - `app/main.py` keeps a module-level `app = create_app()` (for
    `uvicorn app.main:app`) alongside the `create_app()` factory (for
    the "clean composition function" requirement and for tests that
    want a fresh instance) rather than picking only one form.

## Implementation Notes

- Files/modules affected (all new; no existing WU1 file was modified
  except the WU1 housekeeping items recorded separately):
  - `backend/app/api/__init__.py`, `backend/app/api/router.py`
  - `backend/app/application/__init__.py`,
    `backend/app/application/authentication/__init__.py`,
    `backend/app/application/employer_account_360/__init__.py`
  - `backend/app/domain/__init__.py`
  - `backend/app/ports/__init__.py`
  - `backend/app/adapters/__init__.py`,
    `backend/app/adapters/persistence/__init__.py`,
    `backend/app/adapters/salesforce/__init__.py`
  - `backend/app/core/__init__.py`
  - `backend/app/main.py` (rewritten: `create_app()` factory + module-level `app`)
  - `backend/tests/test_architecture.py` (new)
  - `backend/tests/test_main.py` (extended with a `create_app()` assertion)
- Dependency changes: **none**. No new package was added in this work
  unit; the architecture checks use only the standard library (`ast`,
  `importlib`, `pkgutil`, `pathlib`).

## Problems / AI Mistakes

- Observed issue: the first draft of the architecture test forbade
  `pydantic` imports from `domain/`, extrapolating beyond what
  Implementation Design §7 actually lists as forbidden for domain models
  ("FastAPI, SQLAlchemy, frontend, or Salesforce types"). Left
  uncorrected, this would have pre-committed a domain-modeling
  constraint (plain dataclasses vs. pydantic `BaseModel`) that
  Work Unit 3 has not yet decided and the approved design does not
  require.
- Observed issue: initial one-line docstrings for
  `app/adapters/salesforce/__init__.py` and `app/ports/__init__.py`
  exceeded the project's 100-character Ruff line-length limit
  (`E501`), caught immediately by `ruff check`.

## Corrections

- Removed `pydantic` from the architecture test's forbidden-import list
  for `domain/`, keeping only what Implementation Design §7 actually
  names (web framework, database library, Salesforce client) plus
  network clients (`httpx`/`httpx2`), which §11.1 rules out for the
  Enrollment Summary domain service specifically ("does not access
  Salesforce, configuration, persistence, the session, or the
  frontend").
- Shortened the two over-length docstrings to fit the 100-character
  limit without wrapping into multi-line docstrings.

## Validation

- Command: `uv run ruff check .` — Result: pass, no findings (16 source files).
- Command: `uv run ruff format --check .` — Result: pass, all files formatted.
- Command: `uv run mypy` (strict) — Result: pass, no issues in 16 source files.
- Command: `uv run pytest -v` — Result: pass, 6/6
  (`test_architecture.py` ×4, `test_main.py` ×2).
- Architecture-check meaningfulness proof: temporarily added
  `import fastapi` to `app/domain/__init__.py` →
  `test_domain_has_no_framework_or_outer_layer_imports` FAILED with
  `AssertionError: app/domain/__init__.py imports fastapi: domain must
  remain technology-neutral`; reverted → same test PASSED again; the
  other three architecture tests were unaffected in both runs.
- Command: manual `uvicorn app.main:app --port 8123` on a background
  process, then `curl -s -o /dev/null -w '%{http_code}'
  http://127.0.0.1:8123/openapi.json` — Result: `200`, clean startup log
  (`Application startup complete` → request served → clean shutdown),
  confirming real ASGI startup (not just `TestClient`) with no runtime
  secret requirement and no database initialization.
- Command: full root `make validate` (install → lint → format-check →
  typecheck → build → test → secret-scan) from a clean checkout
  (`frontend/node_modules`, `backend/.venv`, `frontend/dist` removed
  first) — Result: pass end to end, including `gitleaks detect` ("no
  leaks found" across the full commit history).
- Classification: Human Validated — all checks above reviewed and
  accepted for this work unit.

## Effort Observations

- Not measured: no elapsed-time instrumentation was used; no defensible
  non-AI baseline exists for scaffolding six empty packages plus a
  boundary test.
- Qualitative: writing the architecture test forced an explicit
  re-reading of Implementation Design §7's "must not contain" column per
  module, which surfaced the pydantic over-constraint before it was
  committed — the test-writing process itself acted as a design-review
  step, not just a validation artifact.

## Lessons Learned

- When a design table gives an explicit forbidden-import list per
  module, encode exactly that list in the check — extrapolating to
  "obviously related" libraries (like pydantic, which is adjacent to but
  distinct from the named FastAPI/SQLAlchemy/Salesforce set) risks
  constraining a decision a later work unit is supposed to make.
- A negative-behavior proof (deliberately breaking the rule, confirming
  the test catches it, then reverting) is cheap and directly answers
  "does this test actually test anything," which a merely-passing suite
  cannot answer on its own.

## Reusable Assets

- `tests/test_architecture.py` pattern: stdlib-only, `ast`-based import
  boundary checks plus a `pkgutil.walk_packages` + `importlib`
  circular-import sweep. Reusable as-is for later work units — new
  forbidden-import rules can be added as additional tuples/tests without
  new dependencies, and the circular-import test automatically covers
  every new module added under `app/`.
