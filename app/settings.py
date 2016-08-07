"""
Appliction configuration settings
"""
import os

from tornado.options import define

define("debug", default=True, help="Debug settings")
define("port", default=9000, help="Port to run the server on")

_CUR_DIR = os.path.dirname(os.path.realpath(__file__))
MODEL_DIR = os.path.join(_CUR_DIR, "..", "models")
LOG_DIR = os.path.join(_CUR_DIR, "..", "logs")

MAX_THREAD_POOL = 10

LOG_SETTINGS = {
    'version': 1,
    "root": {
        "level": "WARNING",
        "handlers": ["console"],
    },
    "formatters": {
        "json": {
            "()": "app.utils.log_formatters.JSONFormatter",
        },
        "simple": {
            "format": "%(levelname)s %(message)s",
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': "simple"
        },
        'applog': {
            "class": "logging.handlers.TimedRotatingFileHandler",
            'level': "INFO",
            'formatter': "json",
            'filename': os.path.join(LOG_DIR, "app.log"),
            "when": "D",
            "interval": 2,
            "backupCount": 5
        },
        'accesslog': {
            "class": "logging.handlers.TimedRotatingFileHandler",
            'level': "INFO",
            'formatter': "json",
            'filename': os.path.join(LOG_DIR, "access.log"),
            "when": "D",
            "interval": 2,
            "backupCount": 5
        },
    },
    "loggers": {
        "tornado.access": {
            "handlers": ["console", "accesslog"],
            "level": "INFO",
            "propagate": False,
        },
        "tornado.application": {
            "handlers": ["console", "applog"],
            "level": "INFO",
            "propagate": False,
        },
        "tornado.general": {
            "handlers": ["console", "applog"],
            "level": "INFO",
            "propagate": False,
        },
        "app": {
            "handlers": ["console", "applog"],
            "level": "INFO",
            "propagate": False,
        },
    }
}