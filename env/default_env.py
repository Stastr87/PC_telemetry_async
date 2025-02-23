from sys import path
import os

NEW_WORK_DIR = os.path.abspath(os.path.join(__file__, "../.."))
path.append(NEW_WORK_DIR)

PATH_TO_PYTHON_EXE = os.path.join('C:\\', '.venv', 'python312', 'Scripts', 'python.exe')
PATH_TO_PYTHON_LINUX = "python3"
LOG_DIR = os.path.join(NEW_WORK_DIR, 'logs')
DEBUG_MODE = True
DOCKER_MODE = False
RESPONSE_TEMP_DIR = os.path.join(NEW_WORK_DIR, 'tempdir', 'response_files')