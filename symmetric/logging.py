"""
A module to set up the logging configuration of symmetric.
"""

import os
import logging.config

import symmetric.constants


# Logging configuration
logging.config.dictConfig({
    "version": 1,
    "formatters": {
        "console": {
            "format": "[%(asctime)s] [%(levelname)s] %(module)s: %(message)s"
        },
        "file": {
            "format": ("[%(asctime)s] [%(levelname)s] %(pathname)s - "
                       "line %(lineno)d: \n%(message)s\n")
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "formatter": "console"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": os.getenv(
                "LOG_FILE",
                default=symmetric.constants.LOG_FILE_NAME
            ),
            "formatter": "file"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    }
})
