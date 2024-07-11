from sqlalchemy import create_engine, URL

from .orm_models import Base


def setup_sql_alchemy():
    # Postgres / SqlAlchemy setup
    url = URL.create(
        drivername="postgresql",
        username="backend",
        password="hello",
        host="db",
        port=5432,
        database="sensors"
    )
    engine = create_engine(url)
    engine.connect()
    Base.metadata.create_all(bind=engine)
    return engine
