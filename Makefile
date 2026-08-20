.PHONY: install install-frontend install-backend \
	build build-frontend \
	lint lint-frontend lint-backend \
	format format-check format-frontend format-check-frontend format-backend format-check-backend \
	typecheck typecheck-frontend typecheck-backend \
	test test-frontend test-backend \
	backend-dev frontend-dev \
	secret-scan validate clean

# --- Install ---

install: install-frontend install-backend

install-frontend:
	cd frontend && npm install

install-backend:
	cd backend && uv sync

# --- Build / startup ---

build: build-frontend

build-frontend:
	cd frontend && npm run build

backend-dev:
	cd backend && uv run uvicorn app.main:app --reload

frontend-dev:
	cd frontend && npm run dev

# --- Lint ---

lint: lint-frontend lint-backend

lint-frontend:
	cd frontend && npm run lint

lint-backend:
	cd backend && uv run ruff check .

# --- Format ---

format: format-frontend format-backend

format-check: format-check-frontend format-check-backend

format-frontend:
	cd frontend && npm run format

format-check-frontend:
	cd frontend && npm run format:check

format-backend:
	cd backend && uv run ruff format .

format-check-backend:
	cd backend && uv run ruff format --check .

# --- Type check ---

typecheck: typecheck-frontend typecheck-backend

typecheck-frontend:
	cd frontend && npm run typecheck

typecheck-backend:
	cd backend && uv run mypy

# --- Test ---

test: test-frontend test-backend

test-frontend:
	cd frontend && npm test

test-backend:
	cd backend && uv run pytest

# --- Security ---

secret-scan:
	gitleaks detect --source . --config .gitleaks.toml --redact -v

# --- Aggregate ---

validate: install lint format-check typecheck build test secret-scan

clean:
	rm -rf frontend/dist frontend/coverage frontend/node_modules/.tmp
	rm -rf backend/.pytest_cache backend/.mypy_cache backend/.ruff_cache
