import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from guvicorn_logger import Logger, __version__


def test_version():
    assert __version__ == "0.1.0"


logger = Logger().configure()

logger.info("Information")
logger.error("Error")
logger.warning("Warning")
logger.critical("Critical")

fmt = "(%(pid)s) | %(levelprefix)s | %(module)s:%(lineno)s | %(message)s"
logger = Logger(fmt=fmt).configure()

logger.info("Information")
logger.error("Error")
logger.warning("Warning")
logger.critical("Critical")

fmt = "(%(pid)s) | %(levelprefix)s | %(module)s:%(lineno)s | %(message)s"
logger = Logger(fmt=fmt, use_colors=False).configure()

logger.info("Information")
logger.error("Error")
logger.warning("Warning")
logger.critical("Critical")
