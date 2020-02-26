"""
Module to hold every custom exception.
"""


class AppImportError(Exception):
    """
    Exception for when there's an error finding the symmetric object inside
    the specified module.
    """
