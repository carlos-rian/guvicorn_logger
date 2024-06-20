import os
import sys
from datetime import datetime

from pytz import timezone

from guvicorn_logger.core import AccessFormatter, DefaultFormatter

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from guvicorn_logger import Logger, __version__


def test_version():
    assert __version__ == "0.1.0"


logger = Logger().configure()

logger.info("Information")
logger.error("Error")
logger.warning("Warning")
logger.critical("Critical")

fmt = "(%(pid)s) | %(levelprefix)s %(message)s"
logger = Logger(fmt=fmt).configure()

logger.info("Information")
logger.error("Error")
logger.warning("Warning")
logger.critical("Critical")

fmt = "(%(pid)s) | %(levelprefix)s %(message)s"
logger = Logger(fmt=fmt, use_colors=False).configure()

logger.info("Information")
logger.error("Error")
logger.warning("Warning")
logger.critical("Critical")


def timetz(*args):
    return datetime.now(tz).timetuple()


tz = timezone("Asia/Shanghai")  # UTC, Asia/Shanghai, Europe/Berlin
AccessFormatter.converter = timetz
DefaultFormatter.converter = timetz

logger = Logger().configure()

logger.info("Information")
logger.error("Error")
logger.warning("Warning")
logger.critical("Critical")
