# Employer Account Portal

WorkflowFox Showcase #2 — a read-only Employer Account 360 portal. A
React/TypeScript/Vite frontend and a Python/FastAPI backend, organized as
a modular monolith, with Salesforce as the authoritative source for
Employer Account, Contact, and Enrollment data.

See [`docs/design/05-implementation-design.md`](docs/design/05-implementation-design.md)
for the approved architecture and technology decisions, and
[`docs/ai/10-ai-assisted-engineering-plan.md`](docs/ai/10-ai-assisted-engineering-plan.md)
for how this repository is built up in bounded, reviewed work units.

## Current status

This repository currently contains **Work Unit 1 — Repository Foundation**
only: the approved folder structure, pinned frontend/backend toolchains,
and repeatable root-level commands. No application behavior, API
endpoints, authentication, Salesforce integration, or UI screens exist
yet. See [`engineering-journal/01-repository-foundation.md`](engineering-journal/01-repository-foundation.md)
for what was built and validated.

## Repository structure

| Path | Contents |
|---|---|
| `frontend/` | React + TypeScript + Vite application |
| `backend/` | Python + FastAPI application (`uv`-managed) |
| `contracts/` | The approved OpenAPI contract |
| `docs/` | Phase-by-phase design documentation |
| `tests/` | Cross-cutting end-to-end tests and Salesforce fixtures |
| `scripts/` | Repeatable setup/seed/validation tasks |
| `engineering-journal/` | Per-work-unit engineering evidence |
| `prompts/` | Sanitized, reusable AI-assistance prompts |
| `assets/` | Screenshots and other publishable assets |

## Requirements

- Node.js (current LTS) and npm
- Python 3.12+ and [`uv`](https://docs.astral.sh/uv/)
- [`gitleaks`](https://github.com/gitleaks/gitleaks) for local secret scanning

## Getting started

All common tasks are wrapped by the root `Makefile` so contributors do
not need to memorize `npm`/`uv` invocations directly:

```bash
make install        # install frontend and backend dependencies
make build           # production frontend build
make lint             # ESLint + Ruff
make format-check     # Prettier + Ruff format, check only
make typecheck        # tsc --build (strict) + mypy (strict)
make test             # Vitest + pytest
make secret-scan       # Gitleaks over the full repository history
make validate           # install + lint + format-check + typecheck + test + secret-scan

make frontend-dev    # run the Vite dev server
make backend-dev     # run the FastAPI app with uvicorn --reload
```

Copy [`.env.example`](.env.example) to a local, git-ignored `.env` before
running the backend; see [Security Design §12](docs/security/07-security-design.md#12-secret-management)
for what belongs — and what must never appear — in that file.
