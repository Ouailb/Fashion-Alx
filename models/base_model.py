#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel:
    """A base class for all models"""

    id = Column(Integer, primary_key=True, autoincrement=True)

    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            time = '%Y-%m-%dT%H:%M:%S.%f'
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            for key, value in kwargs.items():
                if key not in ["__class__", "created_at", "updated_at"]:
                    if hasattr(self, key):
                        setattr(self, key, value)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        if "password" in dictionary:
            del dictionary["password"]
        if "_sa_instance_state" in dictionary:
            del dictionary["_sa_instance_state"]

        for key, value in dictionary.items():
            if isinstance(value, datetime):
                dictionary[key] = datetime.isoformat(value)
        return dictionary

    def delete(self):
        """delete the current instance from the storage"""
        from models import storage
        storage.delete(self)

    def __str__(self):
        """Returns a string representation of the instance"""
        dictionary_repr = "__repr__ ==>\n"
        for key, value in self.to_dict().items():
            dictionary_repr += f'\t{key}: {value}\n'
        return dictionary_repr
