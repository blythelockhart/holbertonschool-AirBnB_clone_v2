#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
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
    amenities = relationship("Amenity", secondary="place_amenity",
                             viewonly=False,
                             back_populates="place_amenities")

#    if getenv('HBNB_TYPE_STORAGE', None) != 'db':
#        @property
#        def reviews(self):
#            """A list of Review instances with place_id equal to the current Place.id"""
#            from models import storage
#            review_list = []
#            all_reviews = storage.all(Review)
#            for review in all_reviews.values():
#                if review.place_id == self.id:
#                    review_list.append(review)
#            return review_list
#
#        @property
#        def amenities(self):
#            """Getter for amenities attribute"""
#            from models import storage
#            amen_list = []
#            all_amenities = storage.all(Amenity)
#            for amenity in all_amenities.values():
#                if amenity.id == self.amenity_ids:
#                    amen_list.append(amenity)
#            return amen_list
#
#        @amenities.setter
#        def amenities(self, amenity):
#            """Setter for amenities attribute"""
#            if isinstance(amenity, Amenity):
#                if amenity.id not in self.amenity_ids:
#                    self.amenity_ids.append(amenity.id)
