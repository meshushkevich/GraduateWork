import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from src.logger import log_info

if Path(".env").exists():
    log_info("Loading environment variables from .env file")
    load_dotenv()
else:
    log_info("No .env file found")
USER = os.getenv("PGSQL_USER")
PASSWORD = os.getenv("PGSQL_PASSWORD")
HOSTNAME = os.getenv("PGSQL_HOSTNAME")
DATABASE_NAME = os.getenv("PGSQL_DATABASE")
if not (USER and PASSWORD and HOSTNAME and DATABASE_NAME):
    raise ValueError("Environment variables for database not set")

_engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOSTNAME}/{DATABASE_NAME}"
)
log_info("Database connection established!")


def get_engine():
    return _engine
