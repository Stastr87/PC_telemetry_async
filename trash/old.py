import subprocess
from datetime import datetime
from os import mkdir

import psutil
from flask import request
from flask_restx import Resource, Namespace
from flask_cors import cross_origin
from flask import abort


from api_extension import swagger
from stored_data_operation import DataObject
from web_plugin.api_package.schemas import RETURN_HW_DATA_SCHEMA_POST, COMMON_RESPONSE_SCHEMA, ERROR_RESPONSE_SCHEMA, \
    STOP_TELEMETRY_COLLECTION_POST

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


@swagger.route("/return_hw_data", endpoint="/return_hw_data")
class ReturnHWData(Resource):
    """Get hardware usage data
    """
    @swagger.doc('return_hw_data - info field')
    @cross_origin()
    @swagger.expect(RETURN_HW_DATA_SCHEMA_POST)
    @swagger.marshal_with(COMMON_RESPONSE_SCHEMA)
    def post(self):
        """Получение данных о телеметрии ПК за указанный период времени
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
            abort(400, f"ValueError {str(val_err)}")


        try:
            tab = DataObject(start, end)
            return_data = tab.get_csv_data()
            return_body = {"message":"OK","error":None,"data":return_data}
            return return_body, 200
        except Exception as err:
            my_logger.error(f"{request.url} (POST) error: \n{err}")
            abort(400, f"Another problem occurred: {str(err)}")


@swagger.route("/run_telemetry_collection", endpoint="/run_telemetry_collection")
class RunTelemetryCollection(Resource):
    """Start collecting telemetry data
    """
    @swagger.doc('run_telemetry_collection - info field')
    # @api_instance.marshal_with(COMMON_RESPONSE_SCHEMA)
    @cross_origin()
    def get(self):
        """Запуск модуля сбора телеметрии ПК
        """
        # Перенести в конфиг
        path_to_python_exe = "C:\\.venv\\python312\\Scripts\\python.exe"

        proc = subprocess.Popen([path_to_python_exe, 'save_telemetry_data.py'],
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
                abort(400, error_msg)

        except subprocess.TimeoutExpired as timeout_err:
            return {"message": "OK", "error": str(timeout_err), "data": return_data}, 201

        except Exception as err:
            abort(400, str(err))

@swagger.route("/stop_telemetry_collection", endpoint="/stop_telemetry_collection")
class StopTelemetryCollection(Resource):
    @swagger.doc('stop_telemetry_collection - info field')
    @cross_origin()
    def get(self):
        pid = None
        temp_file = os.path.join('tempdir','pid.txt')

        if os.path.isfile(temp_file):
            with open(temp_file, 'r') as pidfile:
                pid = int(pidfile.read())
        else:
            return {"message": "fail", "error": "Запись телеметрии не осуществляется"}, 200
        if psutil.pid_exists(pid):
            try:
                # Закрываем процесс
                p = psutil.Process(pid)
                p.terminate()
                # Удаляем временный файл
                os.remove(os.path.join('tempdir','pid.txt'))
                return {"message": f"process pid {pid} terminated", "error": None}, 200
            except Exception as err:
                abort(400, str(err))
        else:
            return {"message": "fail", "error": "Запись телеметрии не осуществляется"}, 200





