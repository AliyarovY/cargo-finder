from typing import List

from src import tables
from src.base.services import APIServiceMixin
from src.base.utils import get_by
from src.car.models import CarWithDistance
from src.cargo import models
from src.location.logic import get_location_by, get_distanse_beteween_locations_by_id, get_location
from src.location.models import LocationRead


class CargoService(APIServiceMixin):
    MAX_CARGO_CAR_BETWEEN_DISTANCE = 450

    def create(
            self,
            cargo_data: models.CargoCreate
    ) -> models.CargoRead:
        pick_up_location_id = get_location_by(
            self.session,
            zip=cargo_data.pick_up_zip
        ).id
        delivery_location_id = get_location_by(
            self.session,
            zip=cargo_data.delivery_zip
        ).id
        cargo = tables.Cargo(
            pick_up_location_id=pick_up_location_id,
            delivery_location_id=delivery_location_id,
            description=cargo_data.description,
            weight=cargo_data.weight,
        )
        self.session.add(cargo)
        self.session.commit()

        cargo_detail = self._extract_detail_from_table(cargo)
        return models.CargoRead(id=cargo.id, **cargo_detail.dict())

    def list(
            self,
            query_wght: int | None,
            query_distance: bool,
    ) -> list[models.CargoInList]:
        query_responces = (
            self.session
            .query(
                tables.Cargo
            )
        ).all()

        cargos = []
        for cargo in query_responces:
            if any([
                not query_wght is None and cargo.weight != query_wght,
            ]):
                continue

            nearby_cars = self._get_nearby_cars(cargo.pick_up_location_id)

            # set more info
            if any(x for x in [query_wght, query_distance]):
                more = models.MoreInListInfo()
                if query_wght:
                    more.weight = query_wght
                if query_distance:
                    more.nearby_cars_mile_disctances = [
                        get_distanse_beteween_locations_by_id(
                            car.location_id, cargo.pick_up_location_id,
                            self.session)
                        for car in nearby_cars
                    ]

            else:
                more = None

            # prepare
            to_be_append = models.CargoInList(
                id=cargo.id,
                pick_up_location=get_location(cargo.pick_up_location_id, self.session),
                delivery_location=get_location(cargo.delivery_location_id, self.session),
                nearby_cars_count=len(nearby_cars),
                more=more
            )
            cargos.append(to_be_append)

        return cargos

    def detail(self, cargo_id: int) -> models.CargoDetailWithCars:
        cargo = get_by(tables.Cargo, self.session, id=cargo_id)
        cargo_detail = self._extract_detail_from_table(cargo)
        cars = self._get_cars_for_detail(cargo_detail)

        output = models.CargoDetailWithCars(
            **cargo_detail.dict(),
            cars=cars,
        )
        return output

    def update(self, cargo_id: int, update_data: models.CargoUpdate) -> models.CargoRead:
        cargo = get_by(tables.Cargo, self.session, id=cargo_id)
        for k, v in update_data.dict().items():
            if v is None:
                continue
            setattr(cargo, k, v)
        self.session.commit()
        return self._get(cargo)

    def delete(self, cargo_id: int) -> models.CargoRead:
        cargo = get_by(tables.Cargo, self.session, id=cargo_id)
        output = self._get(cargo)
        self.session.delete(cargo)
        self.session.commit()
        return output

    def _get(self, cargo: tables.Cargo) -> models.CargoRead:
        output = models.CargoRead(
            id=cargo.id,
            weight=cargo.weight,
            description=cargo.description,
            pick_up_location=get_location(cargo.pick_up_location_id, self.session),
            delivery_location=get_location(cargo.delivery_location_id, self.session),
        )
        return output

    def _get_cars_for_detail(self, cargo_detail: models.CargoDetail) -> List[models.CarWithDistance]:
        cars = self.session.query(tables.Car).all()
        pick_up_location = cargo_detail.pick_up_location
        cars_list = [
            CarWithDistance(
                unique_number=car.unique_number,
                distance=get_distanse_beteween_locations_by_id(
                    pick_up_location.id, car.location_id,
                    session=self.session,
                )
            )
            for car in cars
        ]
        return cars_list

    def _extract_detail_from_table(self, cargo: tables.Cargo) -> models.CargoDetail:
        pick_up_location = get_location(cargo.pick_up_location_id, self.session)
        delivery_location = get_location(cargo.delivery_location_id, self.session)

        pick_up_location_data = LocationRead.from_orm(pick_up_location)
        delivery_location_data = LocationRead.from_orm(delivery_location)

        cargo_detail = models.CargoDetail(
            description=cargo.description,
            weight=cargo.weight,
            pick_up_location=pick_up_location_data,
            delivery_location=delivery_location_data,
        )
        return cargo_detail

    def _get_nearby_cars(
            self,
            pick_up_location_id: int,
    ) -> int:
        query = (
            self.session
            .query(tables.Car)
            .all()
        )
        return [
            car
            for car in query
            if get_distanse_beteween_locations_by_id(car.location_id, pick_up_location_id,
                                                     session=self.session) <= self.MAX_CARGO_CAR_BETWEEN_DISTANCE
        ]
