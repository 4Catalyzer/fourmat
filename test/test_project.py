import os
from pathlib import Path
import pytest

from fourmat.lint import Project, PathContext

TEST_DIR = Path(__file__).parent.resolve()
REPO_ROOT = TEST_DIR.parent.resolve()


@pytest.fixture
def reset():
    Project._PROJECT_ROOT = None
    os.chdir(REPO_ROOT)


def test_project(reset):
    with PathContext(TEST_DIR):
        assert str(Project.get_root()) == str(REPO_ROOT)


def test_with_pyproject(reset):
    test_project_path = (TEST_DIR / "fixture" / "test_project").resolve()
    with PathContext(test_project_path):
        assert str(Project.get_root()) == str(test_project_path)


def test_with_fourmat_file(reset):
    test_project_path = (
        TEST_DIR / "fixture" / "test_project_fourmat"
    ).resolve()
    with PathContext(test_project_path):
        assert str(Project.get_root()) == str(test_project_path)


def test_fixture_dir(reset):
    fixture = (TEST_DIR / "fixture").resolve()
    with PathContext(fixture):
        assert str(Project.get_root()) == str(REPO_ROOT)


def test_system_pwd_fallback(reset):
    with PathContext("/tmp"):
        assert str(Project.get_root()) == str(Path("/tmp").resolve())
