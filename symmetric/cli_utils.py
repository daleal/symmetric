"""
A module to hold some CLI utilities.
"""

import os
import sys
import json
import traceback
import importlib

import symmetric.errors
import symmetric.openapi.utils


def start_server(module, server, port, debug):
    """
    Gets the symmetric object and then runs it with the parameters given
    to the method.
    """
    symmetric_object = get_symmetric_object(module, debug)
    symmetric_object.run(host=server, port=port, debug=debug)


def document_api_markdown(module, filename):
    """
    Gets the symmetric object and then calls the markdown documentation method.
    """
    symmetric_object = get_symmetric_object(module, True)
    docs = symmetric_object.generate_markdown_documentation(module)
    with open(filename, "w") as docs_file:
        docs_file.write(docs)


def document_openapi(module, filename):
    """
    Gets the symmetric object and then calls the OpenAPI Specification method.
    """
    symmetric_object = get_symmetric_object(module, True)
    docs = symmetric.openapi.utils.get_openapi(
        symmetric_object,
        f"{symmetric.helpers.humanize(module)} API"
    )
    with open(filename, "w") as docs_file:
        json.dump(docs, docs_file, indent=2)


def get_symmetric_object(module_name, debug):
    """
    Imports the module :module_name and the tries to find the
    symmetric object. This method is strongly inspired in gunicorn's own
    import_app method and uvicorn's main method.
    """
    # Import the module
    try:
        # Add current directory to path
        sys.path.insert(0, ".")
        module = importlib.import_module(module_name)
    except ImportError:
        # If the user wrote module.py instead of just module
        if module_name.endswith(".py") and os.path.exists(module_name):
            actual_name = module_name.rsplit('.', 1)[0]
            error = (f"Module {module_name} not found. "
                     f"Did you mean {actual_name}?")
            raise ImportError(error)
        raise

    # Get the symmetric object
    try:
        symmetric_object = getattr(module, "symmetric")
    except AttributeError:
        if debug:
            traceback.print_exception(*sys.exc_info())
        error = f"Failed to find the symmetric object in {module_name}."
        raise symmetric.errors.AppImportError(error)

    return symmetric_object
