"""
A module for every helper of the OpenAPI documentation generator.
"""

import symmetric.constants


def is_not_docs(route):
    """Checks if a route is not a documentation-related route."""
    # Check that the route is not the schema route
    not_schema = route != symmetric.constants.OPENAPI_ROUTE
    # Check that the route is not the interactive documentation route
    not_documentation = route != symmetric.constants.DOCUMENTATION_ROUTE

    # Return if the route is neither of the documentation routes
    return not_schema and not_documentation
