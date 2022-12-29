from typing import Union

from fastapi import APIRouter, status

from app.connectors.ldap_adapter import LdapAdapter
from app.core import logging
from app.core.config import settings
from app.schemas.auth import (LoginRequest, LoginResponse, RefreshRequest,
                              TokenBase)
from app.schemas.base import ErrorBase
from app.utils import jwt

v1_router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)


@v1_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=Union[LoginResponse, ErrorBase],
    responses={
        400: {"model": ErrorBase},
        500: {"model": ErrorBase},
        403: {"model": ErrorBase},
    },
)
async def login(payload: LoginRequest):
    adapter = LdapAdapter(username=payload.username, password=payload.password)
    adapter.authenticate()
    data = adapter.exc_query()
    access_token = jwt.generate_token(
        jwt.generate_claims(
            data["cn"], settings.ACCESS_TOKEN_EXP_TIME, data["group"]
        )
    )
    refresh_token = jwt.generate_token(
        jwt.generate_claims(
            data["cn"], settings.REFRESH_TOKEN_EXP_TIME, data["group"]
        )
    )
    logger.info("User logged in")
    return LoginResponse(
        **data, access_token=access_token, refresh_token=refresh_token
    )


# TODO: Before returning token pairs, check in AD if user is still active
@v1_router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    response_model=Union[TokenBase, ErrorBase],
    responses={
        400: {"model": ErrorBase},
        500: {"model": ErrorBase},
        403: {"model": ErrorBase},
    },
)
async def refresh(payload: RefreshRequest):
    claims = jwt.decode_token(payload.refresh_token)
    access_token = jwt.generate_token(
        jwt.generate_claims(
            claims.username, settings.ACCESS_TOKEN_EXP_TIME, claims.group
        )
    )
    refresh_token = jwt.generate_token(
        jwt.generate_claims(
            claims.username, settings.REFRESH_TOKEN_EXP_TIME, claims.group
        )
    )
    logger.debug("User refreshed token")
    return TokenBase(access_token=access_token, refresh_token=refresh_token)
