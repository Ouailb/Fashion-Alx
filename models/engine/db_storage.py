#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from models.base_model import Base
from models.order_items import OrderItem
from models.order import Order
from models.product import Product
from models.user import User
from models.cart import Cart
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {
    "Product": Product, "OrderItem": OrderItem,
    "Order": Order, "User": User, "Cart": Cart
}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instatntiates database engine"""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host_name = getenv('HBNB_MYSQL_HOST')
        db_name = getenv('HBNB_MYSQL_DB')
        db_url = f"mysql+mysqldb://{user}:{password}@{host_name}/{db_name}"

        self.__engine = create_engine(db_url, pool_pre_ping=True)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def all(self, cls=None, order_asc=None, order_desc=None, filter=None):
        """query on the current database session"""
        new_dict = {}
        i = 1
        if filter and isinstance(filter, dict) and len(filter) == 1:
            f_key, f_value = next(iter(filter.items()))
        else:
            f_key = None
        for clss in classes.values():
            if cls is None or cls is clss:
                if cls and order_asc and hasattr(cls, order_asc):
                    if f_key and hasattr(cls, f_key):
                        objs = self.__session.query(cls).filter(getattr(cls, f_key) == f_value).order_by(getattr(cls, order_asc)).all()
                    else:
                        objs = self.__session.query(cls).order_by(getattr(cls, order_asc)).all()

                elif cls and order_desc and hasattr(cls, order_desc):
                    if f_key and hasattr(cls, f_key):
                        objs = self.__session.query(cls).filter(getattr(cls, f_key) == filter[f_key]).order_by(getattr(cls, order_desc).desc()).all()
                    else:
                        objs = self.__session.query(cls).order_by(getattr(cls, order_desc).desc()).all()

                else:
                    if f_key and hasattr(cls, f_key):
                        objs = self.__session.query(cls).filter(getattr(cls, f_key) == filter[f_key]).all()
                    else:
                        objs = self.__session.query(cls).all()
                for obj in objs:
                    key = f'(N°{i}) ' + obj.__class__.__name__ + '.' + str(obj.id)
                    new_dict[key] = obj
                    i += 1
        return (new_dict)

    def count(self, cls=None):
        """count all classes"""
        cpt = 0
        for clss in classes:
            if cls is None or cls is classes[clss]:
                objs = self.__session.query(classes[clss]).all()
                cpt += len(objs)
        return cpt

    def get_by_id(self, cls, id):
        """get object by class and id"""
        for clss in classes:
            if cls is classes[clss]:
                result = self.__session.query(cls).filter(cls.id == id).first()
                if result:
                    return result
        return None
    
    def get_user_by_email(self, email):
        """get user by email"""
        user = self.__session.query(User).filter(User.email == email).first()
        if user:
            return user
        return None

    def filter_product(self, c_type, c_name, order_asc=None, order_desc=None):
        """filter products by category"""
        new_dict = {}
        i = 1
        if order_asc and hasattr(Product, order_asc):
            objs = self.__session.query(Product).filter(Product.category_type == c_type).filter(Product.category_name == c_name).order_by(getattr(Product, order_asc)).all()
        elif order_desc and hasattr(Product, order_desc):
            objs = self.__session.query(Product).filter(Product.category_type == c_type).filter(Product.category_name == c_name).order_by(getattr(Product, order_desc).desc()).all()
        else:
            objs = self.__session.query(Product).filter(Product.category_type == c_type).filter(Product.category_name == c_name).all()
        for obj in objs:
            key = f'(N°{i}) ' + obj.__class__.__name__ + '.' + str(obj.id)
            new_dict[key] = obj
            i += 1
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
