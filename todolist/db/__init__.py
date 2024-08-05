import urllib
from logging import LoggerAdapter
from typing import Dict

from oslo_config import cfg
from oslo_log import log
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CONF = cfg.CONF
LOG: LoggerAdapter = log.getLogger(__name__)

DB_SESSION_LOCAL: sessionmaker


def setup_db() -> None:
    if CONF.database.connection.startswith("sqlite"):
        engine = create_engine(
            CONF.database.connection,
            pool_pre_ping=True,
            connect_args={"check_same_thread": False},
        )
    else:
        engine_cfg: Dict[str, int] = {}
        engine_cfg["pool_size"] = CONF.database.max_pool_size
        engine_cfg["max_overflow"] = CONF.database.max_overflow

        connection = connection_database()

        engine = create_engine(connection, pool_pre_ping=True, **engine_cfg)

    global DB_SESSION_LOCAL
    DB_SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    LOG.info("DB setup complete")


def connection_database() -> str:
    connection = CONF.database.connection
    right = connection.rfind("@", 1)
    left = connection.find(":", connection.find(":") + 1)
    connection = (
        connection[: left + 1]
        + urllib.parse.quote_plus(connection[left + 1 : right])
        + connection[right:]
    )
    return connection
