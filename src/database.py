from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.base.utils import full_up_cars
from src.tables import Base
from src.config import settings

engine = create_engine(
    settings.db_url,
)

Session = sessionmaker(
    engine,
)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    full_up_cars()
