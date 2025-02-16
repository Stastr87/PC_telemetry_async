from json import dumps

import requests
from requests import Session, Response
from requests.exceptions import HTTPError

from env.default_env import LOG_DIR



import os
import sys
new_work_dir = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(new_work_dir)
from utils.custom_logger import CustomLogger

log_file_name = "base_api.log"
logger_instance = CustomLogger(logger_name="base_api",
                                dt_fmt='%H:%M:%S',
                                file_path=os.path.join(new_work_dir,LOG_DIR, log_file_name),
                                level="debug")
my_logger = logger_instance.logger

class BaseApi:
    def __init__(self):
        self.host = "undefined"
        self.session = Session()
        self.api_name_space = "undefined"
        self.api_url = "undefined"
        self.set_header("Content-Type", "application/json")

    def set_header(self, header: str, value: str) -> None:
        """Set session header"""
        self.session.headers.update({header: value})

    def set_request_url(self,end_point: str):
        return f'{self.host}/{self.api_name_space}/{end_point}'

    @staticmethod
    def response_data_catch(data: Response):
        """Catch response data"""
        try:
            response_data = data.json()
            return response_data
        except:
            return data.text

    def send_request(self, req_type: str, url: str, params=None, data=None):
        try:
            response =  self.session.request(req_type,
                                             url,
                                             headers=self.session.headers,
                                             params=params,
                                             data=dumps(data))
            response_data = self.response_data_catch(response)
            return response_data
        except HTTPError as http_err:
            error_message = f"{url} -> HTTP error occurred: {http_err}"
            my_logger.error(error_message)
        except Exception as err:
            error_message = f"{__name__} -> Other error occurred: {err}"
            my_logger.error(error_message,exc_info=True)

    def post(self,method, data):
        """Send POST request."""
        url = self.set_request_url(method)
        response_data = self.send_request("POST", url,data=data)
        return response_data


    def get(self,method, data):
        """Send GET request."""
        url = self.set_request_url(method)
        response_data = self.send_request("GET", url)
        return response_data