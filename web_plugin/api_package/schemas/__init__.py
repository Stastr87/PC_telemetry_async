"""Define schemas in self doc service swagger"""

from flask_restx import fields

COMMON_DATA_RETURN_SCHEMA = {
    "message": fields.String(),
    "error": fields.Boolean(),
    "data": fields.Raw(),
}


COMMON_RETURN_SCHEMA = {
    "message": fields.String(),
    "error": fields.Boolean(),
}

RUN_TELEMETRY_COLLECTION_SCHEMA_GET = {
    "message": fields.String(),
    "error": fields.Boolean(),
    "data": fields.Integer(),
}

PERIOD_REQUEST_DATA = {"start_time": fields.String(), "end_time": fields.String()}
