import logging

from app.core.config import settings
from app.middlewares.request_context import get_request_id


class RequestCorrelationFilter(logging.Filter):
    """This will fetch the request id from context vars and add it as log record"""

    def filter(self, record):
        record.request_id = get_request_id()
        return True


def getLogger(name):
    """
    Helper function to get a logger with a logging format which contains a unique request ID.
    The Request ID is generated via a middleware and added in context var.
    Only this function should be used for logging anything accross the app
    """
    logger = logging.getLogger(name)
    stream_handler = logging.StreamHandler()
    stream_handler.addFilter(RequestCorrelationFilter())

    formatter = logging.Formatter(
        "%(levelname)s - %(asctime)s - %(request_id)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    logger.addHandler(stream_handler)
    return logger
