import time

from fastapi import Request, Response

from app.core import logging
from app.core.constants import SUCCESS_RESPONSE_CODE

logger = logging.getLogger(__name__)


async def timeit_logger(request: Request, call_next: callable):
    """
    Middleware for catching global exception if it is missed
    and also for logging time taken for each request to be processed
    """
    start_time = time.time()
    try:
        logger.info(
            f"Request received for {request.method} {request.url.path}"
        )
        response: Response = await call_next(request)
        if response.status_code in SUCCESS_RESPONSE_CODE:
            logger.info(
                f"Request completed for {request.method} {request.url.path} in {time.time() - start_time:0.2f}s"
            )
        else:
            logger.error(
                f"Request failed for {request.method} {request.url.path} in {time.time() - start_time:0.2f}s"
            )
        return response
    except Exception as e:
        logger.error(f"exception occurred while processing request {str(e)}")
        logger.error(
            f"Request failed for {request.method} {request.url.path} in {time.time() - start_time:0.2f}s"
        )
        return Response("Internal server error", status_code=500)
