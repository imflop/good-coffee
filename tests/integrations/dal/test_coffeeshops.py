import pytest

from good_coffee.lib.dal.coffeshops import CoffeeShopRepository

from ...factory_boys import CoffeeShopFactory


@pytest.fixture()
def repository(db):
    return CoffeeShopRepository(db)


@pytest.mark.asyncio
async def test_get_coffee_shop(repository):
    coffee_shop = CoffeeShopFactory.create()
    result = await repository.get(coffee_shop.id)

    assert result.name == coffee_shop.name
