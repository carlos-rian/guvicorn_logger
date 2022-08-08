# from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI

from guvicorn_logger import Logger

app = FastAPI()


# app.add_middleware(CorrelationIdMiddleware)


logger = Logger(correlation_id=False).configure()


@app.get("/")
def main():
    logger.info("Message - Info")
    logger.error("Message - Error")
    logger.warning("Message - Warning")
    logger.critical("Message - Critical")
