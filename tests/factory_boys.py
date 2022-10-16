from datetime import datetime
from random import randint

import factory
from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy import orm

from good_coffee.lib.dal.models.coffeeshops import (CityModel, CoffeeShopModel,
                                                    CountryModel)

Session = orm.scoped_session(orm.sessionmaker())


def generate_id(obj, create, value):
    if hasattr(obj, "id") and obj.id is None:
        obj.id = value or randint(1, 1000000)


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"
        strategy = factory.BUILD_STRATEGY

    id = factory.PostGeneration(generate_id)


class CountryFactory(BaseFactory):
    class Meta:
        model = CountryModel

    name = factory.Faker("pystr")
    slug_name = factory.Faker("pystr")


class CityFactory(BaseFactory):
    class Meta:
        model = CityModel

    name = factory.Faker("city")
    slug_name = factory.Faker("pystr")

    country = factory.SubFactory(CountryFactory)


class CoffeeShopFactory(BaseFactory):
    class Meta:
        model = CoffeeShopModel

    name = factory.Faker("pystr")
    slug_name = factory.Faker("pystr")
    instagram_url = factory.Faker("url")
    city_id = factory.Faker("pyint")
    latitude = factory.Faker("pyfloat")
    longitude = factory.Faker("pyfloat")
    description = factory.Faker("pystr")
    created_at = factory.LazyFunction(datetime.utcnow)
    updated_at = factory.LazyFunction(datetime.utcnow)

    city = factory.SubFactory(CityFactory)
