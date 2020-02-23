"""
This module contains the endpoints classes.
"""

import inspect


class Endpoint:

    """
    Class to encapsulate an endpoint.
    """

    def __init__(self, route, methods, response_code, function):
        self.__route = route
        self.__methods = methods
        self.__response_code = response_code
        self.__function = function

    def __lt__(self, other):
        return self.route < other.route

    @property
    def route(self):
        """Returns the route of the endpoint."""
        return self.__route

    def generate_documentation(self):
        """Generates the documentation of the function."""
        docstring = f"## `{self.__route}`\n\n"
        docstring += f"### Description\n\n"
        docstring += f"`HTTP` methods accepted: "
        docstring += f"{', '.join([f'`{x}`' for x in self.__methods])}\n\n"
        docstring += f"{self.__get_docstring()}\n\n"
        docstring += f"### Parameters\n\n{self.__get_parameters()}\n"
        return docstring

    def __get_docstring(self):
        """Gets the docstring of the function."""
        docstring = inspect.getdoc(self.__function)
        return docstring if docstring else "No description provided."

    def __get_parameters(self):
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
