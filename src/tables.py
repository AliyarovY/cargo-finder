import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, validates

Base = declarative_base()


class Location(Base):
    __tablename__ = 'location'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    city = sa.Column(sa.String, nullable=False)
    state = sa.Column(sa.String, nullable=False)
    zip = sa.Column(sa.String, nullable=False, unique=True)
    lat = sa.Column(sa.Numeric(10, 5))
    lng = sa.Column(sa.Numeric(10, 5))

    def __repr__(self):
        return f'{self.state} | {self.city} | {self.zip}'


class Car(Base):
    __tablename__ = 'car'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    unique_number = sa.Column(sa.String, unique=True, nullable=False)
    location_id = sa.Column(sa.Integer, sa.ForeignKey('location.id'), nullable=False)
    capacity = sa.Column(
        sa.Integer,
        sa.CheckConstraint('capacity >= 1 AND capacity <= 1000'),
        nullable=False,
    )

    def __repr__(self):
        return self.unique_number


class Cargo(Base):
    __tablename__ = 'cargo'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    pick_up_location_id = sa.Column(sa.Integer, sa.ForeignKey('location.id'), nullable=False)
    delivery_location_id = sa.Column(sa.Integer, sa.ForeignKey('location.id'), nullable=False)
    description = sa.Column(sa.TEXT, nullable=False)
    weight = sa.Column(
        sa.Integer,
        sa.CheckConstraint('weight >= 1 AND weight <= 1000'),
        nullable=False,
    )

    def __repr__(self):
        return self.description

