from pathlib import Path
from pkg_resources import get_distribution, DistributionNotFound

import click

# -----------------------------------------------------------------------------

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass

# -----------------------------------------------------------------------------

ASSETS_DIR = Path(__file__).parent / "assets"

# -----------------------------------------------------------------------------


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


# -----------------------------------------------------------------------------

from . import lint  # noqa: F401
