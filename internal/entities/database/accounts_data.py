from uuid import UUID

from numpy.ma.core import append
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, BIGINT

from .base import Base, BaseDB


class AccountData(Base):
    __tablename__ = "accounts_data"

    id = Column(Integer, autoincrement=True, primary_key=True)
    account_id = Column(PG_UUID(as_uuid=True), ForeignKey("accounts.id"))
    is_payment = Column(Boolean, default=True)
    deal_id = Column(BIGINT, ForeignKey("deals.id"), nullable=True)
    value = Column(String)

    refs = []

    def dict(self):
        return {
            "id": self.id,
            "account_id": self.account_id,
            "is_payment": self.is_payment,
            "deal_id": self.deal_id,
            "value": self.value,
        }


class AccountsData(BaseDB[AccountData]):
    def __init__(self):
        super().__init__(AccountData)

    async def new(self, instance: AccountData):
        await self._add_obj(instance)

    async def get(self, id: int) -> AccountData | None:
        result = await self._get_object(id)
        return result

    async def update(self, instance: AccountData) -> None:
        await self._update_obj(instance=instance)

    async def delete(self, instance: AccountData) -> None:
        await self._delete_obj(instance=instance)

    async def found(self, ids: list[int | str]) -> list[AccountData]:
        result: list[AccountData] = list()
        for id in ids:
            ac_data = await self._get_object(int(id))
            if ac_data is not None:
                result.append(ac_data)
        return result

    async def find_by_deal(self, deal_id: int) -> list[AccountData]:
        filters = {AccountData.deal_id: deal_id}
        result = await self._get_objects(filters)
        return result

    async def get_by_account(self, account_id: UUID | str) -> list[AccountData]:
        if isinstance(account_id, str):
            try:
                account_id = UUID(account_id)
            except ValueError:
                return []
        filters = {AccountData.account_id: account_id, AccountData.is_payment: False}
        result = await self._get_objects(filters)
        return result
