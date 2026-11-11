from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

if __package__:
    from .models import Base
else:
    from models import Base

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


def build_database_url() -> str | URL:
    mysql_url = os.getenv("MYSQL_DATABASE_URL")
    if mysql_url:
        return mysql_url

    mysql_settings = {
        "MYSQL_USER": os.getenv("MYSQL_USER"),
        "MYSQL_PASSWORD": os.getenv("MYSQL_PASSWORD"),
        "MYSQL_HOST": os.getenv("MYSQL_HOST"),
        "MYSQL_PORT": os.getenv("MYSQL_PORT"),
        "MYSQL_DATABASE": os.getenv("MYSQL_DATABASE"),
    }
    if any(value is not None for value in mysql_settings.values()):
        required_settings = ("MYSQL_USER", "MYSQL_HOST", "MYSQL_PORT", "MYSQL_DATABASE")
        missing_settings = [
            key
            for key in required_settings
            if not mysql_settings[key]
        ]
        if mysql_settings["MYSQL_PASSWORD"] is None:
            missing_settings.append("MYSQL_PASSWORD")

        if missing_settings:
            missing = ", ".join(missing_settings)
            raise RuntimeError(f"Configuração MySQL incompleta no .env. Defina: {missing}.")

        return URL.create(
            "mysql+pymysql",
            username=mysql_settings["MYSQL_USER"],
            password=mysql_settings["MYSQL_PASSWORD"],
            host=mysql_settings["MYSQL_HOST"],
            port=int(mysql_settings["MYSQL_PORT"]),
            database=mysql_settings["MYSQL_DATABASE"],
        )

    sqlite_path = ROOT_DIR / "appcursinho.db"
    return f"sqlite:///{sqlite_path}"


def create_session_factory():
    database_url = build_database_url()
    engine_kwargs = {"future": True}

    if isinstance(database_url, str) and database_url.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}

    engine = create_engine(database_url, **engine_kwargs)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return SessionLocal


SessionLocal = create_session_factory()


def init_db() -> None:
    engine = SessionLocal.kw["bind"]
    Base.metadata.create_all(bind=engine)
