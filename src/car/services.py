from fastapi import HTTPException

from geopy.distance import distance
from starlette import status

from location.models import LocationRead
from src import tables
from src.base.services import APIServiceMixin
from src.base.utils import get_by
from src.car import models
from src.location.logic import get_location, get_location_by, get_random_location


class CarService(APIServiceMixin):
    def create(self, car_data: models.CarCreate) -> models.CarRead:
        location = LocationRead.from_orm(get_random_location())
        location_id = location.id
        car = tables.Car(**car_data.dict(), location_id=location_id)
        self.session.add(car)
        self.session.commit()
        return models.CarRead(id=car.id, location=location, **car_data.dict())

    def get_distance(self, distance_data: models.DistanceCreate) -> dict[str, int]:
        car_location = self._get_location_by_car(distance_data.car_id)
        main_location = get_location(
            distance_data.location_id,
            self.session,
        )
        main_point = (main_location.lat, main_location.lng)
        car_point = (car_location.lat, car_location.lng)
        res_distance = distance(main_point, car_point).miles
        return models.DistanceRead(distance=res_distance)

    def update(self, car_id: int, update_data) -> tables.Car:
        update_data = {k: v for k, v in update_data.dict().items() if not v is None}
        car = get_by(tables.Car, self.session, id=car_id)

        if is_zip_used := ('zip' in update_data):
            zip = update_data['zip']
            car.location_id = get_location_by(self.session, zip=zip).id

        for k, v in update_data.items():
            if is_zip_used and k == 'location_id':
                continue
            setattr(car, k, v)

        self.session.commit()
        response_car = models.CarRead(
            id=car.id,
            unique_number=car.unique_number,
            capacity=car.capacity,
            location=get_location(car.location_id, self.session)
        )
        return response_car

    def _get_location_by_car(self, car_id: int) -> tables.Location:
        car = self._get(car_id)
        location = get_location(car.location_id, self.session)
        return location

    def _get(self, id: int) -> tables.Car:
        car = (
            self.session
            .query(tables.Car)
            .filter_by(id=id)
        ).first()
        if car is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Car with {id} id is not found.'
            )
        return car
