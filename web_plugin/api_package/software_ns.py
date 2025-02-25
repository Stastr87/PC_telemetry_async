"""Define software telemetry section in swagger"""

import os
import sys

from flask_cors import cross_origin
from flask_restx import Namespace, Resource

from env.default_env import NEW_WORK_DIR
from utils.custom_logger import CustomLogger

sys.path.append(NEW_WORK_DIR)

LOG_FILE_NAME = "api_package.log"
logger_instance = CustomLogger(
    logger_name="api_package",
    file_path=os.path.join(NEW_WORK_DIR, "logs", LOG_FILE_NAME),
    level="debug",
)
my_logger = logger_instance.logger

soft_ns = Namespace(
    "software telemetry", description="access to software telemetry data"
)


@soft_ns.route("/hello")
class Hello(Resource):
    """Get hardware usage data"""

    @cross_origin()
    @soft_ns.doc("hello - info field")
    def get(self):
        """starting collecting telemetry data"""
        return "Hello", 200
