import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import DB_URL, TOKEN
from handlers import register_handlers
from middlewares import AuthMiddleware


bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
auth_middleware = AuthMiddleware()


logging.basicConfig(level=logging.DEBUG)


async def on_startup(dp: Dispatcher):
    dp.middleware.setup(auth_middleware)
    register_handlers(dp)


async def on_shutdown(dp: Dispatcher):
    await auth_middleware.close()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
