"""Import-boundary conformance checks for the modular-monolith dependency rules.

Static AST parsing is used instead of a dependency-graph library: the check
set is small and stable, so a stdlib-only test keeps the architecture
validation itself framework-independent (Implementation Design SS5.1, SS7).
"""

from __future__ import annotations

import ast
import importlib
import pkgutil
from pathlib import Path

import app

APP_ROOT = Path(app.__file__).resolve().parent

# Domain must stay technology-neutral: no framework, database, or Salesforce
# client library, and no dependency on an outer layer.
FORBIDDEN_EXTERNAL_IN_DOMAIN = (
    "fastapi",
    "starlette",
    "sqlite3",
    "sqlalchemy",
    "httpx",
    "httpx2",
    "simple_salesforce",
)
FORBIDDEN_INTERNAL_IN_DOMAIN = ("app.api", "app.application", "app.adapters")


def _imported_module_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            names.add(node.module)
    return names


def _python_files(package_dir: Path) -> list[Path]:
    return sorted(package_dir.rglob("*.py"))


def _assert_none_imported(
    file: Path, imported: set[str], forbidden: tuple[str, ...], reason: str
) -> None:
    for name in imported:
        for prefix in forbidden:
            if name == prefix or name.startswith(f"{prefix}."):
                relative = file.relative_to(APP_ROOT.parent)
                raise AssertionError(f"{relative} imports {name}: {reason}")


def test_domain_has_no_framework_or_outer_layer_imports() -> None:
    for file in _python_files(APP_ROOT / "domain"):
        imported = _imported_module_names(file)
        _assert_none_imported(
            file,
            imported,
            FORBIDDEN_EXTERNAL_IN_DOMAIN,
            "domain must remain technology-neutral (Implementation Design SS5.1, SS7)",
        )
        _assert_none_imported(
            file,
            imported,
            FORBIDDEN_INTERNAL_IN_DOMAIN,
            "domain must not depend on an outer layer",
        )


def test_application_does_not_import_concrete_salesforce_adapter() -> None:
    for file in _python_files(APP_ROOT / "application"):
        imported = _imported_module_names(file)
        _assert_none_imported(
            file,
            imported,
            ("app.adapters.salesforce",),
            "application must depend on the Salesforce gateway port, not the concrete adapter",
        )


def test_api_does_not_import_salesforce_implementation_directly() -> None:
    for file in _python_files(APP_ROOT / "api"):
        imported = _imported_module_names(file)
        _assert_none_imported(
            file,
            imported,
            ("app.adapters.salesforce",),
            "API delivery must not import Salesforce implementation modules directly",
        )


def test_every_app_module_imports_without_circular_dependency() -> None:
    module_names = [name for _, name, _ in pkgutil.walk_packages(app.__path__, prefix="app.")]
    for name in [app.__name__, *module_names]:
        importlib.import_module(name)
