from sqlalchemy import (
    Column,
    Boolean,
    BigInteger,
    ForeignKey,
    Integer,
    Float,
    String,
    DateTime,
)
from sqlalchemy.sql import func

from internal.entities.models import DataDeals
from internal.service.GetMessage import rounding_numbers
from .accounts import Accounts
from .accounts_data import AccountsData
from .base import Base, BaseDB
from .categories import Categories


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, autoincrement="auto", primary_key=True)
    buyer_id = Column(BigInteger, ForeignKey("users.id"))
    price = Column(Float)
    commission = Column(Float)
    wallet = Column(String)
    guarantor = Column(Boolean)
    payment_status = Column(Boolean)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    refs = []

    def dict(self):
        return {
            "id": self.id,
            "buyer_id": self.buyer_id,
            "price": self.price,
            "commission": self.commission,
            "wallet": self.wallet,
            "guarantor": self.guarantor,
            "payment_status": self.payment_status,
            "created_at": self.created_at,
        }


class Deals(BaseDB[Deal]):
    def __init__(self):
        super().__init__(Deal)

    async def new(self, instance: Deal):
        await self._add_obj(instance)

    async def get(self, id: int) -> Deal | None:
        result = await self._get_object(id)
        return result

    async def update(self, instance: Deal) -> None:
        await self._update_obj(instance=instance)

    async def delete(self, instance: Deal) -> None:
        await self._delete_obj(instance=instance)

    async def get_data_deals(self) -> list[DataDeals]:
        result = list()
        async for deal in self:
            accountsData = await AccountsData().find_by_deal(deal.id)
            if not accountsData:
                continue
            account = await Accounts().get(accountsData[0].account_id)
            if account is None:
                continue

            category = await Categories().get(account.category_id)
            for account_data in accountsData:
                result.append(
                    DataDeals(
                        id=deal.id,
                        category=category.name,
                        name=account.name,
                        price=deal.price,
                        description=account.description,
                        data=account_data.value,
                        date=deal.created_at.strftime("%d.%m.%Y в %H:%M"),
                        guarantor=deal.guarantor,
                    )
                )
        return result

    async def get_user_deals(self, id: int) -> list[DataDeals]:
        filters = {Deal.buyer_id: id}
        deals = await self._get_objects(filters=filters)
        result = list()

        for deal in deals:
            accountsData = await AccountsData().find_by_deal(deal.id)
            if not accountsData:
                continue
            account = await Accounts().get(accountsData[0].account_id)
            if account is None:
                continue
            category = await Categories().get(account.category_id)

            for account_data in accountsData:
                data_deal = DataDeals(
                    id=deal.id,
                    category=category.name,
                    name=account.name,
                    price=rounding_numbers(str(deal.price)),
                    description=account.description,
                    data=account_data.value,
                    date=deal.created_at.strftime("%d.%m.%Y в %H:%M "),
                    guarantor=deal.guarantor,
                )
                result.append(data_deal)

        return result

    async def in_(self, id: int) -> Deal | bool:
        result = await self.get(id)
        if type(result) is Deal:
            return result
        return False

    async def get_last_deal(self, user_id) -> Deal:
        sql = select(Deal).where(Deal.buyer_id == user_id).order_by(Deal.id.desc()).limit(1)  # noqa
        data = await self._get_by_query(sql)
        if not data:
            return None
        return data[0]

    async def get_unpaid_deals(self) -> list[Deal]:
        filters = {Deal.payment_status: 0}
        data = await self._get_objects(filters)
        return data

    async def get_guarantor_deals(self) -> list[Deal]:
        filters = {Deal.guarantor: True}
        data = await self._get_objects(filters)
        return data

    async def get_all(self):
        return await self._get_objects({})
