import sys
import os

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.join(
    SRC_DIR, os.path.basename(os.path.dirname(SRC_DIR))
))
