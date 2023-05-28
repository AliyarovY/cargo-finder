from pydantic import BaseModel
from pydantic.types import Decimal


class BaseLocationModel(BaseModel):
    city: str
    state: str
    zip: str
    lat: Decimal
    lng: Decimal


class LocationCreate(BaseLocationModel):
    ...


class LocationRead(BaseLocationModel):
    id: int

    class Config:
        orm_mode=True


