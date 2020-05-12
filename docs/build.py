"""
Builds the documentation as a static web page.

The files here are used to automatically create the documentation for
the package from the documentation's source (in the `source` folder)
as well as the documentation string in the package's source code.

The renderer is the documentation generator Sphinx, which is configured
via the (Python) script `conf.py`. All text may use mark-up according
to the CommonMark specification of the Markdown syntax, as supported
by the Sphinx extension `recommonmark`, which is used to convert
Markdown to reStructuredText, Sphinx's native input format.

The HTML documentation will end up in the `build` folder, where
`index.html` is the start page. It is essentially a static web
site that could be deployed to a web server as is.
"""
__license__ = 'MIT'

# Dependencies
from subprocess import run             # external processes
from pathlib import Path               # file-system paths

# Get absolute path to the folder this script resides in.
here = Path(__file__).absolute().parent

# Run Sphinx.
result = run('sphinx-build . build', cwd=here)
if result.returncode:
    raise RuntimeError(f'Error while building HTML source.')
