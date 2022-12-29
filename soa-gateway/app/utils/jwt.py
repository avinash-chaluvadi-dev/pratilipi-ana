from datetime import datetime, timedelta, timezone

import jwt
from pydantic.error_wrappers import ValidationError

from app.core import exceptions
from app.core.config import settings
from app.schemas.auth import AccessTokenClaims


def generate_token(payload: dict) -> bytes:
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.CRYPTOGRAPHY)
    return token


def decode_token(token: str) -> AccessTokenClaims:
    claims = {}
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.CRYPTOGRAPHY])
        claims = AccessTokenClaims(**payload)

    except jwt.ExpiredSignatureError:
        raise exceptions.BadRequestException(message="Token expired")
    except jwt.InvalidSignatureError as e:
        raise exceptions.ForbiddenException(message=str(e))
    except (jwt.PyJWTError, ValidationError):
        raise exceptions.BadRequestException(message="Invalid Token")

    return claims


def generate_claims(username: str, expiration_minutes: int, group: str = None) -> dict[str:any]:
    claims = {
        "username": username,
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=expiration_minutes),
    }

    if group:
        claims["group"] = group

    return claims
