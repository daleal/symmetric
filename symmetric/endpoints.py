"""
This module contains the endpoints classes.
"""

import inspect

import symmetric.helpers


class Endpoint:

    """
    Class to encapsulate an endpoint.
    """

    def __init__(self, route, methods, response_code, function, has_token):
        self.__route = route
        self.__methods = methods
        self.__response_code = response_code
        self.__function = function
        self.__has_token = has_token

    def __lt__(self, other):
        return self.route < other.route

    def __eq__(self, other):
        return self.route == other.route

    @property
    def route(self):
        """Returns the route of the endpoint."""
        return self.__route

    # COMMON DOCUMENTATION METHODS

    def __get_docstring(self):
        """Gets the docstring of the function."""
        docstring = inspect.getdoc(self.__function)
        return docstring if docstring else "No description provided."

    # JSON SCHEMA DOCUMENTATION METHODS

    def openapi_documentation(self):
        """Generate the OpenAPI documentation for the endpoint."""
        request_body = self.__json_schema_request_body()
        response_codes = self.__response_codes_openapi()
        docstring = self.__get_docstring()
        path_doc = {}
        for http_method in map(lambda x: x.lower(), self.__methods):
            path_doc[http_method] = {
                "description": docstring,
                "responses": response_codes
            }
            has_props = bool(request_body["properties"])
            has_body = has_props or bool(request_body["additionalProperties"])
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
            self.__route: path_doc
        }

    def __json_schema_request_body(self):
        """Assembles the JSON schema for the request body."""
        any_type = [
            {
                "type": "string"
            },
            {
                "type": "number"
            },
            {
                "type": "integer"
            },
            {
                "type": "boolean"
            },
            {
                "type": "array"
            },
            {
                "type": "object"
            },
        ]
        params = inspect.getfullargspec(self.__function)
        schema = {}
        if params.args:
            parameters_amount = len(params.args)
            if params.defaults:
                defaults_amount = len(params.defaults)
                no_defaults = parameters_amount - defaults_amount
                for ii in range(no_defaults):
                    if params.args[ii] not in params.annotations:
                        var_label = "oneOf"
                        var_type = any_type
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
                        var_type = any_type
                    else:
                        var_label = "type"
                        var_type = symmetric.helpers.type_to_string(
                            params.annotations[params.args[no_defaults + jj]])
                    schema[params.args[no_defaults + jj]] = {
                        var_label: var_type,
                        "default": params.defaults[jj]
                    }
            else:
                for ii in range(parameters_amount):
                    if params.args[ii] not in params.annotations:
                        var_label = "oneOf"
                        var_type = any_type
                    else:
                        var_label = "type"
                        var_type = symmetric.helpers.type_to_string(
                            params.annotations[params.args[ii]])
                    schema[params.args[ii]] = {
                        var_label: var_type
                    }
        return {
            "type": "object",
            "properties": schema,
            "additionalProperties": params.varkw is not None
        }

    def __response_codes_openapi(self):
        """Gets the error codes for the OpenAPI Schema."""
        params = inspect.getfullargspec(self.__function)
        responses = {
            f"{self.__response_code}": {
                "description": "Successful operation"
            },
            "500": {
                "description": "Unexpected internal error (API method "
                               "failed, probably due to a missuse of the "
                               "underlying function)."
            }
        }
        if self.__has_token:
            responses["401"] = {
                "description": "Invalid or non-existent authentication "
                               "credentials."
            }
        if "return" in params.annotations:
            responses[f"{self.__response_code}"]["content"] = {
                "application/json": {
                    "schema": {
                        "type": symmetric.helpers.type_to_string(
                            params.annotations["return"])
                    }
                }
            }
        return responses

    # MARKDOWN DOCUMENTATION METHODS

    def generate_markdown_documentation(self):
        """Generates the documentation of the function."""
        docstring = f"## `{self.__route}`\n\n"
        docstring += f"### Description\n\n"
        docstring += f"{self.__get_docstring()}\n\n"
        docstring += f"### Metadata\n\n"
        docstring += f"`HTTP` methods accepted: "
        docstring += f"{', '.join([f'`{x}`' for x in self.__methods])}\n\n"
        if self.__has_token:
            docstring += "Requires an authentication token.\n\n"
        else:
            docstring += "Does not require an authentication token.\n\n"
        docstring += f"### Parameters\n\n{self.__get_markdown_parameters()}\n"
        return docstring

    def __get_markdown_parameters(self):
        """Gets the parameters of the function."""
        params = inspect.getfullargspec(self.__function)
        if not params.args:
            return "No required parameters."
        parameters_amount = len(params.args)
        docstring = "```py\n{\n"
        if params.defaults:
            defaults_amount = len(params.defaults)
            no_defaults = parameters_amount - defaults_amount
            for ii in range(no_defaults):
                docstring += f"    {params.args[ii]},\n"

            for jj in range(defaults_amount):
                docstring += f"    {params.args[no_defaults + jj]},  # "
                if isinstance(params.defaults[jj], str):
                    default = f'"{params.defaults[jj]}"'
                else:
                    default = params.defaults[jj]
                docstring += f"defaults to {default}\n"
        else:
            for ii in range(parameters_amount):
                docstring += f"    {params.args[ii]},\n"

        docstring += "}\n```"

        return docstring
