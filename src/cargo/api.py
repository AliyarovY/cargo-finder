from fastapi import (
    APIRouter,
    Depends,
    status, Query,
)

from src.cargo import models
from src.cargo.services import CargoService

cargo_router = APIRouter(
    prefix='/cargo',
    tags=['cargo'],
)


@cargo_router.post(
    '/',
    response_model=models.CargoRead,
    status_code=status.HTTP_201_CREATED,
)
async def cargo_create(
        cargo_data: models.CargoCreate,
        service: CargoService = Depends(),
):
    return service.create(cargo_data)


@cargo_router.get(
    '/list',
    response_model=list[models.CargoInList],
)
async def get_cargo_list(
        service: CargoService = Depends(),
        weight: int | None = Query(default=None),
        disctance: bool = Query(default=False),
):
    return service.list(weight, disctance)


@cargo_router.get(
    '/{cargo_id}',
    response_model=models.CargoDetailWithCars,
)
async def get_cargo_with_cars(
        cargo_id: int,
        service: CargoService = Depends(),
):
    return service.detail(cargo_id)


@cargo_router.patch(
    '/{cargo_id}',
    response_model=models.CargoRead,
)
async def cargo_update(
        cargo_id: int,
        update_data: models.CargoUpdate,
        service: CargoService = Depends(),
):
    return service.update(cargo_id, update_data)


@cargo_router.delete(
    '/{cargo_id}',
    response_model=models.CargoRead,
)
async def cargo_delete(
        cargo_id: int,
        service: CargoService = Depends(),
):
    return service.delete(cargo_id)
