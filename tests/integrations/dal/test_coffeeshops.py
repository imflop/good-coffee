import pytest

from good_coffee.lib.dal.coffeshops import CoffeeShopRepository

from ...factory_boys import CityFactory, CoffeeShopFactory


@pytest.fixture()
def repository(db):
    return CoffeeShopRepository(db)


async def test_get_coffee_shop(repository):
    coffee_shop = CoffeeShopFactory.create()
    result = await repository.get(coffee_shop.id)

    assert result.name == coffee_shop.name


async def test_get_coffee_shops(repository):
    city = CityFactory.create()
    coffee_shops = CoffeeShopFactory.create_batch(2, city=city)
    result = await repository.get_coffee_shops(city.name)

    assert len(coffee_shops) == len(result)
