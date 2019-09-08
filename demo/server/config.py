import backoff
from grift import BaseConfig, ConfigProperty, EnvLoader
import psycopg2
from psycopg2.extras import DictCursor
from pyorient.ogm import Config, Graph
from schematics.types import StringType
from sqlalchemy import create_engine


class ServerConfig(BaseConfig):
    POSTGRES_DB = ConfigProperty(property_type=StringType())
    POSTGRES_USER = ConfigProperty(property_type=StringType())
    POSTGRES_PASSWORD = ConfigProperty(property_type=StringType(), exclude_from_varz=True)
    POSTGRES_HOST = ConfigProperty(property_type=StringType())
    ORIENTDB_DB = ConfigProperty(property_type=StringType())
    ORIENTDB_USER = ConfigProperty(property_type=StringType())
    ORIENTDB_PASSWORD = ConfigProperty(property_type=StringType(), exclude_from_varz=True)
    ORIENTDB_HOST_AND_PORT = ConfigProperty(property_type=StringType())


server_config = ServerConfig([EnvLoader()])


def get_graph_client():
    db_url = 'plocal://' + server_config.ORIENTDB_HOST_AND_PORT + '/' + server_config.ORIENTDB_DB
    graph = Graph(Config.from_url(
        db_url, server_config.ORIENTDB_USER, server_config.ORIENTDB_PASSWORD), strict=True)
    return graph


@backoff.on_exception(
    backoff.fibo, psycopg2.OperationalError, max_tries=10
)
def get_postgres_client(
    dbname=server_config.POSTGRES_DB,
    user=server_config.POSTGRES_USER,
    password=server_config.POSTGRES_PASSWORD,
    host=server_config.POSTGRES_HOST,
):
    return psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, cursor_factory=DictCursor
    )


sqlalchemy_engine = create_engine('postgresql://', creator=get_postgres_client)
