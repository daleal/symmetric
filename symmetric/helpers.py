"""
A module for every helper of symmetric.
"""

import os
import json
import inspect

import symmetric.constants
from symmetric.core import app


def verb(dirty):
    """
    Given a 'dirty' string (lowercased, with trailing whitespaces), strips
    it and returns it uppercased.
    """
    return dirty.strip().upper()


def humanize(module_name):
    """Transforms a module name into a pretty human-likable string."""
    module_name = module_name.lower()
    module_name = module_name.replace('_', ' ').replace('-', ' ')
    module_name = module_name.title()
    return module_name


def authenticated(body, auth_token, client_token_name, server_token_name):
    """
    Returns True if the body contains the necessary token to query the
    endpoint. If no auth token is required, also returns True.
    """
    if not auth_token:
        # No auth is required
        return True
    # Auth is required from now on
    if client_token_name not in body:
        # The body does not include the desired token
        return False
    # If the token in the body equals the one in the env, return True
    token = os.getenv(server_token_name, symmetric.constants.API_DEFAULT_TOKEN)
    return body[client_token_name] == token


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


def log_request(request, route, function):
    """
    Recieves a request object, a route string and a function and
    logs the request event. It also logs the json body of the request.
    """
    app.logger.info(
        f"{request.method} request to '{route}' endpoint "
        f"('{function.__name__}' function)."
    )
    body = request.get_json()
    if body:
        log_body(body)


def log_body(body):
    """Given a json request body, logs it."""
    app.logger.info("Request Body:\n" + json.dumps(
        body,
        indent=2,
        sort_keys=False,
        ensure_ascii=False
    ))
