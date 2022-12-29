import json

import requests
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import Mount
from ldap3 import SAFE_SYNC, Connection

from app.connectors.db_conn import get_engine
from app.connectors.ldap_adapter import LdapAdapter
from app.core import constants, exceptions, logging
from app.core.config import settings
from app.core.constants import PROTEGRITY_HEADERS, PROTEGRITY_SAMPLE_INPUT
from app.middlewares.request_context import RequestContextLogMiddleware
from app.middlewares.timeit import timeit_logger

from .api import (auth, voicemail, voicemail_archive, voicemail_box,
                  voicemail_features)

logger = logging.getLogger(__name__)


APP_META = {
    "title": settings.APP_TITLE,
    "description": settings.APP_DESCRIPTION,
    "version": settings.APP_VERSION,
    "contact": settings.APP_CONTACT,
    "swagger_ui_parameters": {"defaultModelsExpandDepth": -1},
    "debug": settings.DEBUG,
}
app = FastAPI(**APP_META)
v1 = FastAPI(**APP_META)

v1.middleware("http")(timeit_logger)
v1.add_middleware(RequestContextLogMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(exceptions.BadRequestException)
async def bad_request_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": exc.message},
    )


@app.exception_handler(exceptions.InternalServerError)
async def internal_server_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": exc.message},
    )


@app.exception_handler(exceptions.ForbiddenException)
async def forbidden_resource_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"error": exc.message},
    )


@app.exception_handler(exceptions.RecordNotFound)
async def record_notfound_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": exc.message},
    )


@app.exception_handler(exceptions.RecordAlreadyExists)
async def record_conflict_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error": exc.message},
    )


@app.exception_handler(exceptions.UnauthorisedError)
async def unauthorised_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": exc.message},
    )


@app.exception_handler(exceptions.NotAcceptableError)
async def not_acceptable_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        content={"error": exc.message},
    )


@app.exception_handler(exceptions.RequestTimeoutError)
async def request_timeout_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_408_REQUEST_TIMEOUT,
        content={"error": exc.message},
    )


@app.exception_handler(exceptions.GenerateReportException)
async def generate_report_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
        content={"error": exc.message},
    )


# include all routes
v1.include_router(auth.v1_router)
v1.include_router(voicemail.v1_router)
v1.include_router(voicemail_box.v1_router)
v1.include_router(voicemail_features.v1_router)
v1.include_router(voicemail_archive.v1_router)


# mount version 1 of API, similarly v2 can also be mounted if there are any
app.mount("/v1", v1)

# propagate exception handlers to sub apps
mounted_routes = [route for route in app.routes if isinstance(route, Mount)]
for exc, handler in app.exception_handlers.items():
    for m in mounted_routes:
        m.app.add_exception_handler(exc, handler)


@app.get("/ping")
async def ping():
    return {"status": "Alive"}


@app.get("/healthcheck")
async def healthcheck():
    context = {}
    context["dbstatus"] = "Passed"
    try:
        db = get_engine().connect()
        db.close()
    except Exception as e:
        logger.error(f"Exception during health check {str(e)}")
        raise exceptions.InternalServerError(
            message=constants.HEALTH_CHECK_DB_FAILED
        )
    try:
        adapter = LdapAdapter(
            username=settings.LDAP_USERNAME, password=settings.LDAP_PASSWORD
        )
        Connection(
            adapter.get_server(),
            f"{settings.LDAP_USERNAME}{settings.LDAP_DOMAIN}",
            settings.LDAP_PASSWORD,
            client_strategy=SAFE_SYNC,
            auto_bind=True,
        )
        context["ldapstatus"] = "Passed"
    except Exception as e:
        logger.error(f"Exception during health check {str(e)}")
        raise exceptions.InternalServerError(
            message=constants.HEALTH_CHECK_LDAP_FAILED
        )
    try:
        payload = json.dumps(PROTEGRITY_SAMPLE_INPUT)
        tokenize_response = requests.request(
            "POST",
            settings.TOKENIZE_URL_JSON,
            auth=(settings.PROTEGRITY_USERNAME, settings.PROTEGRITY_PASSWORD),
            headers=PROTEGRITY_HEADERS,
            data=payload,
            verify=settings.BASE_CERTIFICATE,
        )
        if tokenize_response.status_code == 200:
            context["protegrityStatus"] = "Passed"

    except Exception as e:
        logger.error(f"Exception during health check {str(e)}")
        raise exceptions.InternalServerError(
            message=constants.PROTEGRITY_SERVER_FAILED
        )
    return JSONResponse(context)
