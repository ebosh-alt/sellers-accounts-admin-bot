from aiogram.types import BotCommand
from loguru import logger

from internal.app.app import bot, dp
from internal.entities.database.base import create_async_database
from internal.handlers import routers
from pkg import middleware
from pkg.logger import set_logger


@logger.catch()
async def run():
    await create_async_database()
    set_logger()

    for router in routers:
        dp.include_router(router)
    dp.update.middleware(middleware.Logging())
    await set_commands()
    await dp.start_polling(bot)


async def set_commands():
    await bot.set_my_commands(
        commands=[BotCommand(command="admin", description="Открыть меню администратора")]
    )
