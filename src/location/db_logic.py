import random

from fastapi import HTTPException
from geopy.distance import distance, geodesic
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session
from starlette import status

from src import tables
from src.database import get_session
from src.location.models import LocationRead


def get_all_locations() -> list[tables.Location]:
    session = next(get_session())
    res = session.query(tables.Location).all()
    session.close()
    return res


def get_random_location(locations: list[tables.Location] = get_all_locations()) -> LocationRead:
    random_location = random.choice(locations)
    return random_location


def get_location(id: int, session: Session) -> tables.Location:
    locaiton = (
        session
        .query(tables.Location)
        .filter_by(id=id)
    ).first()
    if locaiton is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Location with {id} id is not found.',
        )
    return locaiton


def get_location_by(session: Session, **kwargs) -> tables.Location:
    exp = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Location is not found.',
    )
    try:
        locaiton = (
            session
            .query(tables.Location)
            .filter_by(**kwargs)
        ).first()
    except ProgrammingError as err:
        raise exp
    if locaiton is None:
        raise exp
    return locaiton


def get_distanse_beteween_locations(
        frst_location: tables.Location,
        sec_location: tables.Location,
) -> geodesic:
    frst_point = (frst_location.lat, frst_location.lng,)
    sec_point = (sec_location.lat, sec_location.lng,)

    return distance(frst_point, sec_point)


def get_distanse_beteween_locations_by_id(frst_loc_id: int, sec_loc_id: int, session: Session) -> geodesic:
    frst_location = get_location(frst_loc_id, session)
    sec_location = get_location(sec_loc_id, session)

    return get_distanse_beteween_locations(frst_location, sec_location)
