from __future__ import annotations

import dataclasses as dc

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from .models.coffeeshops import CityModel, CoffeeShopModel


@dc.dataclass(frozen=True, repr=False, slots=True)
class CoffeeShopRepository:
    db: AsyncSession

    async def get(self, coffee_shop_id: int) -> CoffeeShopModel | None:
        stmt = (
            select(CoffeeShopModel)
            .options(selectinload(CoffeeShopModel.city))
            .where(CoffeeShopModel.id == coffee_shop_id)
        )

        result = await self.db.execute(stmt)
        row = result.fetchone()

        return row[CoffeeShopModel] if row else None

    async def get_coffee_shops(self, city_name: str) -> list[CoffeeShopModel]:
        stmt = (
            select(CoffeeShopModel)
            .join(CityModel)
            .options(selectinload(CoffeeShopModel.city))
            .where(CityModel.name.ilike(city_name))
        )

        result = await self.db.execute(stmt)
        rows = result.all()

        return [row[CoffeeShopModel] for row in rows]
