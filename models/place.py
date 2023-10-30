#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, Table
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    __tablename__ = 'places'
    reviews = relationship("Review", cascade="all, delete-orphan",
                           backref="place")
    amenities = relationship("Amenity", secondary=place_amenity,
                            viewonly=False, back_populates="place_amenities")

    @property
    def amenities(self):
        """ Getter attribute for amenities """
        return self.amenity_ids

    @amenities.setter
    def amenities(self, amenity):
        """ Setter attribute for amenities """
        if isinstance(amenity, Amenity):
            self.amenity_ids.append(amenity.id)
