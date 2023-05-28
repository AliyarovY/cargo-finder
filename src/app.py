from fastapi import FastAPI

from src.car.api import car_router
from src.cargo.api import cargo_router
from src.config import settings

app = FastAPI(
    title='Cargo-Finder',
    version='1.0.0',
    debug=settings.debug,
)

app.include_router(car_router)
app.include_router(cargo_router)
