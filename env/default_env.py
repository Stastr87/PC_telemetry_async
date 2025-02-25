"""Define environment params for multi OS usage"""

import os
from sys import path

NEW_WORK_DIR = os.path.abspath(os.path.join(__file__, "../.."))
path.append(NEW_WORK_DIR)

# PATH_TO_PYTHON_EXE = os.path.join("C:\\", ".venv", "python312", "Scripts", "python.exe")
PATH_TO_PYTHON_EXE = (
    'path for "python.exe" file for strating scrypts via api OS windows'
)
PATH_TO_PYTHON_LINUX = "python3"
LOG_DIR = os.path.join(NEW_WORK_DIR, "logs")
# Use False in production mode
DEBUG_MODE = True
# Use True if production as Docker image
DOCKER_MODE = False
RESPONSE_TEMP_DIR = os.path.join(NEW_WORK_DIR, "tempdir", "response_files")
