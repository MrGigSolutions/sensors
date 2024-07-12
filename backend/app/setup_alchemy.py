import os

from sqlalchemy import create_engine, URL

from .orm_models import Base


def setup_sql_alchemy():
    # Postgres / SqlAlchemy setup
    url = URL.create(
        drivername="postgresql",
        username=os.environ.get("PGUSER"),
        password=os.environ.get("PGPASSWORD"),
        host=os.environ.get("PGPHOST"),
        port=os.environ.get("PGPORT"),
        database=os.environ.get("PGPDATABASE"),
    )
    engine = create_engine(url)
    engine.connect()
    Base.metadata.create_all(bind=engine)
    return engine
