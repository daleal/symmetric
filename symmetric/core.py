"""
The main module of symmetric.
"""

import os
import bisect
import logging.config
import flask

import symmetric.endpoints


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


# Create flask app object
app = flask.Flask(__name__)


from symmetric.helpers import verb, humanize, log_request


class Symmetric:

    """
    Main class to encapsulate every important feature of the symmetric package.
    """

    # Define allowed HTTP methods
    __allowed_methods = [
        "OPTIONS",
        "GET",
        "HEAD",
        "POST",
        "PUT",
        "DELETE",
        "TRACE"
    ]

    def __init__(self, app_object):
        self.__app = app_object
        self.__endpoints = []

    def __call__(self, *args, **kwargs):
        """
        Enable WSGI servers to start with CLI utilities
        (like gunicorn module:symmetric).
        """
        return self.__app.__call__(*args, **kwargs)

    def router(self, route, methods=["get"], response_code=200):
        """
        Decorator modifier. Recieves a route string, a list of HTTP methods and
        a response code. If the route does not start with '/', it gets added.
        HTTP methods are also filtered. Returns the final decorated function.
        """
        route = f"/{route}" if route[0] != "/" else route
        methods = [
            verb(x) for x in methods
            if verb(x) in Symmetric.__allowed_methods
        ]

        def decorator(function):
            """
            Function decorator. Recieves the main function and wraps it as a
            flask endpoint. Returns the wrapped function.
            """
            # Save endpoint
            self.__save_endpoint(
                symmetric.endpoints.Endpoint(
                    route, methods, response_code, function
                )
            )

            # Decorate the wrapper
            @self.__app.route(
                route, methods=methods, endpoint=function.__name__
            )
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
                    self.__app.logger.error(
                        f"[[symmetric]] exception caught: {err}"
                    )
                    return flask.jsonify({}), 500
            return wrapper
        return decorator

    def run(self, *args, **kwargs):
        """Executes the main run function of the Flask object."""
        self.__app.run(*args, **kwargs)

    def generate_documentation(self, module_name):
        """
        Gets the documentation of every endpoint and assembles it into a
        markdown formatted string.
        """
        raw_docs = [x.generate_documentation() for x in self.__endpoints]
        docs = f"# {humanize(module_name)} API Documentation\n\n"
        docs += "\n".join(raw_docs)
        return docs

    def __save_endpoint(self, endpoint):
        """Saves an endpoint object and sorts the endpoints list."""
        bisect.insort(self.__endpoints, endpoint)


# Create symmetric object
sym = Symmetric(app)
