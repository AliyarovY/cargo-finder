from pydantic import BaseModel, Field, validator, root_validator

from src.car.models import DistanceRead, CarWithDistance
from src.location.models import LocationRead


class BaseCargoModel(BaseModel):
    description: str
    weight: int

    @validator('weight')
    def check_weight(cls, v):
        mn, mx = 0, 1001
        if not 1 <= v <= 1000:
            raise ValueError(f'weight must be greater than {mn} and less than {mx} .')
        return v


class CargoCreate(BaseCargoModel):
    pick_up_zip: str
    delivery_zip: str

    @root_validator
    def check_passwords_match(cls, values):
        k1, k2 = 'pick_up_zip', 'delivery_zip'
        if values.get(k1) == values.get(k2):
            raise ValueError(f'{k1} and {k2} should not be the same.')
        return values


class CargoDetail(BaseCargoModel):
    pick_up_location: LocationRead
    delivery_location: LocationRead


class CargoDetailWithCars(CargoDetail):
    cars: list[CarWithDistance]


class CargoRead(CargoDetail):
    id: int

    class Config:
        orm_mode = True


class MoreInListInfo(BaseModel):
    weight: int | None = None
    nearby_cars_mile_disctances: list[int] | None = None


class CargoInList(BaseModel):
    id: int
    pick_up_location: LocationRead
    delivery_location: LocationRead
    nearby_cars_count: int
    more: MoreInListInfo | None = None


class CargoUpdate(BaseCargoModel):
    description: str | None = None
    weight: int | None = None
