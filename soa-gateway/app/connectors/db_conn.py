from urllib.parse import quote

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core import logging
from app.core.config import settings
from app.core.constants import SQLALCHEMY_ENGINE_OPTIONS

logger = logging.getLogger(__name__)

DATABASE_URL = f"mysql://{settings.DB_USER}:%s@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

Base = declarative_base()


def get_engine():
    engine = create_engine(
        DATABASE_URL % quote(settings.DB_PASS),
        echo=False,
        isolation_level=SQLALCHEMY_ENGINE_OPTIONS.get("isolation_level"),
        pool_size=SQLALCHEMY_ENGINE_OPTIONS.get("pool_size"),
        pool_recycle=SQLALCHEMY_ENGINE_OPTIONS.get("pool_recycle"),
        pool_pre_ping=SQLALCHEMY_ENGINE_OPTIONS.get("pool_pre_ping"),
        pool_timeout=SQLALCHEMY_ENGINE_OPTIONS.get("pool_timeout"),
    )
    return engine


SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=get_engine()
)


def get_db():
    db = SessionLocal()
    try:
        logger.info("DB connection opened")
        yield db
    finally:
        logger.info("Closing DB connection")
        db.close()
