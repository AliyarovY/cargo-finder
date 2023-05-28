import csv

from src.base.services import APIServiceMixin
from src.config import BASE_DIR
from src.database import get_session
from src.location import models
from src import tables


class LocationService(APIServiceMixin):
    report_fields = [
        "zip", "lat", "lng", "city", "state_id", "state_name",
        "zcta", "parent_zcta", "population", "density",
        "county_fips", "county_name", "county_weights",
        "county_names_all", "county_fips_all", "imprecise", "military",
        "timezone"
    ]

    def __init__(self):
        self.session = next(get_session())

    def import_to_db_csv(self, file):
        reader = csv.DictReader(
            file,
            fieldnames=self.report_fields,
        )
        next(reader, None)  # Skip the header
        locations_data = [
            models.LocationCreate(
                city=row['city'],
                state=row['state_name'],
                zip=row['zip'],
                lat=row['lat'],
                lng=row['lng'],
            )
            for row in reader
        ]
        self.create_many(locations_data)

    def create_many(
            self,
            locations_data: list[models.LocationCreate]
    ) -> list[tables.Location]:
        locations = [
            tables.Location(
                **location_data.dict()
            )
            for location_data in locations_data
        ]
        self.session.add_all(locations)
        self.session.commit()
        return locations


if __name__ == '__main__':
    with open(BASE_DIR / 'uszips.csv') as csvfile:
        LocationService().import_to_db_csv(csvfile)
