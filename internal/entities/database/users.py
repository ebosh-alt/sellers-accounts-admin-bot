from sqlalchemy import Column, String, BigInteger

from .base import Base, BaseDB


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String)

    refs = []

    def dict(self):
        return {"id": self.id,
                "username": self.username,
                }


class Users(BaseDB[User]):
    def __init__(self):
        super().__init__(User)

    async def new(self, instance: User):
        await self._add_obj(instance)

    async def get(self, id: int) -> User | None:
        result = await self._get_object(id)
        return result

    async def update(self, instance: User) -> None:
        await self._update_obj(instance=instance)

    async def delete(self, instance: User) -> None:
        await self._delete_obj(instance=instance)

    async def in_(self, id: int) -> User | bool:
        result = await self.get(id)
        if type(result) is User:
            return result
        return False

    async def register_user(self, id: int, username: str):
        user = await self.in_(id=id)

        if user is False:
            user = User(id=id, username=username)
            await self.new(user)
