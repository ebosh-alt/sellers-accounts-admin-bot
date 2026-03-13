from typing import Any, Sequence, AsyncIterator, List, TypeVar, Generic, Type

from loguru import logger
from sqlalchemy import select, update, Row, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, selectinload
from sqlalchemy.orm import sessionmaker

from config.config import config

Base = declarative_base()

__factory: sessionmaker | None = None

T = TypeVar("T", bound=Base)


async def close_database():
    __factory.close_all()


async def create_async_database():
    global __factory
    engine = create_async_engine(config.db.link_connect)
    if __factory:
        return
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await create_factory()
    await conn.close()


async def create_factory():
    global __factory
    engine = create_async_engine(config.db.link_connect)
    __factory = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


def get_factory():
    global __factory
    return __factory()


class BaseDB(Generic[T]):
    def __init__(self, obj: Type[T]):
        self.obj = obj

    @staticmethod  # __table__ = "accounts"
    async def _get_session() -> AsyncSession:
        async with get_factory() as session:
            return session

    async def _add_obj(self, instance):
        async with await self._get_session() as session:
            session.add(instance)
            await session.flush()
            await session.refresh(instance)  # Обновляем объект
            # self.update_json(instance) // сохранение данные в json
            instance_id = instance.id
            logger.info(f"add new {instance.__class__.__name__}: id={instance_id}")
            await session.commit()
        await session.bind.dispose()
        return instance_id

    async def _get_object(self, id: int | str):
        async with await self._get_session() as session:
            sql = select(self.obj).where(self.obj.id == id)
            for ref in self.obj.refs:
                sql = sql.options(selectinload(ref))
            result = await session.execute(sql)
            result = result.fetchone()
            if result:
                result = result[0]
        await session.bind.dispose()
        return result

    async def _get_objects(self, filters: dict | list = None):
        async with await self._get_session() as session:
            sql = select(self.obj)
            if isinstance(filters, dict):
                for key in filters:
                    sql = sql.where(key == filters[key])
            elif isinstance(filters, list):
                for flt in filters:
                    sql = sql.where(flt)
            for ref in self.obj.refs:
                sql = sql.options(selectinload(ref))
            result = await session.execute(sql)
            result = result.scalars().all()
        await session.bind.dispose()
        return result

    async def __aiter__(self) -> AsyncIterator[Any]:
        """
        Асинхронный итератор для постраничного получения данных из базы.
        """
        async with await self._get_session() as session:
            # Создаем запрос с учетом отношений (refs)
            query = select(self.obj)
            for ref in self.obj.refs:
                query = query.options(selectinload(ref))

            async for instance in await session.stream(query):
                yield instance[0]

    async def _update_obj(self, instance):
        async with await self._get_session() as session:
            query = (
                update(self.obj)
                .where(self.obj.id == instance.id)
                .values(**instance.dict())
            )
            await session.execute(query)
            logger.info(f"update data {instance.__class__.__name__}: id={instance.id}")
            await session.commit()

    async def _delete_obj(self, instance):
        async with await self._get_session() as session:
            await session.delete(instance)
            logger.info(f"delete {instance.__class__.__name__}: id={instance.id}")
            await session.commit()

    async def _get_attributes(
            self, attribute: str
    ) -> Sequence[Row[tuple[Any, ...] | Any]]:
        # получение всех значений конкретного атрибута сущности
        async with await self._get_session() as session:
            sql = select(self.obj).column(attribute)
            result = await session.execute(sql)
            return result.all()

    async def _in(self, attribute, values: list):
        async with await self._get_session() as session:
            sql = select(self.obj).where(attribute.in_(values))
            result = await session.execute(sql)
            return result.scalars().all()

    async def _update_all_values(self, attribute, value):
        async with await self._get_session() as session:
            query = update(self.obj).values({attribute: value})
            await session.execute(query)
            await session.commit()

    async def _bulk_add(self, instances: list[Any]):
        if not instances:
            logger.info("Empty list provided for bulk add")
            return False

        async with await self._get_session() as session:
            session.add_all(instances)
            logger.info(
                f"Adding {len(instances)} {instances[0].__class__.__name__} to the database"
            )
            await session.commit()
            return True

    async def _get_by_query(self, query: Select) -> List[T]:
        async with await self._get_session() as session:
            result = await session.execute(query)
            result = result.unique().scalars().all()
        return result
