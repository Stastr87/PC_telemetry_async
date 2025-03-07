"""Define environment params for multi OS usage"""

import os
from sys import path

NEW_WORK_DIR = os.path.abspath(os.path.join(__file__, "../.."))
path.append(NEW_WORK_DIR)

PATH_TO_PYTHON_EXE = ""

PATH_TO_PYTHON_LINUX = "python3"

LOG_DIR = os.path.join(NEW_WORK_DIR, "logs")

# Use False for production
DEBUG_MODE = False

# Use True if production as Docker image
DOCKER_MODE = True

# temp dir for json files created during requests
RESPONSE_TEMP_DIR = os.path.join(NEW_WORK_DIR, "tempdir", "response_files")
# time period for clean RESPONSE_TEMP_DIR
CLEAR_TEMP_FOLDER_TIMEOUT = 15

# web server params
API_HOST = "0.0.0.0"
API_PORT = 5555
