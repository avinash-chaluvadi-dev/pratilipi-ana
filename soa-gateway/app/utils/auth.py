from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core import constants, exceptions, logging
from app.utils import jwt

logger = logging.getLogger(__name__)


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                logger.error(f"Invalid token scheme expected: Bearer")
                raise exceptions.ForbiddenException(
                    message=constants.JWT_INVALID_SCHEME
                )
            payload = jwt.decode_token(credentials.credentials)
            return payload
        else:
            raise exceptions.ForbiddenException(
                message=constants.JWT_INVALID_CODE
            )
