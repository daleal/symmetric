"""
The main module of symmetric.
"""

import os
import sys
import json
import bisect
import logging.config
import flask

import symmetric.constants
import symmetric.endpoints
import symmetric.helpers
import symmetric.errors


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
        self.__server_token_name = symmetric.constants.API_SERVER_TOKEN_NAME
        self.__client_token_name = symmetric.constants.API_CLIENT_TOKEN_NAME

    def __call__(self, *args, **kwargs):
        """
        Enable WSGI servers to start with CLI utilities
        (like gunicorn module:symmetric).
        """
        return self.__app.__call__(*args, **kwargs)

    def router(self, route, methods=["get"], response_code=200,
               auth_token=False):
        """
        Decorator modifier. Recieves a route string, a list of HTTP methods, a
        response code and a boolean indicating whether or not to authenticate.
        If the route does not start with '/', it gets added. HTTP methods are
        also filtered. Returns the final decorated function.
        """
        try:
            symmetric.helpers.parse_url(route)
        except symmetric.errors.IncorrectURLFormatError as err:
            self.__app.logger.error(
                f"[[symmetric]] IncorrectURLFormatError: {err}"
            )
            sys.exit(1)

        methods = [
            symmetric.helpers.verb(x) for x in methods
            if symmetric.helpers.verb(x) in Symmetric.__allowed_methods
        ]

        def decorator(function):
            """
            Function decorator. Recieves the main function and wraps it as a
            flask endpoint. Returns the wrapped function.
            """
            try:
                self.__save_endpoint(
                    symmetric.endpoints.Endpoint(
                        route, methods, response_code, function, auth_token
                    )
                )
            except symmetric.errors.DuplicatedURLError as err:
                self.__app.logger.error(
                    f"[[symmetric]] DuplicatedURLError: {err}"
                )
                sys.exit(1)

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
                    self.__log_request(flask.request, route, function)

                    # Get the body
                    body = flask.request.get_json()
                    if not body:
                        body = {}

                    # Check for token authentication
                    symmetric.helpers.authenticate(
                        body, auth_token, self.__client_token_name,
                        self.__server_token_name)

                    # Filter method parameters
                    parameters = symmetric.helpers.filter_params(
                        function, body, auth_token, self.__client_token_name)
                    return flask.jsonify(function(**parameters)), response_code
                except symmetric.errors.AuthenticationRequiredError as err:
                    # Error authenticating
                    self.__app.logger.error(
                        f"[[symmetric]] exception caught: {err}"
                    )
                    return flask.jsonify({}), 401
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
        docs = f"# {symmetric.helpers.humanize(module_name)} "
        docs += "API Documentation\n\n"
        docs += ("Endpoints that require an authentication token should "
                 f"send it in a key named `{self.__client_token_name}` "
                 "inside the request body.\n\n")
        raw_docs = [x.generate_documentation() for x in self.__endpoints]
        docs += "\n".join(raw_docs)
        return docs

    def __save_endpoint(self, endpoint):
        """Saves an endpoint object and sorts the endpoints list."""
        if endpoint in self.__endpoints:
            message = f"Endpoint '{endpoint.route}' was defined twice."
            raise symmetric.errors.DuplicatedURLError(message)
        bisect.insort(self.__endpoints, endpoint)

    def __log_request(self, request, route, function):
        """
        Recieves a request object, a route string and a function and
        logs the request event. It also logs the json body of the request.
        """
        self.__app.logger.info(
            f"{request.method} request to '{route}' endpoint "
            f"('{function.__name__}' function)."
        )
        body = request.get_json()
        if body:
            self.__log_body(body)

    def __log_body(self, body):
        """Given a json request body, logs it."""
        self.__app.logger.info("Request Body:\n" + json.dumps(
            body,
            indent=2,
            sort_keys=False,
            ensure_ascii=False
        ))


# Create flask app object
app = flask.Flask(__name__)


# Create symmetric object
sym = Symmetric(app)


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
            "filename": os.getenv(
                "LOG_FILE",
                default=symmetric.constants.LOG_FILE_NAME
            ),
            "formatter": "file"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    }
})
