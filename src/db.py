from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if __package__:
    from .models import Base
else:
    from models import Base

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent

def build_database_url() -> str:
    mysql_url = os.getenv("MYSQL_DATABASE_URL")
    if mysql_url:
        return mysql_url

    sqlite_path = ROOT_DIR / "appcursinho.db"
    return f"sqlite:///{sqlite_path}"


def create_session_factory():
    database_url = build_database_url()
    engine_kwargs = {"future": True}

    if database_url.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}

    engine = create_engine(database_url, **engine_kwargs)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return SessionLocal


SessionLocal = create_session_factory()


def init_db() -> None:
    engine = SessionLocal.kw["bind"]
    Base.metadata.create_all(bind=engine)
