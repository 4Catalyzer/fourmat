import shutil
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from subprocess import CalledProcessError

import click

from . import ASSETS_DIR, cli

# -----------------------------------------------------------------------------

CONFIG_FILE = Path(".fourmat")

SNAPSHOT_GLOB = "*/snapshots/snap_*.py"
SNAPSHOT_REGEX = r".*\/snapshots\/snap_.*\.py"
CONFIGURATION_FILES = (".flake8", "pyproject.toml")


class PyProjectConfig:
    """
    Helper methods to access pyproject.toml settings
    """

    PATH = Path("pyproject.toml")
    CONF = None

    @property
    def _data(self):
        if self.CONF is None:
            try:
                import toml
                self.CONF = toml.load(self.PATH)
            except ImportError:
                self.CONF = {}
        return self.CONF

    @property
    def isort(self):
        """
        Returns isort settings in pyproject.toml
        """
        return self._data.get("isort") or None

    @property
    def black(self):
        """
        Returns black settings in pyproject.toml
        """
        return self._data.get("black") or None


PY_PROJECT_CONFIG = PyProjectConfig()


class IsortConfig:
    DOT_ISORT = Path(".isort.cfg")

    def __init__(self):
        self._has_extend_skip_glob = None

    @property
    def has_extend_skip_glob(self):
        """
        Returns True if the user has specified extend_skip_glob in their .isort.cfg
        or pyproject.toml configuration.
        """
        if self._has_extend_skip_glob is None:
            if self.DOT_ISORT.exists():
                self._has_extend_skip_glob = (
                    "extend_skip_glob" in self.DOT_ISORT.read_text()
                )
            else:
                isort_cfg = PY_PROJECT_CONFIG.isort
                if isort_cfg is not None:
                    self._has_extend_skip_glob = (
                        "extend_skip_glob" in isort_cfg
                    )
            self._has_extend_skip_glob = False
        return self._has_extend_skip_glob


ISORT_CONFIG = IsortConfig()

# -----------------------------------------------------------------------------


def get_project_paths():
    return CONFIG_FILE.read_text().split()


# -----------------------------------------------------------------------------


def copy_configuration(override=False):
    for name in CONFIGURATION_FILES:
        if override is True or not Path(name).exists():
            # This will always be in project root because we implicitly assert
            # in get_project_paths().
            shutil.copy(ASSETS_DIR / name, ".")


def black(paths, *, check=False):
    # Do not override extend-exclude if the user has specified it in their black configuration
    exclude_arg = (
        ()
        if "extend_exclude" in (PY_PROJECT_CONFIG.black or {})
        else ("--extend-exclude", SNAPSHOT_REGEX)
    )
    subprocess.run(
        (
            "black",
            *(("--check", "--diff") if check else ()),
            *exclude_arg,
            "--quiet",
            "--",
            *paths,
        ),
        check=True,
    )


def isort(paths, *, check=False):
    # Do not override extend-skip-glob if the user has specified it in their isort configuration
    skip_arg = (
        ()
        if ISORT_CONFIG.has_extend_skip_glob
        else ("--extend-skip-glob", SNAPSHOT_GLOB)
    )
    subprocess.run(
        (
            "isort",
            *(("--check", "--diff") if check else ()),
            *skip_arg,
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
        files = files or get_project_paths()
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
        files = files or get_project_paths()
        copy_configuration(override=override_config)

        isort(files)
        black(files)
        flake8(files)
    except CalledProcessError as e:
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        pass
