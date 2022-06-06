import io
import os

from setuptools import find_packages, setup
NAME = "action-launcher"
DESCRIPTION = "Implements methos to make an API SERVER"
AUTHOR = ""
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "1.1.0"
REQUIRED = [
    "library-chain==1.1.0", 
    "preprocessor==1.1.0"
]
EXTRAS_REQUIRED = {}
ENTRY_POINTS = {
    "console_scripts": [
        "acc_admin_action_launcher = actions_chain.acc_admin_action_launcher:main", 
        "acc_node_action_launcher = actions_chain.acc_node_action_launcher:main", 
        "root_node_action_launcher = actions_chain.root_node_action_launcher:main" 
    ]
}

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
    include_package_data=True,
    entry_points=ENTRY_POINTS,
)


