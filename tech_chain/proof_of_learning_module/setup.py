import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = "proof_of_learning_module"
DESCRIPTION = "Proof of learning function for blck main funcs."
AUTHOR = ""
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "1.1.0"
REQUIRED = [ ]
EXTRAS_REQUIRED = {}
ENTRY_POINTS = {}


# Get the current path
here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description, if not there use the short description.
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        LONG_DESCRIPTION = '\n' + f.read()
except IOError:
    LONG_DESCRIPTION = DESCRIPTION

# Actual setup function:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(exclude=["docs", "docs.*", "tests", "tests.*"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS_REQUIRED,
    entry_points=ENTRY_POINTS
)

