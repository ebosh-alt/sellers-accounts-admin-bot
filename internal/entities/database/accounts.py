from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import (
    Column,
    select,
    String,
    Boolean,
    Float,
    Integer,
    ForeignKey,
    Row,
    RowMapping,
    DateTime,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func

from .base import Base, BaseDB


class Account(Base):
    __tablename__ = "accounts"

    id: UUID = Column(PG_UUID(as_uuid=True), primary_key=True)
    category_id: int = Column(Integer, ForeignKey("categories.id"))
    name: str = Column(String)
    price: float = Column(Float)
    description: str = Column(String)
    accepted: bool = Column(Boolean)
    view_type: bool = Column(Boolean)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    refs = []

    def dict(self):
        return {
            "id": self.id,
            "category_id": self.category_id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "accepted": self.accepted,
            "view_type": self.view_type,
            "created_at": self.created_at,
        }


class Accounts(BaseDB[Account]):
    def __init__(self):
        super().__init__(Account)

    async def new(self, instance: Account):
        await self._add_obj(instance)

    async def get(self, id: UUID | str) -> Account | None:
        if isinstance(id, str):
            try:
                id = UUID(id)
            except ValueError:
                return None
        result = await self._get_object(id)
        return result

    async def update(self, instance: Account) -> None:
        await self._update_obj(instance=instance)

    async def delete(self, instance: Account) -> None:
        await self._delete_obj(instance=instance)

    async def in_(self, id: UUID | str) -> Account | bool:
        result = await self.get(id)
        if isinstance(result, Account):
            return result
        return False

    # TODO: edit logic
    async def get_instance_by_name(self, name: str, **kwargs):
        filters = {Account.name: name, Account.view_type: True}
        result: list[Account] = await self._get_objects(filters=filters)
        instance = result
        return instance

    async def get_last(self) -> Account:
        filters = {}
        data = await self._get_objects(filters)
        return data[-1]

    async def get_by_deal_id(self, deal_id: int) -> list[Account]:
        from internal.entities.database.accounts_data import AccountData

        async with await self._get_session() as session:
            sql = (
                select(Account, AccountData)
                .join(AccountData, AccountData.account_id == Account.id)
                .where(AccountData.deal_id == deal_id)  # noqa
            )
            result = await session.execute(sql)
            rows = result.all()

        accounts: list[Account] = []
        for account, account_data in rows:
            account.data = account_data.value
            accounts.append(account)

        return accounts

    async def get_view(self):
        filters = {Account.view_type: True, Account.accepted: True}
        instances: list[Account] = await self._get_objects(filters=filters)
        return instances

    async def count_by_name_category(self, name, category_id, **kwargs) -> int:
        filters = {Account.view_type: True,
                   Account.name: name,
                   Account.category_id: category_id,
                   }
        instances: list[Account] = await self._get_objects(filters=filters)
        return len(instances)

    async def get_by_name_category(self, category_id, **kwargs) -> Sequence[Row[Any] | RowMapping | Any]:
        async with await self._get_session() as session:
            subquery = (
                select(
                    Account.name,
                    func.min(Account.id).label("min_id")
                )
                .where(
                    Account.category_id == category_id,  # noqa
                    Account.view_type.is_(True)  # noqa
                )
                .group_by(Account.name)
                .subquery()
            )

            stmt = (
                select(Account)
                .join(subquery, Account.id == subquery.c.min_id)
            )

            result = await session.execute(stmt)
            unique_accounts = result.scalars().all()

            return unique_accounts

    async def get_viewed_by_category(self, category_name: str, **kwargs) -> list[Account]:
        from internal.entities.database.categories import Category
        sql = (
            select(Account)
            .join(Category, Account.category_id == Category.id)
            .where(
                Account.view_type.is_(True),  # noqa
                Account.accepted.is_(True),  # noqa
                Category.name == category_name,  # noqa
            )
        )
        result = await self._get_by_query(sql)
        return result

    async def get_by_name_category_by_select(self, name: str, category_name: str, **kwargs) -> list[Account]:
        from internal.entities.database.categories import Category
        sql = (
            select(Account)
            .join(Category, Account.category_id == Category.id)
            .where(
                Account.view_type.is_(True),  # noqa
                Category.name == category_name,  # noqa
                Account.name == name  # noqa
            )
        )
        result = await self._get_by_query(sql)
        return result

    async def accepted_accounts(self, accounts_list: list[Account]):
        for account in accounts_list:
            account.accepted = True

        await self._bulk_add(accounts_list)

    async def get_by_uid(self, uid):
        pass
