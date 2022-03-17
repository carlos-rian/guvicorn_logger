import http
import logging
from copy import copy

import click
from uvicorn.logging import AccessFormatter as _AF
from uvicorn.logging import DefaultFormatter as _DF

TRACE_LOG_LEVEL = 5


class DefaultFormatter(_DF):
    level_name_colors = {
        TRACE_LOG_LEVEL: lambda level_name: click.style(
            str(level_name), fg="blue", bold=True
        ),
        logging.DEBUG: lambda level_name: click.style(
            str(level_name), fg="cyan", bold=True
        ),
        logging.INFO: lambda level_name: click.style(
            str(level_name), fg="green", bold=True
        ),
        logging.WARNING: lambda level_name: click.style(
            str(level_name), fg="yellow", bold=True
        ),
        logging.ERROR: lambda level_name: click.style(
            str(level_name), fg="red", bold=True
        ),
        logging.CRITICAL: lambda level_name: click.style(
            str(level_name), fg="bright_red", bold=True
        ),
    }

    def color_default(self, asctime: str, level_no: int) -> str:
        def default(asctime: str) -> str:
            return str(asctime)

        func = self.level_name_colors.get(level_no, default)
        return func(asctime)

    def formatMessage(self, record: logging.LogRecord) -> str:
        recordcopy = copy(record)
        levelname = recordcopy.levelname
        asctime = recordcopy.__dict__.get("asctime", "")
        _norm_process = "PID: " + str(recordcopy.__dict__.get("process", ""))
        process = _norm_process + ": " + " " * (9 - len(_norm_process))
        message = recordcopy.__dict__.get("message", "")
        module = recordcopy.__dict__.get("module", "")
        lineno = recordcopy.__dict__.get("lineno", "")

        seperator = " " * (8 - len(recordcopy.levelname))

        if self.use_colors:
            levelname = self.color_level_name(levelname, recordcopy.levelno)
            asctime = self.color_default(asctime, recordcopy.levelno)
            message = click.style(message, fg="bright_white")
            process = self.color_default(process, recordcopy.levelno)
            module = click.style(str(module), fg="bright_white")
            lineno = click.style(str(lineno), fg="bright_white")
            if "color_message" in recordcopy.__dict__:
                recordcopy.msg = recordcopy.__dict__["color_message"]
                recordcopy.__dict__["message"] = recordcopy.getMessage()

        recordcopy.asctime = asctime
        recordcopy.message = message
        recordcopy.module = module
        recordcopy.lineno = lineno
        recordcopy.__dict__["pid"] = process
        recordcopy.__dict__["levelprefix"] = levelname + ":" + seperator
        return super().formatMessage(recordcopy)


class AccessFormatter(_AF):
    level_name_colors = {
        TRACE_LOG_LEVEL: lambda level_name: click.style(
            str(level_name), fg="blue", bold=True
        ),
        logging.DEBUG: lambda level_name: click.style(
            str(level_name), fg="cyan", bold=True
        ),
        logging.INFO: lambda level_name: click.style(
            str(level_name), fg="green", bold=True
        ),
        logging.WARNING: lambda level_name: click.style(
            str(level_name), fg="yellow", bold=True
        ),
        logging.ERROR: lambda level_name: click.style(
            str(level_name), fg="red", bold=True
        ),
        logging.CRITICAL: lambda level_name: click.style(
            str(level_name), fg="bright_red", bold=True
        ),
    }

    def color_default(self, asctime: str, level_no: int) -> str:
        def default(asctime: str) -> str:
            return str(asctime)

        func = self.level_name_colors.get(level_no, default)
        return func(asctime)

    def get_status_code(self, status_code: int) -> str:
        try:
            status_phrase = http.HTTPStatus(status_code).phrase
        except ValueError:
            status_phrase = ""
        status_and_phrase = "%s %s" % (status_code, status_phrase)
        if self.use_colors:

            def default(code: int) -> str:
                return status_and_phrase  # pragma: no cover

            func = self.status_code_colours.get(status_code // 100, default)
            return func(status_and_phrase)
        return status_and_phrase

    def normalize_default(self, recordcopy: logging.LogRecord) -> logging.LogRecord:
        levelname = recordcopy.levelname
        asctime = recordcopy.__dict__.get("asctime", "")
        _norm_process = "PID: " + str(recordcopy.__dict__.get("process", ""))
        process = _norm_process + ": " + " " * (9 - len(_norm_process))
        message = recordcopy.__dict__.get("message", "")
        module = recordcopy.__dict__.get("module", "")
        lineno = recordcopy.__dict__.get("lineno", "")

        seperator = " " * (8 - len(recordcopy.levelname))
        if self.use_colors:
            levelname = self.color_level_name(levelname, recordcopy.levelno)
            asctime = self.color_default(asctime, recordcopy.levelno)
            message = click.style(message, fg="bright_white")
            process = self.color_default(process, recordcopy.levelno)
            module = click.style(str(module), fg="bright_white")
            lineno = click.style(str(lineno), fg="bright_white")
        recordcopy.asctime = asctime
        recordcopy.message = message
        recordcopy.module = module
        recordcopy.lineno = lineno
        recordcopy.__dict__["pid"] = process
        recordcopy.__dict__["levelprefix"] = levelname + ":" + seperator

    def formatMessage(self, record: logging.LogRecord) -> str:
        recordcopy = copy(record)
        self.normalize_default(recordcopy)
        (
            client_addr,
            method,
            full_path,
            http_version,
            status_code,
        ) = recordcopy.args
        status_code = self.get_status_code(int(status_code))
        request_line = "%s %s HTTP/%s" % (method, full_path, http_version)
        if self.use_colors:
            request_line = click.style(request_line, bold=True)
        recordcopy.message = f'{client_addr} - "{request_line}" {status_code}'
        return super().formatMessage(recordcopy)
