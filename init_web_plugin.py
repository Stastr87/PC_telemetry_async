"""Init web server with api plugin"""

from flask import Flask
from flask_cors import CORS
from waitress import serve

from api_extension import swagger
from env.default_env import API_HOST, API_PORT, DEBUG_MODE, DOCKER_MODE
from utils.common_utils import TestThread
from utils.key_input import key_for_exit
from utils.logger.common_logger import common_logger
from utils.temp_file_remover_daemon import file_remover

app = Flask(__name__)
swagger.init_app(app)
cors = CORS(app)  # allow CORS for all domains on all routes.
app.config["CORS_HEADERS"] = "Content-Type"
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False


def start_flask_app():
    """Start debug app"""
    app.run(API_HOST, debug=False, port=API_PORT)


def wsgi_server():
    """start wsgi server"""
    serve(app, host=API_HOST, port=API_PORT)


if __name__ == "__main__":
    if DEBUG_MODE:
        start_flask_app()

    elif DOCKER_MODE:
        common_logger.warning("DOCKER_MODE is active")
        wsgi_server_thread = TestThread(
            "wsgi_server", wsgi_server, hello_msg=f"{API_HOST}:{API_PORT}"
        )
        wsgi_server_thread.start()

    else:
        quit_thread = TestThread(
            "key_for_exit", key_for_exit, hello_msg="Press ESC for exit"
        )
        quit_thread.start()

        wsgi_server_thread = TestThread(
            "wsgi_server", wsgi_server, daemon=True, hello_msg=f"{API_HOST}:{API_PORT}"
        )
        wsgi_server_thread.start()

    file_remover_t = TestThread("file_remover", file_remover, daemon=True)
    file_remover_t.start()
