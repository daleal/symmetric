"""
A module for every helper of symmetric.
"""

import json

from .app import app


def verb(dirty):
    """
    Given a 'dirty' string (lowercased, with trailing whitespaces), strips
    it and returns it uppercased.
    """
    return dirty.strip().upper()


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
