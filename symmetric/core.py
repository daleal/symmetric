"""
The main module of symmetric.
"""

import sys
import json
import bisect
import flask

import symmetric.logging
import symmetric.constants
import symmetric.endpoints
import symmetric.helpers
import symmetric.errors
import symmetric.openapi.utils
import symmetric.openapi.docs


class _SymmetricSingleton(type):

    """
    Singleton metaclass to limit the existance of the symmetric object to one.
    """

    def __call__(cls, *args, **kwargs):
        """Defines the class creation method."""
        if not hasattr(cls, "symmetric_instance"):  # Object does not exist
            # Create object
            cls.symmetric_instance = super().__call__(*args, **kwargs)
        return cls.symmetric_instance  # Return symmetric object


class _Symmetric(metaclass=_SymmetricSingleton):

    """
    Main class to encapsulate every important feature of the symmetric package.
    """

    # Define allowed HTTP methods
    __allowed_methods = [
        "GET",
        "PUT",
        "POST",
        "DELETE",
        "OPTIONS",
        "HEAD",
        "PATCH",
        "TRACE"
    ]

    def __init__(self):
        self.__app = flask.Flask(__name__)  # Create flask app object
        self.__endpoints = []
        self.__openapi_schema = None
        self.__server_token_name = symmetric.constants.API_SERVER_TOKEN_NAME
        self.__client_token_name = symmetric.constants.API_CLIENT_TOKEN_NAME
        self.setup()

    @property
    def endpoints(self):
        """Returns a list with the endpoints."""
        return self.__endpoints

    @property
    def openapi(self):
        """
        Returns the openapi schema. If it does not exist, it creates it
        and returns it.
        """
        if not self.__openapi_schema:
            self.__openapi_schema = symmetric.openapi.utils.get_openapi(
                self,
                symmetric.helpers.humanize(
                    symmetric.helpers.get_module_name(self)
                ) + " API"
            )
        return self.__openapi_schema

    @property
    def client_token_name(self):
        """Return the client token name."""
        return self.__client_token_name

    def setup(self):
        """Sets up the API."""
        # Set up the endpoint for the openapi json schema
        # pylint: disable=W0612
        @self.__app.route(symmetric.constants.OPENAPI_ROUTE)
        def openapi_schema():
            return self.openapi

        # Set up the endpoint for the interactive documentation
        # pylint: disable=W0612
        @self.__app.route(symmetric.constants.DOCUMENTATION_ROUTE)
        def docs():
            return symmetric.openapi.docs.get_redoc_html(
                symmetric.helpers.humanize(
                    symmetric.helpers.get_module_name(self)
                ) + " API"
            )

    def __call__(self, *args, **kwargs):
        """
        Enable WSGI servers to start with CLI utilities
        (like gunicorn module:symmetric).
        """
        return self.__app.__call__(*args, **kwargs)

    def set_client_token_name(self, client_token_name):
        """Changes the default client token name to :client_token_name."""
        if not isinstance(client_token_name, str):  # Manage wrong type
            error = ("Invalid client token name type "
                     "given on set_client_token_name call")
            raise symmetric.errors.InvalidTokenNameError(error)
        if not client_token_name:  # Manage empty client token name
            error = ("Empty client token name given "
                     "on set_client_token_name call")
            raise symmetric.errors.InvalidTokenNameError(error)
        # Set new client token name
        self.__client_token_name = client_token_name
        return True

    def set_server_token_name(self, server_token_name):
        """Changes the default server token name to :server_token_name."""
        if not isinstance(server_token_name, str):  # Manage wrong type
            error = ("Invalid server token name type "
                     "given on set_server_token_name call")
            raise symmetric.errors.InvalidTokenNameError(error)
        if not server_token_name:  # Manage empty server token name
            error = ("Empty server token name given "
                     "on set_server_token_name call")
            raise symmetric.errors.InvalidTokenNameError(error)
        # Set new server token name
        self.__server_token_name = server_token_name
        return True

    def router(self, route, methods=["post"], response_code=200,
               auth_token=False):
        """
        Decorator modifier. Recieves a route string, a list of HTTP methods, a
        response code and a boolean indicating whether or not to authenticate.
        The route gets format-checked. Returns the original function unchanged.
        """
        try:
            symmetric.helpers.parse_route(route)
        except symmetric.errors.IncorrectRouteFormatError as err:
            self.__app.logger.error(
                f"[[symmetric]] IncorrectRouteFormatError: {err}"
            )
            sys.exit(1)

        methods = [
            symmetric.helpers.verb(x) for x in methods
            if symmetric.helpers.verb(x) in _Symmetric.__allowed_methods
        ]

        def decorator(function):
            """
            Function decorator. Recieves the main function and wraps it as a
            flask endpoint. Returns the original unwrapped function.
            """
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
                    request_headers = flask.request.headers
                    if not body:
                        body = {}

                    # Check for token authentication
                    symmetric.helpers.authenticate(
                        request_headers, auth_token, self.__client_token_name,
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

            # Save Endpoint
            try:
                self.__save_endpoint(
                    symmetric.endpoints.Endpoint(
                        route,
                        methods,
                        response_code,
                        function,  # Save unchanged function
                        wrapper,   # Save flask decorated function
                        auth_token
                    )
                )
            except symmetric.errors.DuplicatedRouteError as err:
                self.__app.logger.error(
                    f"[[symmetric]] DuplicatedRouteError: {err}"
                )
                sys.exit(1)

            return function  # Return unchanged function
        return decorator

    def run(self, *args, **kwargs):
        """Executes the main run function of the Flask object."""
        self.__app.run(*args, **kwargs)

    def generate_markdown_documentation(self, module_name):
        """
        Gets the documentation of every endpoint and assembles it into a
        markdown formatted string.
        """
        docs = f"# {symmetric.helpers.humanize(module_name)} "
        docs += "API Documentation\n\n"
        docs += ("Endpoints that require an authentication token should "
                 f"send it in a key named `{self.__client_token_name}` "
                 "inside the request headers.\n\n")
        raw_docs = [
            x.generate_markdown_documentation() for x in self.__endpoints]
        docs += "\n".join(raw_docs)
        return docs

    def __save_endpoint(self, endpoint):
        """Saves an endpoint object and sorts the endpoints list."""
        if endpoint in self.__endpoints:
            message = f"Endpoint '{endpoint.route}' was defined twice."
            raise symmetric.errors.DuplicatedRouteError(message)
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


# Create symmetric object
symmetric_object = _Symmetric()
