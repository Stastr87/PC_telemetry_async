"""Define common logger"""

import os

from env.default_env import LOG_DIR
from utils.custom_logger import CustomLogger

LOG_FILE_NAME = "common_logger.log"
logger_instance = CustomLogger(
    logger_name="common_logger",
    file_path=os.path.join(LOG_DIR, LOG_FILE_NAME),
    level="debug",
)
common_logger = logger_instance.logger
