#!/usr/bin/python3
""" holds class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, CheckConstraint, Float
from sqlalchemy.orm import relationship




class Product(BaseModel, Base):
    """Representation of a user"""
    __tablename__ = 'products'
    title = Column(String(256), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(1024), nullable=False)
    discount = Column(Integer, CheckConstraint('discount <= 100'), default=0)
    category_name = Column(String(127), nullable=False)
    category_type = Column(String(127), nullable=False)
    img_url = Column(String(128))
