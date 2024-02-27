"""Init ShepardTTS module."""

from pathlib import Path

__version__ = "dev"

version_file = Path("_version.txt")

if version_file.is_file():
    with version_file.open() as fp:
        __version__ = fp.read().strip()
