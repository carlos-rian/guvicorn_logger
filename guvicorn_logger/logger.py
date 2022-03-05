import logging
from logging import config

from gunicorn import glogging


class Logger:
    """
    formatter default: [%(asctime)s] PID: %(process)s %(levelprefix)s %(message)s
    """

    def __init__(self, fmt: str = None, use_colors: bool = True) -> None:
        DEFAULT_FORMAT = "(%(asctime)s) (%(pid)s) | %(levelprefix)s %(message)s"
        self._formatter = fmt or DEFAULT_FORMAT
        self._use_colors = use_colors

    def get_config(self):
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "guvicorn_logger.core.DefaultFormatter",
                    "fmt": self._formatter,
                    "use_colors": self._use_colors,
                },
                "access": {
                    "()": "guvicorn_logger.core.AccessFormatter",
                    "fmt": self._formatter,
                    "use_colors": self._use_colors,
                },
            },
            "handlers": {
                "console": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
                "access": {
                    "formatter": "access",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "root": {"handlers": ["console"], "level": "INFO"},
            "loggers": {
                "gunicorn": {"propagate": True},
                "gunicorn.info": {"propagate": True},
                "gunicorn.access": {
                    "level": "INFO",
                    "handlers": ["access"],
                    "propagate": False,
                    "qualname": "gunicorn.access",
                },
                "gunicorn.error": {"propagate": True},
                "uvicorn": {"propagate": True},
                "uvicorn.access": {
                    "level": "DEBUG",
                    "handlers": ["access"],
                    "propagate": False,
                    "qualname": "uvicorn.access",
                },
                "uvicorn.error": {"propagate": True},
            },
        }

    def configure(self) -> glogging.logging:
        log_config = self.get_config()
        config.dictConfig(log_config)
        glogging.dictConfig(log_config)

        return glogging.logging
