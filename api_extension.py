
from flask_restx import Api

from web_plugin.api_package.telemetry_ns import telemetry_ns
from web_plugin.api_package.software_ns import soft_ns

swagger = Api(version='1.0', title="PC telemetry API", description="swagger doc service", doc='/swagger')
swagger.add_namespace(telemetry_ns, path='/api/v1')
swagger.add_namespace(soft_ns, path='/api/v1')