"""Init web server with api plugin"""

from flask import Flask
from flask_cors import CORS
from waitress import serve

from api_extension import swagger
from env.default_env import DEBUG_MODE, API_PORT, API_HOST
from utils.common_utils import clear_temp_data

clear_temp_data()

app = Flask(__name__)
swagger.init_app(app)

cors = CORS(app)  # allow CORS for all domains on all routes.

app.config["CORS_HEADERS"] = "Content-Type"
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False


if __name__ == "__main__":
    if DEBUG_MODE:
        app.run(API_HOST, debug=True, port=API_PORT)
    else:
        serve(app, host=API_HOST, port=API_PORT)
