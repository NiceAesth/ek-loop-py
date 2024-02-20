from datetime import date
from importlib import metadata

__title__ = "ek-loop-py"
__author__ = "Nice Aesthetics"
__license__ = "MIT"
__copyright__ = f"Copyright {date.today().year} {__author__}"

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    import tomllib

    __version__ = tomllib.load("pyproject.toml")["tool"]["poetry"]["version"] + "dev"
