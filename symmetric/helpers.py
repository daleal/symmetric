"""
A module for every helper of symmetric.
"""

import re
import os
import inspect

import symmetric.constants
import symmetric.errors


def verb(dirty):
    """
    Given a 'dirty' string (lowercased, with trailing whitespaces), strips
    it and returns it uppercased.
    """
    return dirty.strip().upper()


def get_module_name(symmetric_object):
    """
    Given a symmetric object, returns the name of the module where the
    first endpoint was defined. If such endpoint does not exist, return
    a generic module name.
    """
    if not symmetric_object.endpoints:
        return "symmetric"
    return symmetric_object.endpoints[0].function.__module__.split(".")[0]


def type_to_string(type_obj):
    """Given a python type, return its JSON schema string counterpart."""
    type_str = type_obj.__name__
    if type_str == "str":
        return "string"
    if type_str == "float":
        return "number"
    if type_str == "int":
        return "integer"
    if type_str == "bool":
        return "boolean"
    if type_str == "NoneType":
        return "null"
    if type_str == "list":
        return "array"
    return "object"


def humanize(module_name):
    """Transforms a module name into a pretty human-likable string."""
    module_name = module_name.lower()
    module_name = module_name.replace('_', ' ').replace('-', ' ')
    module_name = module_name.title()
    return module_name


def parse_route(route):
    """
    If :route does not match the expected route pattern,
    raises IncorrectRouteFormatError.
    """
    if re.fullmatch(symmetric.constants.ROUTE_PATTERN, route) is None:
        message = (f"Your route '{route}' does not match with the symmetric "
                   "route guidelines. Refer to the documentation at "
                   "https://github.com/daleal/symmetric for more information.")
        raise symmetric.errors.IncorrectRouteFormatError(message)


def authenticate(headers, auth_token, client_token_name, server_token_name):
    """
    Raises an exception if the headers do not include the client token
    or if it is different to the server token.
    """
    if not auth_token:
        # No auth is required
        return
    # Auth is required from now on
    if client_token_name not in headers:
        # The headers do not include the desired token
        error = "The request does not include an authentication token."
        raise symmetric.errors.AuthenticationRequiredError(error)
    # If the token in the headers equals the one in the env, return True
    token = os.getenv(server_token_name, symmetric.constants.API_DEFAULT_TOKEN)
    if headers[client_token_name] != token:
        error = "Incorrect authentication token."
        raise symmetric.errors.AuthenticationRequiredError(error)


def filter_params(function, data, has_token, token_key):
    """Filters parameters so that the function recieves only what it needs."""
    # Filter token key
    if has_token:
        data.pop(token_key, None)

    # Get the parameters
    params = inspect.getfullargspec(function)
    if params.varkw is not None:
        # The function recieves kwargs, return the full dictionary
        return data
    if not params.args:
        # The function does not recieve args, return an empty dict
        return {}
    # Filter every param whose key is not in the params dictionary
    return {k: v for k, v in data.items() if k in params.args}
