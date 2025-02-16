import json


import tempfile
import subprocess
from datetime import datetime
from os import mkdir

import psutil
from flask import request, send_file
from flask_restx import Resource, Namespace
from flask_cors import cross_origin

from env.default_env import PATH_TO_PYTHON_EXE, LOG_DIR
from stored_data_operation import DataObject
from utils.file_remover import FileRemover

from web_plugin.api_package.schemas import RUN_TELEMETRY_COLLECTION_SCHEMA_GET, STOP_TELEMETRY_COLLECTION_SCHEMA_GET, \
    PERIOD_REQUEST_DATA, COMMON_RETURN_SCHEMA

import os
import sys
new_work_dir = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.append(new_work_dir)

from utils.custom_logger import CustomLogger

log_file_name = "telemetry_ns.log"
logger_instance = CustomLogger(logger_name="telemetry_ns",
                                dt_fmt='%H:%M:%S',
                                file_path=os.path.join(new_work_dir,LOG_DIR,log_file_name),
                                level="debug")
my_logger = logger_instance.logger

telemetry_ns = Namespace('telemetry', description='access to host telemetry data')


@telemetry_ns.route("/cpu_usage_to_json")
@telemetry_ns.doc(params={"start_time":{"description":"start of request period",
                                        "type": "str"},
                          "end_time":{"description":"end of request period",
                                      "type": "str"}})
class CPUUsageToJson(Resource):
    """return json file contained cpu usage data with query in params"""
    #TODO Удалять временный файл после отправки по запросу
    @cross_origin()
    @telemetry_ns.doc('return json file contained cpu usage data')
    # @telemetry_ns.expect(telemetry_ns.model('cpu_usage_data_post', PERIOD_REQUEST_DATA))
    # @telemetry_ns.marshal_with(telemetry_ns.model('cpu_usage_schema', RAW_DATA_SCHEMA))
    def get(self):
        start = request.args.get('start_time')
        end = request.args.get('end_time')

        try:
            if datetime.fromisoformat(start)>datetime.fromisoformat(end):
                raise ValueError("Время начала периода позже его окончания")
        except ValueError as val_err:
            my_logger.error(f"{request.url} (POST) ValueError: \n{val_err}")
            telemetry_ns.abort(400, f"ValueError {str(val_err)}")
        try:
            df = DataObject(start, end)
            return_data = df.get_cpu_usage()
            tempdir = tempfile.mkdtemp()
            fp = tempfile.NamedTemporaryFile(mode='w+t',
                                             suffix='.json',
                                             delete = False,
                                             dir=tempdir)
            fp.write(json.dumps(return_data))

            resp = send_file(fp.name, as_attachment=True)
            file_remover = FileRemover()
            fp.close()
            file_remover.cleanup_once_done(resp, tempdir)
            return resp, 200

        except Exception as err:
            my_logger.error(f"{request.url} (POST) error: \n{err}")
            telemetry_ns.abort(400, f"Another problem occurred: {str(err)}")


@telemetry_ns.route("/cpu_usage")
@telemetry_ns.doc(params={"start_time":{"description":"start of request period",
                                        "type": "str"},
                          "end_time":{"description":"end of request period",
                                      "type": "str"}})
class CPUUsage(Resource):
    """return cpu usage data with query in params"""
    @cross_origin()
    @telemetry_ns.doc('return cpu usage data')
    # @telemetry_ns.expect(telemetry_ns.model('cpu_usage_data_post', PERIOD_REQUEST_DATA))
    # @telemetry_ns.marshal_with(telemetry_ns.model('cpu_usage_schema', RAW_DATA_SCHEMA))
    def get(self):
        start = request.args.get('start_time')
        end = request.args.get('end_time')

        try:
            if datetime.fromisoformat(start)>datetime.fromisoformat(end):
                raise ValueError("Время начала периода позже его окончания")
        except ValueError as val_err:
            my_logger.error(f"{request.url} (POST) ValueError: \n{val_err}")
            telemetry_ns.abort(400, f"ValueError {str(val_err)}")
        try:
            df = DataObject(start, end)
            return_data = df.get_cpu_usage()
            return_body = return_data
            return return_body, 200
        except Exception as err:
            my_logger.error(f"{request.url} (POST) error: \n{err}")
            telemetry_ns.abort(400, f"Another problem occurred: {str(err)}")



@telemetry_ns.route("/cpu_usage_data")
class CPUUsageData(Resource):
    """return cpu usage data
    """
    @cross_origin()
    @telemetry_ns.doc('return cpu usage data')
    @telemetry_ns.expect(telemetry_ns.model('cpu_usage_data_post',PERIOD_REQUEST_DATA))
    @telemetry_ns.marshal_with(telemetry_ns.model('cpu_usage_data_response_schema', COMMON_RETURN_SCHEMA))
    def post(self):
        """Return cpu usage data for requested period
        """
        request_data = request.get_json()
        my_logger.debug(f"request_data: \n{request_data}")
        start = request_data.get("start_time")
        end = request_data.get("end_time")

        try:
            if datetime.fromisoformat(start)>datetime.fromisoformat(end):
                raise ValueError("Время начала периода позже его окончания")
        except ValueError as val_err:
            my_logger.error(f"{request.url} (POST) ValueError: \n{val_err}")
            telemetry_ns.abort(400, f"ValueError {str(val_err)}")

        try:

            df = DataObject(start, end)
            return_data = df.get_cpu_usage()


            return_body = {"message":"OK","error":False,"data":return_data}
            return return_body, 200
        except Exception as err:
            my_logger.error(f"{request.url} (POST) error: \n{err}")
            telemetry_ns.abort(400, f"Another problem occurred: {str(err)}")


@telemetry_ns.route("/return_hw_data")
class ReturnHWData(Resource):
    """Get hardware usage data
    """
    @cross_origin()
    @telemetry_ns.doc('return_hw_data - info field')
    @telemetry_ns.expect(telemetry_ns.model('return_hw_data_schema_post',PERIOD_REQUEST_DATA))
    @telemetry_ns.marshal_with(telemetry_ns.model('return_hw_data_schema_schema_response', COMMON_RETURN_SCHEMA))
    def post(self):
        """Get hardware usage data for requested period
        """
        request_data = request.get_json()
        my_logger.debug(f"request_data: \n{request_data}")
        start = request_data.get("start_time")
        end = request_data.get("end_time")

        try:
            if datetime.fromisoformat(start)>datetime.fromisoformat(end):
                raise ValueError("Время начала периода позже его окончания")
        except ValueError as val_err:
            my_logger.error(f"{request.url} (POST) ValueError: \n{val_err}")
            telemetry_ns.abort(400, f"ValueError {str(val_err)}")

        try:
            tab = DataObject(start, end)
            return_data = tab.get_csv_data()
            return_body = {"message":"OK","error":False,"data":return_data}
            return return_body, 200
        except Exception as err:
            my_logger.error(f"{request.url} (POST) error: \n{err}")
            telemetry_ns.abort(400, f"Another problem occurred: {str(err)}")


@telemetry_ns.route("/run_telemetry_collection")
class RunTelemetryCollection(Resource):
    """Start collecting telemetry data
    """
    @cross_origin()
    @telemetry_ns.doc('run_telemetry_collection - info field')
    @telemetry_ns.marshal_with(telemetry_ns.model('run_telemetry_collection_schema_get',
                                                   RUN_TELEMETRY_COLLECTION_SCHEMA_GET))
    def get(self):
        """starting collecting telemetry data
        """
        python_path = os.path.join('C:\\', '.venv', 'python312', 'Scripts', 'python.exe')
        my_logger.debug(python_path)
        proc = subprocess.Popen([python_path, 'save_telemetry_data.py'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        my_logger.debug(f"{__class__} -> get() -> proc.pid: \n{proc.pid}")
        return_data = proc.pid

        # сохранить pid процесса, для последующего его закрытия
        if not os.path.isdir('tempdir'):
            mkdir('tempdir')
        with open(os.path.join('tempdir','pid.txt'), 'w') as pidfile:
            pidfile.write(str(return_data))

        try:
            stdout, stderr = proc.communicate(timeout=5)
            my_logger.debug(f"{__class__} -> get() -> stdout: \n{stdout}")
            if proc.stderr:
                # handle error
                error_msg = proc.stderr
                my_logger.debug(f"{__class__} -> get() -> error_msg: \n{error_msg}")
                telemetry_ns.abort(400, error_msg)

        except subprocess.TimeoutExpired:
            return_body = {"message":"collecting telemetry data started","error": False,"data": return_data}
            return return_body, 201

        except Exception as err:
            telemetry_ns.abort(400, str(err))



@telemetry_ns.route("/stop_telemetry_collection")
class StopTelemetryCollection(Resource):
    """StopTelemetryCollection"""
    @cross_origin()
    @telemetry_ns.doc('stop_telemetry_collection - info field')
    @telemetry_ns.marshal_with(telemetry_ns.model('stop_telemetry_collection_schema_get', STOP_TELEMETRY_COLLECTION_SCHEMA_GET))
    def get(self):
        """stop collecting hardware usage data"""
        temp_file = os.path.join('tempdir','pid.txt')

        if os.path.isfile(temp_file):
            with open(temp_file, 'r') as pidfile:
                pid = int(pidfile.read())
        else:
            return_body = {"message": "process not exist", "error": True}
            return return_body, 200
        if psutil.pid_exists(pid):
            try:
                # Закрываем процесс
                p = psutil.Process(pid)
                p.terminate()
                # Удаляем временный файл
                os.remove(os.path.join('tempdir','pid.txt'))
                return_body = {"message": f"process pid {pid} terminated", "error": False}
                return return_body, 200
            except Exception as err:
                telemetry_ns.abort(400, str(err))
        else:
            return_body = {"message":"process not exist","error":True}
            return return_body, 204





