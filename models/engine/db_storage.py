#!/usr/bin/python3
""" Database Storage. """
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """ Database storage. """
    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new instance of DBStorage"""
        db_user = os.getenv("HBNB_MYSQL_USER")
        db_pwd = os.getenv("HBNB_MYSQL_PWD")
        db_host = os.getenv("HBNB_MYSQL_HOST")
        db_db = os.getenv("HBNB_MYSQL_DB")
        db_env = os.getenv("HBNB_ENV")
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.
            format(db_user, db_pwd, db_host, db_db),
            pool_pre_ping=True
        )
        if db_env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects in the database session."""
        obj_dict = {}
        classes = [User, State, City, Amenity, Place, Review]

        if cls:
            if isinstance(cls, str):
                cls = next((c for c in classes if c.__name__ == cls), None)
            objects = self.__session.query(cls).all()
        else:
            objects = []
            for c in classes:
                objects.extend(self.__session.query(c).all())
        for obj in objects:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the session when called to close."""
        self.__session.close()
