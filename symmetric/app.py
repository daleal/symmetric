"""
The main module of symmetric.
"""

import os
import json
import flask
import logging.config


# Logging configuration
logging.config.dictConfig({
    "version": 1,
    "formatters": {
        "console": {
            "format": "[%(asctime)s] [%(levelname)s] %(module)s: %(message)s"
        },
        "file": {
            "format": ("[%(asctime)s] [%(levelname)s] %(pathname)s - "
                       "line %(lineno)d: \n%(message)s\n")
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "formatter": "console"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": os.getenv("LOG_FILE", default="module.log"),
            "formatter": "file"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    }
})


# Define allowed HTTP methods
ALLOWED_METHODS = [
    "OPTIONS",
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "TRACE"
]


# Create flask app object
app = flask.Flask(__name__)


from .helpers import verb, log_request


def router(route, methods=["get"], response_code=200):
    """
    Decorator modifier. Recieves a route string, a list of HTTP methods and
    a response code. If the route does not start with '/', it gets added.
    HTTP methods are also filtered. Returns the final decorated function.
    """
    route = f"/{route}" if route[0] != "/" else route
    methods = [verb(x) for x in methods if verb(x) in ALLOWED_METHODS]

    def decorator(function):
        """
        Function decorator. Recieves the main function and wraps it as a
        flask endpoint. Returns the wrapped function.
        """
        @app.route(route, methods=methods, endpoint=function.__name__)
        def wrapper(*args, **kwargs):
            """
            Function wrapper. The main function gets logged, the JSON body
            gets extracted from the request and gets unpacked as **kwargs
            to pass to the main function. Some precautions are also taken
            (namely a try/except combo). Returns the function's output
            jsonified with a response code.
            """
            try:
                log_request(flask.request, route, function)
                body = flask.request.get_json()
                if not body:
                    body = {}
                return flask.jsonify(function(**body)), response_code
            except Exception as err:
                app.logger.error(f"[[symmetric]] exception caught: {err}")
                return flask.jsonify({}), 500
        return wrapper
    return decorator
