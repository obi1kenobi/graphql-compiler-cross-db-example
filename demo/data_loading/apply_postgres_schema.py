from demo.server.config import sqlalchemy_engine
from demo.pg_models import Base


def apply_postgres_schema():
    Base.metadata.drop_all(sqlalchemy_engine)
    Base.metadata.create_all(sqlalchemy_engine)


if __name__ == '__main__':
    apply_postgres_schema()
