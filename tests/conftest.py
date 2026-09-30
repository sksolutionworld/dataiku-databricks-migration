from pathlib import Path

import pytest


@pytest.fixture
def titanic_project_root() -> Path:
    return Path(__file__).parents[1] / "projects" / "TITANIC_MIGRATION_POC"
