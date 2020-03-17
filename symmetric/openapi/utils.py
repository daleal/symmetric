"""
Module to hold the openapi documentation creation utilities.
"""

import inspect
import functools

import symmetric.openapi.constants
import symmetric.openapi.helpers


def get_openapi_endpoint(endpoint):
    """Generate the OpenAPI documentation for :endpoint."""
    request_body = get_openapi_endpoint_body(endpoint)
    response_codes = get_openapi_endpoint_responses(endpoint)
    path_doc = {}
    for http_method in map(lambda x: x.lower(), endpoint.methods):
        path_doc[http_method] = {
            "description": endpoint.docstring,
            "responses": response_codes
        }
        has_props = bool(request_body["properties"])
        has_body = has_props or bool(request_body["additionalProperties"])
        if endpoint.has_token:
            path_doc[http_method]["security"] = [
                {
                    "APIKeyAuth": []
                }
            ]
        if has_body:
            path_doc[http_method]["requestBody"] = {
                "required": has_props,
                "content": {
                    "application/json": {
                        "schema": request_body
                    }
                }
            }
    return {
        endpoint.route: path_doc
    }


def get_openapi_endpoint_body(endpoint):
    """Assembles the JSON schema for the endpoint body."""
    params = inspect.getfullargspec(endpoint.function)
    schema = {}
    if params.args:
        parameters_amount = len(params.args)
        defaults_amount = 0 if not params.defaults else len(params.defaults)
        defaults_amount = len(params.defaults)
        no_defaults = parameters_amount - defaults_amount
        for ii in range(no_defaults):
            if params.args[ii] not in params.annotations:
                var_label = "oneOf"
                var_type = symmetric.openapi.constants.ANY_TYPE
            else:
                var_label = "type"
                var_type = symmetric.helpers.type_to_string(
                    params.annotations[params.args[ii]])
            schema[params.args[ii]] = {
                var_label: var_type
            }
        for jj in range(defaults_amount):
            if params.args[no_defaults + jj] not in params.annotations:
                var_label = "oneOf"
                var_type = symmetric.openapi.constants.ANY_TYPE
            else:
                var_label = "type"
                var_type = symmetric.helpers.type_to_string(
                    params.annotations[params.args[no_defaults + jj]])
            schema[params.args[no_defaults + jj]] = {
                var_label: var_type,
                "default": params.defaults[jj]
            }
    return {
        "type": "object",
        "properties": schema,
        "additionalProperties": params.varkw is not None
    }


def get_openapi_endpoint_responses(endpoint):
    """Gets the OpenAPI Schema error codes for the endpoint."""
    params = inspect.getfullargspec(endpoint.function)
    responses = {
        f"{endpoint.response_code}": {
            "$ref": "#/components/responses/SuccesfulOperation"
        },
        "500": {
            "$ref": "#/components/responses/InternalError"
        }
    }
    if endpoint.has_token:
        responses["401"] = {
            "$ref": "#/components/responses/UnauthorizedError"
        }
    if "return" in params.annotations:
        responses[f"{endpoint.response_code}"]["content"] = {
            "application/json": {
                "schema": {
                    "type": symmetric.helpers.type_to_string(
                        params.annotations["return"])
                }
            }
        }
    return responses


def get_openapi(sym_obj, title, version="0.0.1", openapi_version="3.0.3"):
    """
    Gets the OpenAPI spec of every endpoint and assembles it into a
    JSON formatted object.
    """
    return {
        "openapi": openapi_version,
        "info": {
            "title": title,
            "version": version
        },
        "paths": functools.reduce(
            lambda x, y: {**x, **y},
            [get_openapi_endpoint(endpoint) for endpoint in sym_obj.endpoints
                if symmetric.openapi.helpers.is_not_docs(endpoint.route)],
            {}
        ),
        "components": {
            "securitySchemes": {
                "APIKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": sym_obj.client_token_name
                }
            },
            "responses": {
                "SuccesfulOperation": {
                    "description": "Successful operation"
                },
                "UnauthorizedError": {
                    "description": "Invalid or non-existent authentication "
                                   "credentials."
                },
                "InternalError": {
                    "description": "Unexpected internal error (API method "
                                   "failed, probably due to a missuse of the "
                                   "underlying function)."
                }
            }
        }
    }
