"""Init web server with api plugin"""

from flask import Flask
from flask_cors import CORS
from waitress import serve

from api_extension import swagger
from env.default_env import DEBUG_MODE
from utils.common_utils import clear_temp_data

# from werkzeug.middleware.proxy_fix import ProxyFix


clear_temp_data()

app = Flask(__name__)
swagger.init_app(app)
# app.wsgi_app = ProxyFix(app.wsgi_app)
cors = CORS(app)  # allow CORS for all domains on all routes.

app.config["CORS_HEADERS"] = "Content-Type"
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False


if __name__ == "__main__":
    if DEBUG_MODE:
        app.run("0.0.0.0", debug=True, port=5555)
    else:
        serve(app, host="0.0.0.0", port=5555)
