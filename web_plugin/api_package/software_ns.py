from flask import request
from flask_restx import Resource, Namespace
from flask_cors import cross_origin

import os
import sys
new_work_dir = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.append(new_work_dir)

from utils.custom_logger import CustomLogger

log_file_name = "api_package.log"
logger_instance = CustomLogger(logger_name="api_package",
                                dt_fmt='%H:%M:%S',
                                file_path=os.path.join(new_work_dir,"logs", log_file_name),
                                level="debug")
my_logger = logger_instance.logger

soft_ns = Namespace('software telemetry', description='access to software telemetry data')

@soft_ns.route("/hello")
class Hello(Resource):
    """Get hardware usage data
    """
    @cross_origin()
    @soft_ns.doc('hello - info field')
    def get(self):
        """starting collecting telemetry data
        """
        return 'Hello', 200
