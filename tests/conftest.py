from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
from PySide6 import QtWidgets


def _add_local_venv_site_packages() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))
    py_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    site_packages = repo_root / ".venv" / "lib" / py_version / "site-packages"
    if site_packages.exists():
        sys.path.append(str(site_packages))


_add_local_venv_site_packages()


def pytest_ignore_collect(collection_path: Path, config: pytest.Config) -> bool:
    markexpr = (config.option.markexpr or "").strip()
    if markexpr != "unit":
        return False

    normalized = collection_path.as_posix().rstrip("/")
    if normalized.endswith("tests") or normalized.endswith("tests/unit"):
        return False
    return "tests/unit/" not in normalized


@pytest.fixture(scope="session")
def qapp() -> QtWidgets.QApplication:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    return app


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    known = {"unit", "contract", "integration", "e2e"}
    for item in items:
        if any(item.get_closest_marker(name) for name in known):
            continue
        item.add_marker(pytest.mark.integration)
