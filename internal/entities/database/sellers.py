from sqlalchemy import Column, String, BigInteger, Float

from config.config import config
from .base import Base, BaseDB


class Seller(Base):
    __tablename__ = "sellers"

    id = Column(BigInteger, primary_key=True)
    rating = Column(Float)
    balance = Column(Float)
    username = Column(String)
    wallet = Column(String)

    refs = []

    def dict(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "balance": self.balance,
            "username": self.username,
            "wallet": self.wallet,
        }


class Sellers(BaseDB[Seller]):
    def __init__(self):
        super().__init__(Seller)

    async def new(self, seller: Seller):
        await self._add_obj(seller)

    async def get(self, id: int = None) -> Seller | None:
        if id is None:
            id = config.manager.seller_id
        result = await self._get_object(id)
        return result

    async def update(self, instance: Seller) -> None:
        await self._update_obj(instance=instance)

    async def delete(self, instance: Seller) -> None:
        await self._delete_obj(instance=instance)

    async def in_(self, id: int) -> Seller | bool:
        result = await self.get(id)
        if type(result) is Seller:
            return result
        return False
