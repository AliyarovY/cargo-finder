import random
import string

from fastapi import HTTPException
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session
from starlette import status

from src import tables

def get_random_orm_obj(orm_table, session: Session) -> tables.Base:
    output = random.choice(session.query(orm_table).all())
    return output


def get_by(table: tables.Base, session: Session, **kwargs) -> tables.Base:
    exp = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'{table} is not found.',
    )
    try:
        output = (
            session
            .query(table)
            .filter_by(**kwargs)
        ).first()
    except ProgrammingError:
        raise exp
    if output is None:
        raise exp
    return output


def full_up_cars(session, cnt: int = 20) -> None:
    nbrs = {car.unique_number for car in session.query(tables.Car.unique_number).all()}
    get_un_nb = lambda: str(random.randint(1000, 9999)) + random.choice(string.ascii_uppercase)
    try:
        for _ in range(cnt):
            while True:
                unique_number = get_un_nb()
                if unique_number in nbrs:
                    continue
                break
            location_id = get_random_orm_obj(tables.Location, session).id
            capacity = random.randint(1, 1000)
            car = tables.Car(location_id=location_id, unique_number=unique_number, capacity=capacity)
            session.add(car)
            session.commit()
            nbrs.add(car.unique_number)
    finally:
        session.close()
