from base.utils import full_up_cars
from config import BASE_DIR
from database import get_session, engine
from location.services import LocationService
from tables import Base

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    with open(BASE_DIR / 'uszips.csv') as csvfile:
        LocationService().import_csv_to_db(csvfile)

    full_up_cars(next(get_session()))
