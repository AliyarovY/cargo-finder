from fastapi import (
    APIRouter,
    Depends,
    status,
)

from src.car import models
from src.car.services import CarService

car_router = APIRouter(
    prefix='/cars',
    tags=['cars'],
)


@car_router.post(
    '/',
    response_model=models.CarRead,
    status_code=status.HTTP_201_CREATED,
)
async def car_create(
        car_data: models.CarCreate,
        service: CarService = Depends(),
):
    return service.create(car_data)


@car_router.post(
    '/get_distance',
    response_model=models.DistanceRead
)
async def get_distance(
        distance_data: models.DistanceCreate,
        service: CarService = Depends()
):
    return service.get_distance(distance_data)


@car_router.patch(
    '/{car_id}',
    response_model=models.CarRead
)
async def car_update(
        car_id: int,
        update_data: models.CarUpdate,
        service: CarService = Depends(),
):
    return service.update(car_id, update_data)
