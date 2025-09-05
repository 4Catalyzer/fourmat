from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import click

# -----------------------------------------------------------------------------


try:
    __version__ = version(__name__)
except PackageNotFoundError:
    raise RuntimeError(f"Package '{__name__}' is not installed.")

# -----------------------------------------------------------------------------

ASSETS_DIR = Path(__file__).parent / "assets"

# -----------------------------------------------------------------------------


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


# -----------------------------------------------------------------------------

from . import lint  # isort:skip  # noqa: F401
