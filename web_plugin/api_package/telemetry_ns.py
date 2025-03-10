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
from utils.exceptions import UtilException
from web_plugin.api_package.schemas import (
    COMMON_DATA_RETURN_SCHEMA,
    COMMON_RETURN_SCHEMA,
    PERIOD_REQUEST_DATA,
    RUN_TELEMETRY_COLLECTION_SCHEMA_GET,
)

path.append(NEW_WORK_DIR)

LOG_FILE_NAME = "telemetry_ns.log"
logger_instance = CustomLogger(
    logger_name="telemetry_ns",
    file_path=os.path.join(LOG_DIR, LOG_FILE_NAME),
    level="debug",
)
my_logger = logger_instance.logger


def get_python_path() -> str:
    """return python path according OS type"""
    python_path = ""
    if DOCKER_MODE:
        return python_path
    if platform in ("linux", "linux2", "darwin"):
        # Linux, MacOS
        python_path = PATH_TO_PYTHON_LINUX
    if platform == "win32":
        # Windows
        python_path = PATH_TO_PYTHON_EXE

    return python_path


def get_temp_file() -> tuple:
    """Return temp file object"""
    if not os.path.isdir(RESPONSE_TEMP_DIR):
        mkdir(RESPONSE_TEMP_DIR)
    fldr, file_name = tempfile.mkstemp(".json", text=True, dir=RESPONSE_TEMP_DIR)
    return fldr, file_name


telemetry_ns = Namespace("telemetry", description="access to host telemetry data")


def error_handler(e, http_code: int = 400) -> tuple:
    """Catch error code for error response"""
    response_body = {"message": f"{type(e).__name__} handed! {e}", "error": True}

    if str(e) == "Empty data":
        http_code = 204

    return response_body, http_code


def get_pid() -> int:
    """Return process id from temp file"""
    pid = 0
    try:
        pid_file = os.path.join("tempdir", "pid.txt")

        with open(pid_file, "r", encoding="utf8") as file:
            pid = int(file.read())
    except OSError as err:
        my_logger.debug("No any pid file. %s", err)

    return pid

@telemetry_ns.route("/get_net_adapters")
@telemetry_ns.doc(
    params={
        "start_time": {"description": "start of request period", "type": "str"},
        "end_time": {"description": "end of request period", "type": "str"}
    }
)
class NetAdapters(Resource):
    """HTTP method described in self doc interface swagger"""
    #TODO Отловить случаи когда запрос возвращает ошибки
    @cross_origin()
    @telemetry_ns.doc("return list of net adapters")
    @telemetry_ns.marshal_with(
        telemetry_ns.model("common_data_return_schema", COMMON_DATA_RETURN_SCHEMA)
    )
    def get(self) -> tuple:
        """Return list of net adapters contained in local db"""
        start = request.args.get("start_time")
        end = request.args.get("end_time")

        if not start or not end:
            start_dt = datetime.now() - timedelta(days=1)
            end_dt = datetime.now()
            start = start_dt.isoformat()
            end = end_dt.isoformat()

        try:
            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                raise ValueError("Stop is early than Start")

            df = DataObject(start, end)
            return_data = df.get_net_adapter_list()

            if not return_data:
                raise ValueError("Empty data")


        except (ValueError, OSError) as err:
            return error_handler(err)

        return {"data":return_data, "error": False, "message":"OK"}, 200

@telemetry_ns.route("/net_adapter_usage")
@telemetry_ns.doc(
    params={
        "start_time": {"description": "start of request period", "type": "str"},
        "end_time": {"description": "end of request period", "type": "str"},
        "net_adapter_name": {"description": "stored net adapter name", "type": "str"}
    }
)
class NetAdapterUsage(Resource):
    """HTTP method described in self doc interface swagger"""
    # TODO отловить ошибки когда запрос возвращает ошибки
    @cross_origin()
    @telemetry_ns.doc("return json file contained net adapter usage data")
    def get(self) -> tuple:
        """Return json file contained net adapter usage data with query in params"""
        start = request.args.get("start_time")
        end = request.args.get("end_time")
        net_adapter_name = request.args.get("net_adapter_name")

        if not start or not end:
            start_dt = datetime.now() - timedelta(days=1)
            end_dt = datetime.now()
            start = start_dt.isoformat()
            end = end_dt.isoformat()

        try:
            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                raise ValueError("Stop is early than Start")

            df = DataObject(start, end, net_adapter_name)
            return_data = df.get_network_usage_data()

            if not return_data:
                raise ValueError("Empty data")

            fd, temp_file = get_temp_file()
            with open(temp_file, "w", encoding="utf8") as fpw:
                fpw.write(json.dumps(return_data))
            os.close(fd)

        except (ValueError, OSError) as err:
            return error_handler(err)

        return send_file(temp_file, as_attachment=True), 200


@telemetry_ns.route("/ram_usage_to_json")
@telemetry_ns.doc(
    params={
        "start_time": {"description": "start of request period", "type": "str"},
        "end_time": {"description": "end of request period", "type": "str"},
    }
)
class RAMUsageToJson(Resource):
    """HTTP method described in self doc interface swagger"""

    @cross_origin()
    @telemetry_ns.doc("return json file contained ram usage data")
    def get(self) -> tuple:
        """Return json file contained ram usage data with query in params"""
        start = request.args.get("start_time")
        end = request.args.get("end_time")

        if not start or not end:
            start_dt = datetime.now() - timedelta(days=1)
            end_dt = datetime.now()
            start = start_dt.isoformat()
            end = end_dt.isoformat()

        try:
            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                raise ValueError("Stop is early than Start")

            df = DataObject(start, end)
            return_data = df.get_ram_usage()

            if not return_data:
                raise ValueError("Empty data")

            fd, temp_file = get_temp_file()
            with open(temp_file, "w", encoding="utf8") as fpw:
                fpw.write(json.dumps(return_data))
            os.close(fd)

        except (ValueError, OSError) as err:
            return error_handler(err)

        return send_file(temp_file, as_attachment=True), 200


@telemetry_ns.route("/cpu_usage_to_json")
@telemetry_ns.doc(
    params={
        "start_time": {"description": "start of request period", "type": "str"},
        "end_time": {"description": "end of request period", "type": "str"},
    }
)
class CPUUsageToJson(Resource):
    """HTTP method described in self doc interface swagger"""

    @cross_origin()
    @telemetry_ns.doc("return json file contained cpu usage data")
    # @temp_file_must_be_clean
    def get(self) -> tuple:
        """Return json file contained cpu usage data with query in params"""
        start = request.args.get("start_time")
        end = request.args.get("end_time")

        if not start or not end:
            start_dt = datetime.now() - timedelta(days=1)
            end_dt = datetime.now()
            start = start_dt.isoformat()
            end = end_dt.isoformat()

        try:
            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                raise ValueError("Stop is early than Start")

            df = DataObject(start, end)
            return_data = df.get_cpu_usage()

            if not return_data:
                raise ValueError("Empty data")

            fd, temp_file = get_temp_file()
            with open(temp_file, "w", encoding="utf8") as fpw:
                fpw.write(json.dumps(return_data))
            os.close(fd)

        except (ValueError, OSError) as err:
            return error_handler(err)

        return send_file(temp_file, as_attachment=True), 200


@telemetry_ns.route("/cpu_usage")
@telemetry_ns.doc(
    params={
        "start_time": {"description": "start of request period", "type": "str"},
        "end_time": {"description": "end of request period", "type": "str"},
    }
)
class CPUUsage(Resource):
    """HTTP method described in self doc interface swagger"""

    @cross_origin()
    @telemetry_ns.doc("return cpu usage data")
    def get(self) -> tuple:
        """Return cpu usage data with query in params"""
        start = str(request.args.get("start_time"))
        end = str(request.args.get("end_time"))

        try:
            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                raise ValueError("Start older than End")

            df = DataObject(start, end)
            if not df.get_cpu_usage():
                raise ValueError("Empty data!")

            return_body = str(df.get_cpu_usage())

        except (ValueError, OSError) as err:
            return error_handler(err)

        return return_body, 200


@telemetry_ns.route("/cpu_usage_data")
class CPUUsageData(Resource):
    """HTTP method described in self doc interface swagger"""

    @cross_origin()
    @telemetry_ns.doc("return cpu usage data")
    @telemetry_ns.expect(telemetry_ns.model("period_request_data", PERIOD_REQUEST_DATA))
    @telemetry_ns.marshal_with(
        telemetry_ns.model("common_data_return_schema", COMMON_DATA_RETURN_SCHEMA)
    )
    def post(self) -> tuple:
        """Return cpu usage data for period."""
        request_data = request.get_json()
        my_logger.debug("request_data: \n%s", request_data)
        start = request_data.get("start_time")
        end = request_data.get("end_time")

        try:
            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                raise ValueError("Start older than End")

            df = DataObject(start, end)

            if not df.get_cpu_usage():
                raise ValueError("Empty data!")

            return_data = df.get_cpu_usage()
            return_body = {"message": "OK", "error": False, "data": return_data}

        except (ValueError, OSError) as err:
            return error_handler(err)

        return return_body, 200


@telemetry_ns.route("/csv_data")
class CSVData(Resource):
    """HTTP method described in self doc interface swagger"""

    @cross_origin()
    @telemetry_ns.doc("csv_data - info field")
    @telemetry_ns.expect(
        telemetry_ns.model("period_request_data", PERIOD_REQUEST_DATA)
    )
    @telemetry_ns.marshal_with(
        telemetry_ns.model("common_data_return_schema", COMMON_DATA_RETURN_SCHEMA)
    )
    def post(self) -> tuple:
        """Return  hardware usage CSV data for requested period."""
        request_data = request.get_json()
        my_logger.debug("request_data: \n%s", request_data)
        start = request_data.get("start_time")
        end = request_data.get("end_time")

        try:
            if datetime.fromisoformat(start) > datetime.fromisoformat(end):
                raise ValueError("Stop is early than Start")

            tab = DataObject(start, end)

            if not tab.get_csv_data():
                raise ValueError("Empty data!")

            return_body = {"message": "OK", "error": False, "data": tab.get_csv_data()}

        except ValueError as err:
            return error_handler(err)

        return return_body, 200


@telemetry_ns.route("/run_telemetry_collection")
class RunTelemetryCollection(Resource):
    """HTTP method described in self doc interface swagger"""

    @cross_origin()
    @telemetry_ns.doc("run_telemetry_collection - info field")
    @telemetry_ns.marshal_with(
        telemetry_ns.model(
            "run_telemetry_collection_schema_get", RUN_TELEMETRY_COLLECTION_SCHEMA_GET
        )
    )
    # доработать метод возвращающий результат запуска скрипта сохранения телеметрии
    # with subprocess.Popen() as proc:....
    # pylint: disable=R1732
    def get(self) -> tuple:
        """starting collecting telemetry data"""
        pid = get_pid()
        python_path = get_python_path()
        try:
            if pid != 0:
                raise ValueError("Telemetry process already exist")

            if not python_path:
                raise ValueError("Docker mode is enabled. Use external telemetry lib")

            if not os.path.isfile(python_path):
                raise FileNotFoundError("Python interpreter not found")

            proc = subprocess.Popen(
                [python_path, "save_telemetry_data.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            pid = proc.pid
            my_logger.debug("RunTelemetryCollection -> get() -> proc.pid: %s", pid)

            # сохранить pid процесса, для последующего его закрытия
            if not os.path.isdir("tempdir"):
                mkdir("tempdir")
            with open(
                os.path.join("tempdir", "pid.txt"), "w", encoding="utf8"
            ) as pidfile:
                pidfile.write(str(pid))

            stdout, stderr = proc.communicate(timeout=5)
            my_logger.debug("RunTelemetryCollection -> get() -> stdout: \n%s", stdout)
            if stderr:
                raise UtilException(stderr)

            return_body: dict[str, str | bool] = {}
            if not return_body:
                raise UtilException("Process start fail.")

        except subprocess.TimeoutExpired:
            return_body = {
                "message": "collecting telemetry data started",
                "error": False,
                "data": str(pid),
            }

        except (ValueError, UtilException, FileNotFoundError) as err:
            return error_handler(err)

        return return_body, 201


@telemetry_ns.route("/stop_telemetry_collection")
class StopTelemetryCollection(Resource):
    """HTTP method described in self doc interface swagger"""

    @cross_origin()
    @telemetry_ns.doc("stop_telemetry_collection - info field")
    @telemetry_ns.marshal_with(
        telemetry_ns.model("common_return_schema", COMMON_RETURN_SCHEMA)
    )
    def get(self) -> tuple:
        """stop collecting hardware usage data"""
        try:
            pid = get_pid()
            if pid == 0:
                return {"message": "pid file not found", "error": True}, 200

            if not psutil.pid_exists(pid):
                raise OSError(f"Process {pid} not exist")

            # kill process
            p = psutil.Process(pid)
            p.terminate()
            # ...and delete temp file
            os.remove(os.path.join("tempdir", "pid.txt"))
            return_body = {
                "message": f"process pid {pid} terminated",
                "error": False,
            }

        except OSError as err:
            return error_handler(err)

        return return_body, 200
