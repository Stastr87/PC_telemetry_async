"""API client for PC telemetry service"""

import json
import requests
from requests.exceptions import HTTPError
from base_api import BaseApi
#Logger config
import os
import sys

from telemetry_api_client.config import HOST

new_work_dir = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(new_work_dir)
from utils.custom_logger import CustomLogger

log_file_name = "telemetry_api_client.log"
logger_instance = CustomLogger(logger_name="telemetry_api_client",
                                dt_fmt='%H:%M:%S',
                                file_path=os.path.join(new_work_dir,"logs", log_file_name),
                                level="debug")
my_logger = logger_instance.logger


class TelemetryApiClient(BaseApi):

    def __init__(
        self,
        host: str = HOST,
        name_space: str = 'api/v1'
        # login: str = "admin",
        # password: str = "admin",
    ):
        super().__init__()
        self.host = host
        self.api_name_space = name_space

    def return_hw_data_post_new(self, start_time: str, end_time: str):
        hw_usage_period = {"start_time": start_time,
                           "end_time": end_time}
        return self.post('return_hw_data', hw_usage_period)


