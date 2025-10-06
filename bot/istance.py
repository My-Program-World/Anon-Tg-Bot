from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.middleware import FSMContextMiddleware

from config import TOKEN
from handlers import user
from storage import redis_storage
from middleware import BlockCommandInStateMiddleware

bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher(storage=redis_storage)

user.router.message.middleware(BlockCommandInStateMiddleware())
dp.include_routers(user.router)


__all__ = [
    'bot',
    'dp'
]