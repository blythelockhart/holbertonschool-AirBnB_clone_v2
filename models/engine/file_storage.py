#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from datetime import datetime


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            return {k: v for k, v in self.__objects.items()
                    if isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, 'w') as f:
            temp = {}
            temp.update(self.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            with open(self.__file_path) as f:
                temp = json.load(f)
                time = "%Y-%m-%dT%H:%M:%S.%f"

                for val in temp.values():
                    class_name = val.get('__class__')
                    if class_name:
                        del val['__class__']
                        for key, value in val.items():
                            if key in ('created_at', 'updated_at'):
                                val[key] = datetime.strptime(value, time)
                        self.new(eval(class_name)(**val))
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass

    def delete(self, obj=None):
        """Deletes an object from __objects if it's inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """ Close the file and deserialize the JSON file to objects. """ 
        self.reload()
