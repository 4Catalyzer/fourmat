import os
import shutil
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from subprocess import CalledProcessError

import click

from . import ASSETS_DIR, cli

# -----------------------------------------------------------------------------

CONFIG_FILE = ".fourmat"

CONFIGURATION_FILES = (".flake8", "pyproject.toml")

# -----------------------------------------------------------------------------
class PathContext:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.init_wd = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, _1, _2, _3):
        os.chdir(self.init_wd)


class Project:
    _PROJECT_ROOT = None

    @classmethod
    def get_root(cls):
        if cls._PROJECT_ROOT is not None:
            return cls._PROJECT_ROOT
        init_wd = Path(os.getcwd())
        git_root = cls._git_root()
        git_root_path = Path(git_root) if git_root else None
        cursor = init_wd

        def paths_are_equal(lh, rh):
            return str(lh.resolve()) == str(rh.resolve())

        def cursor_is_project_root():
            if (cursor / "pyproject.toml").exists():
                return True
            if (cursor / ".fourmat").exists():
                return True
            if git_root_path and paths_are_equal(git_root_path, cursor):
                return True

        # Search iteratively through parent directories until the project root is reached.
        while not cursor_is_project_root():
            next_wd = cursor.parent
            if paths_are_equal(next_wd, cursor):
                # Root directory reached. Default to PWD of execution.
                cursor = init_wd
                break
            cursor = next_wd

        cls._PROJECT_ROOT = cursor
        return cursor.resolve()

    @staticmethod
    def _git_root():
        try:
            git_toplevel_cmd = subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"],
                universal_newlines=True,
                stdout=subprocess.PIPE,
            )
            return git_toplevel_cmd.split("\n")[0]
        except Exception:
            return ""


def get_project_paths():
    conf = Project.get_root() / CONFIG_FILE
    return conf.read_text().split()


# -----------------------------------------------------------------------------


def copy_configuration(override=False):
    with PathContext(Project.get_root()):
        for name in CONFIGURATION_FILES:
            if override is True or not Path(name).exists():
                # This will always be in project root because we implicitly assert
                # in get_project_paths().
                shutil.copy(ASSETS_DIR / name, ".")


def black(paths, *, check=False):
    subprocess.run(
        (
            "black",
            *(("--check", "--diff") if check else ()),
            "--quiet",
            "--",
            *paths,
        ),
        check=True,
    )


def isort(paths, *, check=False):
    subprocess.run(
        (
            "isort",
            *(("--check", "--diff") if check else ()),
            "--atomic",
            "--quiet",
            "--",
            *paths,
        ),
        check=True,
    )


def flake8(paths, *, check=True):
    assert check is True, "Flake8 has no fix mode"

    subprocess.run(("flake8", "--", *paths), check=True)


# -----------------------------------------------------------------------------


@cli.command(
    help=f"check code style. If no file is specified, it will run on all the files specified in {CONFIG_FILE}"
)
@click.option(
    "-c",
    "--override-config",
    is_flag=True,
    help=f"specify this flag to override the config files ({', '.join(CONFIGURATION_FILES)})",
)
@click.argument("files", nargs=-1)
def check(override_config, files):
    try:
        if not files:
            files = get_project_paths()
            os.chdir(Project.get_root())
        copy_configuration(override=override_config)

        status = 0

        @contextmanager
        def record_failure():
            try:
                yield
            except CalledProcessError:
                nonlocal status
                status = 1

        # When linting, continue running linters even after failures, to
        # display all lint errors.
        with record_failure():
            isort(files, check=True)
        with record_failure():
            black(files, check=True)
        with record_failure():
            flake8(files, check=True)

        if status:
            sys.exit(status)
    except KeyboardInterrupt:
        pass


@cli.command(
    "fix",
    help=f"automatically fix code. If no file is specified, it will run on all the files specified in {CONFIG_FILE}",
)
@click.option(
    "-c",
    "--override-config",
    is_flag=True,
    help=f"specify this flag to override the config files ({', '.join(CONFIGURATION_FILES)})",
)
@click.argument("files", nargs=-1)
def fix(*, override_config, files):
    try:
        if not files:
            files = get_project_paths()
            os.chdir(Project.get_root())
        copy_configuration(override=override_config)

        isort(files)
        black(files)
        flake8(files)
    except CalledProcessError as e:
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        pass
