"""Init web server with api plugin"""

import threading

from flask import Flask
from flask_cors import CORS
from waitress import serve

from api_extension import swagger
from env.default_env import API_HOST, API_PORT, DEBUG_MODE
from temp_file_remover_daemon import file_remover

app = Flask(__name__)
swagger.init_app(app)
cors = CORS(app)  # allow CORS for all domains on all routes.
app.config["CORS_HEADERS"] = "Content-Type"
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False


def start_flask_app():
    """Start debug app"""
    app.run(API_HOST, debug=False, port=API_PORT)


def start_wsgi_server():
    """Start deploy app"""
    print(f"wsgi server started on {API_HOST}:{API_PORT}")
    serve(app, host=API_HOST, port=API_PORT)


if __name__ == "__main__":
    if DEBUG_MODE:
        start_flask_app()
    else:
        wsgi_server_thread = threading.Thread(target=start_wsgi_server)
        wsgi_server_thread.start()

    file_remover_t = threading.Thread(target=file_remover)
    file_remover_t.daemon = True
    file_remover_t.start()
