from asyncio import sleep

from sqlalchemy.orm import Session

from src import tables
from src.location.logic import get_random_location


async def set_car_random_location_id(seconds=180):
    session = Session()
    cars = session.query(tables.Car).all()
    try:
        while True:
            for car in cars:
                rnd_locaiton_id = get_random_location().id
                car.location_id = rnd_locaiton_id
            sleep(seconds)
    finally:
        session.commit()
        session.close()
