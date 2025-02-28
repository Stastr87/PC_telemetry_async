"""Define environment params for multi OS usage"""

import os
from sys import path

NEW_WORK_DIR = os.path.abspath(os.path.join(__file__, "../.."))
path.append(NEW_WORK_DIR)

PATH_TO_PYTHON_EXE = os.path.join(
    "C:\\",
    "Users",
    "stast",
    ".virtualenvs",
    "pc_telemetry-I_k8Wp_S",
    "Scripts",
    "python.exe",
)
# PATH_TO_PYTHON_EXE = (
#     'path for "python.exe" file for starting scripts via api OS windows'
# )
PATH_TO_PYTHON_LINUX = "python3"
LOG_DIR = os.path.join(NEW_WORK_DIR, "logs")
# Use False for production
DEBUG_MODE = False
# Use True if production as Docker image
DOCKER_MODE = True
RESPONSE_TEMP_DIR = os.path.join(NEW_WORK_DIR, "tempdir", "response_files")

API_HOST = "0.0.0.0"

API_PORT = 5555
