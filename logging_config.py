"""Config setup for janus-api."""

from __future__ import annotations

from logging.config import dictConfig
from pathlib import Path

log_file_path = Path("log/janus-api.log")
log_file_path.parent.mkdir(parents=True, exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "log/janus-api.log",
            "formatter": "default",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["file", "console"],
    },
}

dictConfig(LOGGING_CONFIG)
