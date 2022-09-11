from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .common import Base


class CountryModel(Base):
    __tablename__ = "countries"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(512), unique=True)
    slug_name = Column(String(1024))

    cities = relationship("CityModel", back_populates="country")


class CityModel(Base):
    __tablename__ = "cities"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(512), unique=True)
    slug_name = Column(String(1024))
    country_id = Column(Integer, ForeignKey("countries.id"), index=True)

    country = relationship(CountryModel, back_populates="cities")
    coffee_shops = relationship("CoffeeShopModel")


class CoffeeShopModel(Base):
    __tablename__ = "coffee_shops"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(512), nullable=False)
    slug_name = Column(String(1024))
    instagram_url = Column(String(512), nullable=True)
    city_id = Column(Integer, ForeignKey("cities.id"), index=True)
    latitude = Column(Float(precision=32, decimal_return_scale=None), nullable=False)
    longitude = Column(Float(precision=32, decimal_return_scale=None), nullable=False)
    description = Column(String(1024), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    city = relationship(CityModel, back_populates="coffee_shops")
