import logging

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import Mount

from app.core import constants, exceptions
from app.core.config import settings

from .api import cognitive

logging.basicConfig(
    format="%(levelname)s - %(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
)

logger = logging.getLogger(__name__)

app = FastAPI(**constants.APP_META)

v1 = FastAPI(**constants.APP_META)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include all routes
v1.include_router(cognitive.v1_router)

app.mount("/v1", v1)


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


# propagate exception handlers to sub apps
mounted_routes = [route for route in app.routes if isinstance(route, Mount)]
for exc, handler in app.exception_handlers.items():
    for m in mounted_routes:
        m.app.add_exception_handler(exc, handler)


@app.get("/ping")
async def ping():
    logger.info("Ping success")
    return {"status": "Alive"}
