from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey, DateTime, VARCHAR, Text, JSON
from .connection_db import Base
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import enum


class FuelVariant(enum.Enum):
    petrol = 'petrol'
    diesel = 'diesel'


class GearType(enum.Enum):
    manual = 'manual'
    automatic = 'automatic'


class Dealers(Base):
    __tablename__ = 'dealers'

    dealer_id = Column(Integer, primary_key=True, index=True)
    dealer_name = Column(String(30), nullable=False)
    dealer_mobile = Column(Integer, unique=True, nullable=True)
    dealer_password = Column(VARCHAR(100), nullable=False)
    dealer_address = Column(VARCHAR(120), nullable=False)
    dealer_address = Column(VARCHAR(120), nullable=False)
    access_token = Column(Text)
    # cars = relationship('Cars', backref='Dealers', passive_deletes=True)
    # created_on = Column(DateTime, nullable=False, default=datetime.now())
    # updated_on = Column(DateTime, nullable=False, default=datetime.now())
    cars = relationship('Cars', backref=backref('Dealers', cascade='all,delete'))


class Cars(Base):
    __tablename__ = 'cars'

    car_id = Column(Integer, primary_key=True, index=True)
    reg_num = Column(VARCHAR(30), unique=True, nullable=False)
    model_type = Column(VARCHAR(30), nullable=False)
    model_color = Column(String(30), nullable=False)
    company_name = Column(VARCHAR(30), nullable=False)
    model_name = Column(VARCHAR(30), nullable=False)
    model_year = Column(Integer, nullable=False)
    price = Column(Integer, nullable=True)
    travelled_kms = Column(Integer, nullable=True)
    variant = Column(Enum(FuelVariant))
    gear_type = Column(Enum(GearType))
    used_years = Column(Integer, nullable=True)
    engine_in_cc = Column(Integer, nullable=True)
    num_of_seats = Column(Integer, nullable=True)
    num_of_owners = Column(Integer, nullable=True)
    is_available = Column(Boolean, default=True)
    description = Column(Text)
    dealer_id = Column(Integer, ForeignKey('dealers.dealer_id'))
    # created_on = Column(DateTime, nullable=False, default=datetime.now())
    # updated_on = Column(DateTime, nullable=False, default=datetime.now())
    # cars = relationship("Child", cascade="all,delete", backref="parent")