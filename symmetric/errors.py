"""
Module to hold every custom exception.
"""


class AppImportError(Exception):
    """
    Exception for when there's an error finding the symmetric object inside
    the specified module.
    """


class AuthenticationRequiredError(Exception):
    """
    Exception for when an endpoint requires authentication and the request
    fails to provide the correct authentication token.
    """


class IncorrectRouteFormatError(Exception):
    """
    Exception for when an endpoint route is incorrectly defined (it does
    not follow the expected route format).
    """


class DuplicatedRouteError(Exception):
    """
    Exception for when an endpoint route is already in the added endpoints.
    """
