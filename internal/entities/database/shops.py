from sqlalchemy import Column, String, Integer

from .base import Base, BaseDB


class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    description = Column(String)
    path_photo = Column(String)
    bot_link = Column(String)

    refs = []

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "path_photo": self.path_photo,
            "bot_link": self.bot_link,
        }


class Shops(BaseDB[Shop]):
    def __init__(self):
        super().__init__(Shop)

    async def new(self, instance: Shop):
        await self._add_obj(instance)

    async def get(self, id: int) -> Shop | None:
        result = await self._get_object(id)
        return result

    async def update(self, instance: Shop) -> None:
        await self._update_obj(instance=instance)

    async def delete(self, instance: Shop) -> None:
        await self._delete_obj(instance=instance)

    async def in_(self, id: int) -> Shop | bool:
        result = await self.get(id)
        if type(result) is Shop:
            return result
        return False
