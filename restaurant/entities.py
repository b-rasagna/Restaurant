import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import JSONType

from restaurant.util import MiscUtil

Base = declarative_base()

class Tables(Base):
    """
    Tables entity

    :param id: id of the table
    :type id: int
    :param available: availability of the table
    :type available: boolean
    :param customer_name: name of the customer
    :type customer_name: str
    :param customer_mobile: mobile number of the customer
    :type customer_mobile: integer
    :param order_id: id of the order
    :type order_id: int
    :type description: boolean
    """
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True, autoincrement=True)
    available = Column(Boolean)
    customer_id = Column(Integer)
    customer_name = Column(String(128))
    customer_mobile = Column(String(10))
    order_id = Column(Integer, ForeignKey("orders.id"))
    
    def __init__(self, available, customer_id, customer_name, customer_mobile, order_id):
        """
        Constructor function
        """
        self.available = available
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.customer_mobile = customer_mobile
        self.order_id = order_id

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Orders(Base):
    """
    Orders entity

    :param id: id of the order
    :type id: int
    :param status: status of the order
    :type status: str
    :param items: list of the items ordered along with quantity
    :type items: dict
    :param amount: total amount of items ordered
    :type amount: float
    :param payment: status of the payment
    :type payment: boolean
    :param date: date and time of the order
    :type date: class:`datetime.datetime`
    """
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(128))
    items = Column(JSONType)
    amount = Column(Float)
    payment = Column(Boolean)
    date = Column(DateTime)
    table_id = Column(Integer, ForeignKey("tables.id"))
    time = Column(String)

    def __init__(self, status, items, amount, payment, table_id, time):
        """
        Constructor function
        """
        self.status = status
        self.items = items
        self.amount = amount
        self.payment = payment
        current_date = datetime.datetime.utcnow()
        self.date = current_date
        self.table_id = table_id
        self.time = time

    def to_dict(self):
        return {c.name: MiscUtil().getISODate(getattr(self, c.name)) if c.name == "date" else getattr(self, c.name) for c in self.__table__.columns}

class Items(Base):
    """
    Item entity

    :param id: id of the item
    :type id: int
    :param name: name of the item
    :type name: str
    :param price: price of the item
    :type price: str
    :param time: time taken to cook
    :type time: class:`time.time`
    :param available: availability of the item 
    :type available: boolean
    """
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), unique=True)
    price = Column(Float)
    time = Column(Integer)
    available = Column(Boolean)

    def __init__(self, name, price, time, available):
        """
        Constructor function
        """
        self.name = name
        self.price = price
        self.time = time
        self.available = available

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Customers(Base):
    """
    Customers entity

    :param id: id of the customer
    :type id: int
    :param name: name of the customer
    :type name: str
    :param mobile: mobile number of the customer
    :type mobile: int
    :param order_id: id of the order
    :type order_id: int
    :param date: date and time when customer visited
    :type date: class:`datetime.datetime`
    """
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128))
    mobile = Column(String(10))
    order_id = Column(Integer, ForeignKey("orders.id"))
    date = Column(DateTime)

    def __init__(self, name, mobile, order_id):
        """
        Constructor function
        """
        self.name = name
        self.mobile = mobile
        self.order_id = order_id
        current_date = datetime.datetime.utcnow()
        self.date = current_date

    def to_dict(self):
        return {c.name: MiscUtil().getISODate(getattr(self, c.name)) if c.name == "date" else getattr(self, c.name) for c in self.__table__.columns}