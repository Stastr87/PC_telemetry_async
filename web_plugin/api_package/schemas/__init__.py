"""Define schemas in self doc service swagger"""

from flask_restx import fields

RETURN_HW_DATA_SCHEMA_POST = {
    "start_time": fields.String(),
    "end_time": fields.String(),
}

COMMON_RETURN_SCHEMA = {
    "message": fields.String(),
    "error": fields.Boolean(),
    "data": fields.Raw(),
}


STOP_TELEMETRY_COLLECTION_SCHEMA_GET = {
    "message": fields.String(),
    "error": fields.Boolean(),
}

RUN_TELEMETRY_COLLECTION_SCHEMA_GET = {
    "message": fields.String(),
    "error": fields.Boolean(),
    "data": fields.Integer(),
}

ERROR_SCHEMA_RESPONSE = {"message": fields.String(), "error": fields.Boolean()}

PERIOD_REQUEST_DATA = {"start_time": fields.String(), "end_time": fields.String()}
