import sys
import os

# Setup some variables
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(SRC_DIR)
PACKAGE_NAME = os.path.basename(ROOT).replace("-", "_")
PACKAGE_DIR = os.path.join(SRC_DIR, PACKAGE_NAME)

# Add the package directory to the python path so our tests can use it.
sys.path.append(PACKAGE_DIR)

# Run the tests...
