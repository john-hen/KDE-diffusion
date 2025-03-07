"""Meta information about the application"""

import importlib.metadata

name = 'KDE-diffusion'
try:
    metadata = importlib.metadata.metadata(name)
except importlib.metadata.PackageNotFoundError:              # pragma: no cover
    raise RuntimeError(
        'Application name is wrong in package metadata.'
    ) from None

version = metadata['Version']
summary = metadata['Summary']
