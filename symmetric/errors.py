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


class IncorrectURLFormatError(Exception):
    """
    Exception for when an endpoint URL is incorrectly defined (it does
    not follow the expected URL format).
    """


class DuplicatedURLError(Exception):
    """
    Exception for when an endpoint URL is already in the added endpoints.
    """
