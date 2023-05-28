import re

from pydantic import BaseModel, validator, Field

from src import tables
from src.database import get_session
from src.location.db_logic import get_random_location
from src.location.models import LocationRead


class BaseCarModel(BaseModel):
    unique_number: str
    capacity: int


class ChangeBase(BaseCarModel):
    @validator('unique_number')
    def check_unique_number(cls, v):
        session = next(get_session())
        numbers = {car.unique_number for car in session.query(tables.Car).all()}
        session.close()
        if v in numbers:
            raise ValueError('Number not unique.')

        exception_msg = f'Invalid unique number {v}.'
        valid_value = re.search(r'^\d{4}[A-Z]', v)
        if valid_value is None or valid_value.group() != v:
            raise ValueError(exception_msg)

        return v

    @validator('capacity')
    def check_capacity_is_valid(cls, v):
        mn, mx = 0, 1001
        if not mn <= v <= mx:
            raise ValueError(f'Capacity must be greater than {mn} and less than {mx} .')
        return v


class CarCreate(ChangeBase):
    location: LocationRead = Field(default_factory=get_random_location)


class CarRead(BaseCarModel):
    id: int
    location: LocationRead

    class Config:
        orm_mode = True


class DistanceRead(BaseModel):
    miles: int


class DistanceCreate(BaseModel):
    car_id: int
    location_id: int


class CarWithDistance(BaseModel):
    unique_number: str
    miles_distance: int


class CarUpdate(ChangeBase):
    zip: str | None = None
    unique_number: str | None = None
    location_id: int | None = None
    capacity: int | None = None
