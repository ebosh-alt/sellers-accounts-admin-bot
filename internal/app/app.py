from aiogram import Bot, Dispatcher

from config.config import config

dp = Dispatcher()
bot = Bot(config.telegram_bot.token)
