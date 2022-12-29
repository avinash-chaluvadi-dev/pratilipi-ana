import logging
from contextvars import ContextVar
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

from app.core.constants import REQUEST_ID_CTX_KEY

logger = logging.getLogger(__name__)


_request_id_ctx_var: ContextVar[str] = ContextVar(
    REQUEST_ID_CTX_KEY, default=None
)


def get_request_id() -> str:
    """
    Get unique request id from ContextVar

    :returns unique request id of type str
    """
    return _request_id_ctx_var.get()


class RequestContextLogMiddleware(BaseHTTPMiddleware):
    """
    This Middleware will Generate a unique request ID for each request and add it in
    ContextVar, so that it can be later retrieved and used for logging.
    It will also add the same Request ID in response header as X-Request-ID
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        request_id = _request_id_ctx_var.set(str(uuid4()))
        response = await call_next(request)
        response.headers["X-Request-ID"] = get_request_id()
        _request_id_ctx_var.reset(request_id)

        return response
