#!/usr/bin/python3
""" holds class Category"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class OrderItem(BaseModel, Base):
    """Representation of a Category """
    __tablename__ = 'order_items'
    item_quantity = Column(Integer, default=1)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
