"""Define telemetry section in self doc service swagger"""

import json
import os
import subprocess
import tempfile
from datetime import datetime, timedelta
from os import mkdir
from sys import path, platform

import psutil
from flask import request, send_file
from flask_cors import cross_origin
from flask_restx import Namespace, Resource

from env.default_env import (
    DOCKER_MODE,
    LOG_DIR,
    NEW_WORK_DIR,
    PATH_TO_PYTHON_EXE,
    PATH_TO_PYTHON_LINUX,
    RESPONSE_TEMP_DIR,
)
from stored_data_operation import DataObject
from utils.custom_logger import CustomLogger
from web_plugin.api_package.schemas import (
    COMMON_RETURN_SCHEMA,
    PERIOD_REQUEST_DATA,
    RUN_TELEMETRY_COLLECTION_SCHEMA_GET,
    STOP_TELEMETRY_COLLECTION_SCHEMA_GET,
)

path.append(NEW_WORK_DIR)

LOG_FILE_NAME = "telemetry_ns.log"
logger_instance = CustomLogger(
    logger_name="telemetry_ns",
    file_path=os.path.join(LOG_DIR, LOG_FILE_NAME),
    level="debug",
)
my_logger = logger_instance.logger


def get_python_path():
    """return python path according OS type"""
    python_path = None
    if DOCKER_MODE:
        raise ValueError()

    if platform in ("linux", "linux2"):
        # Linux OS
        python_path = PATH_TO_PYTHON_LINUX
    if platform == "darwin":
        # MacOS
        python_path = PATH_TO_PYTHON_LINUX
    if platform == "win32":
        # Windows
        python_path = PATH_TO_PYTHON_EXE

    return python_path


def get_temp_file():
    """Return temp file object"""
    if os.path.isdir(RESPONSE_TEMP_DIR):
        mkdir(RESPONSE_TEMP_DIR)
    fldr, file_name = tempfile.mkstemp(".json", text=True, dir=RESPONSE_TEMP_DIR)
    return fldr, file_name


telemetry_ns = Namespace("telemetry", description="access to host telemetry data")


@telemetry_ns.route("/ram_usage_to_json")
@telemetry_ns.doc(
    params={
        "start_time": {"description": "start of request period", "type": "str"},
        "end_time": {"description": "end of request period", "type": "str"},
    }
)
class RAMUsageToJson(Resource):
    """return json file contained ram usage data with query in params"""

    @cross_origin()
    @telemetry_ns.doc("return json file contained ram usage data")
    # @temp_file_must_be_clean
    def get(self):
        """Define GET response"""
        start = request.args.get("start_time")
        end = request.args.get("end_time")

        if not start or not end:
            start = datetime.now() - timedelta(days=1)
            end = datetime.now()
            start = start.isoformat()
            end = end.isoformat()

        try:
            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                raise ValueError("Время начала периода позже его окончания")

        except ValueError as val_err:
            my_logger.error("%s ValueError: \n%s", request.url, val_err)
            telemetry_ns.abort(400, f"ValueError {str(val_err)}")

        try:

            df = DataObject(start, end)
            return_data = df.get_ram_usage()

            if not return_data:
                raise ValueError("Empty data")

            my_logger.debug(
                "%s return_data is :>>>>\n%s\n...\n%s",
                __class__,
                json.dumps(return_data)[:40],
                json.dumps(return_data)[-40:],
            )

            fd, temp_file = get_temp_file()

            with open(temp_file, "w", encoding="utf8") as fpw:
                fpw.write(json.dumps(return_data))

            os.close(fd)

            return send_file(temp_file, as_attachment=True), 200

        except OSError as err:
            my_logger.error("%s error: \n%s", request.url, err, exc_info=True)
            telemetry_ns.abort(400, f"OSError problem occurred: {str(err)}")

        except ValueError as err:
            my_logger.error("%s error: \n%s", request.url, err, exc_info=True)
            return 204


@telemetry_ns.route("/cpu_usage_to_json")
@telemetry_ns.doc(
    params={
        "start_time": {"description": "start of request period", "type": "str"},
        "end_time": {"description": "end of request period", "type": "str"},
    }
)
class CPUUsageToJson(Resource):
    """return json file contained cpu usage data with query in params"""

    @cross_origin()
    @telemetry_ns.doc("return json file contained cpu usage data")
    # @temp_file_must_be_clean
    def get(self):
        """Define GET response"""
        start = request.args.get("start_time")
        end = request.args.get("end_time")

        if not start or end:
            start = datetime.now() - timedelta(days=2)
            start = start.isoformat()
            end = datetime.now().isoformat()

        try:
            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                raise ValueError("Время начала периода позже его окончания")
        except ValueError as val_err:
            my_logger.error("%s ValueError: \n%s", request.url, val_err)
            telemetry_ns.abort(400, f"ValueError {str(val_err)}")

        try:
            df = DataObject(start, end)
            return_data = df.get_cpu_usage()
            fd, temp_file = get_temp_file()

            my_logger.debug(
                "%s return_data is :>>>>\n%s\n...\n,%s",
                __class__,
                json.dumps(return_data)[:40],
                json.dumps(return_data)[-40:],
            )

            with open(temp_file, "w") as fpw:
                fpw.write(json.dumps(return_data))

            return send_file(temp_file, as_attachment=True), 200

        except ValueError as err:
            my_logger.error("%s error: \n%s", request.url, err, exc_info=True)
            return 204


@telemetry_ns.route("/cpu_usage")
@telemetry_ns.doc(
    params={
        "start_time": {"description": "start of request period", "type": "str"},
        "end_time": {"description": "end of request period", "type": "str"},
    }
)
class CPUUsage(Resource):
    """return cpu usage data with query in params"""

    @cross_origin()
    @telemetry_ns.doc("return cpu usage data")
    def get(self):
        """Define GET return"""
        start = request.args.get("start_time")
        end = request.args.get("end_time")

        try:
            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                raise ValueError("Время начала периода позже его окончания")
        except ValueError as val_err:
            my_logger.error(f"{request.url} ValueError: \n{val_err}")
            telemetry_ns.abort(400, f"ValueError {str(val_err)}")
        try:
            df = DataObject(start, end)
            return_data = df.get_cpu_usage()
            return_body = return_data
            return return_body, 200
        except Exception as err:
            my_logger.error(f"{request.url} error: \n{err}")
            telemetry_ns.abort(400, f"Another problem occurred: {str(err)}")


@telemetry_ns.route("/cpu_usage_data")
class CPUUsageData(Resource):
    """return cpu usage data"""

    @cross_origin()
    @telemetry_ns.doc("return cpu usage data")
    @telemetry_ns.expect(telemetry_ns.model("cpu_usage_data_post", PERIOD_REQUEST_DATA))
    @telemetry_ns.marshal_with(
        telemetry_ns.model("cpu_usage_data_response_schema", COMMON_RETURN_SCHEMA)
    )
    def post(self):
        """Return cpu usage data for requested period"""
        request_data = request.get_json()
        my_logger.debug(f"request_data: \n{request_data}")
        start = request_data.get("start_time")
        end = request_data.get("end_time")

        try:
            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                raise ValueError("Время начала периода позже его окончания")
        except ValueError as val_err:
            my_logger.error(f"{request.url} (POST) ValueError: \n{val_err}")
            telemetry_ns.abort(400, f"ValueError {str(val_err)}")

        try:

            df = DataObject(start, end)
            return_data = df.get_cpu_usage()

            return_body = {"message": "OK", "error": False, "data": return_data}
            return return_body, 200
        except Exception as err:
            my_logger.error(f"{request.url} (POST) error: \n{err}")
            telemetry_ns.abort(400, f"Another problem occurred: {str(err)}")


@telemetry_ns.route("/return_hw_data")
class ReturnHWData(Resource):
    """Get hardware usage data"""

    @cross_origin()
    @telemetry_ns.doc("return_hw_data - info field")
    @telemetry_ns.expect(
        telemetry_ns.model("return_hw_data_schema_post", PERIOD_REQUEST_DATA)
    )
    @telemetry_ns.marshal_with(
        telemetry_ns.model(
            "return_hw_data_schema_schema_response", COMMON_RETURN_SCHEMA
        )
    )
    def post(self):
        """Get hardware usage data for requested period"""
        request_data = request.get_json()
        my_logger.debug(f"request_data: \n{request_data}")
        start = request_data.get("start_time")
        end = request_data.get("end_time")

        try:
            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                raise ValueError("Время начала периода позже его окончания")
        except ValueError as val_err:
            my_logger.error(f"{request.url} (POST) ValueError: \n{val_err}")
            telemetry_ns.abort(400, f"ValueError {str(val_err)}")

        try:
            tab = DataObject(start, end)
            return_data = tab.get_csv_data()
            return_body = {"message": "OK", "error": False, "data": return_data}
            return return_body, 200
        except Exception as err:
            my_logger.error(f"{request.url} (POST) error: \n{err}")
            telemetry_ns.abort(400, f"Another problem occurred: {str(err)}")


@telemetry_ns.route("/run_telemetry_collection")
class RunTelemetryCollection(Resource):
    """Start collecting telemetry data"""

    @cross_origin()
    @telemetry_ns.doc("run_telemetry_collection - info field")
    @telemetry_ns.marshal_with(
        telemetry_ns.model(
            "run_telemetry_collection_schema_get", RUN_TELEMETRY_COLLECTION_SCHEMA_GET
        )
    )
    def get(self):
        """starting collecting telemetry data"""
        try:
            python_path = get_python_path()
        except ValueError:
            return_body = {
                "message": """Collecting telemetry data fail. \
                Docker mode enabled. \
                Use external telemetry collection lib""",
                "error": True,
                "data": None,
            }
            return return_body, 405

        my_logger.debug(python_path)
        proc = subprocess.Popen(
            [python_path, "save_telemetry_data.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        my_logger.debug(f"{__class__} -> get() -> proc.pid: \n{proc.pid}")
        return_data = proc.pid

        # сохранить pid процесса, для последующего его закрытия
        if not os.path.isdir("tempdir"):
            mkdir("tempdir")
        with open(os.path.join("tempdir", "pid.txt"), "w") as pidfile:
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
            return_body = {
                "message": "collecting telemetry data started",
                "error": False,
                "data": return_data,
            }
            return return_body, 201

        except Exception as err:
            telemetry_ns.abort(400, str(err))


@telemetry_ns.route("/stop_telemetry_collection")
class StopTelemetryCollection(Resource):
    """StopTelemetryCollection"""

    @cross_origin()
    @telemetry_ns.doc("stop_telemetry_collection - info field")
    @telemetry_ns.marshal_with(
        telemetry_ns.model(
            "stop_telemetry_collection_schema_get", STOP_TELEMETRY_COLLECTION_SCHEMA_GET
        )
    )
    def get(self):
        """stop collecting hardware usage data"""
        temp_file = os.path.join("tempdir", "pid.txt")

        if os.path.isfile(temp_file):
            with open(temp_file, "r") as pidfile:
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
                os.remove(os.path.join("tempdir", "pid.txt"))
                return_body = {
                    "message": f"process pid {pid} terminated",
                    "error": False,
                }
                return return_body, 200
            except Exception as err:
                telemetry_ns.abort(400, str(err))
        else:
            return_body = {"message": "process not exist", "error": True}
            return return_body, 204
