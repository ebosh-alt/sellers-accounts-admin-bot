from loguru import logger
from sqlalchemy import Column, String, select, Integer, distinct

from internal.entities.database.accounts import Account
from .base import Base, BaseDB


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)

    refs = []

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Categories(BaseDB[Category]):
    def __init__(self):
        super().__init__(Category)

    async def new(self, instance: Category):
        await self._add_obj(instance)

    async def get(self, id: int) -> Category | None:
        result = await self._get_object(id)
        return result

    async def update(self, instance: Category) -> None:
        await self._update_obj(instance=instance)

    async def delete(self, instance: Category) -> None:
        await self._delete_obj(instance=instance)

    async def in_(self, id: int) -> Category | bool:
        result = await self.get(id)
        if type(result) is Category:
            return result
        return False

    async def get_viewed_categories(self):
        # Запрос для получения категорий с хотя бы одним аккаунтом с view_type = True
        sql = (
            select(distinct(Category.name))
            .join(Account, Account.category_id == Category.id)  # noqa
            .where(Account.view_type.is_(True))  # noqa
            .where(Account.accepted.is_(True))  # noqa
        )
        result = await self._get_by_query(sql)
        return result

    async def get_by_name(self, name):
        filters = {Category.name: name}
        result = await self._get_objects(filters)
        if not result:
            return False
        for el in result:
            logger.info(el.dict())
        return result[0]

    async def get_names(self):
        sql = select(Category.name)
        result = await self._get_by_query(sql)
        names = [el for el in result]
        return names
