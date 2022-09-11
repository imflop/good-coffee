from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dal.coffeshops import CoffeeShopRepository
from .base import async_session_factory


def coffee_shop_repository_factory(db: AsyncSession = Depends(async_session_factory)) -> CoffeeShopRepository:
    return CoffeeShopRepository(db)
