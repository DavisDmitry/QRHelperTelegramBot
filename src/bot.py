import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext

from config import DB_URL, TOKEN
from middlewares import AuthMiddleware


bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
auth_middleware = AuthMiddleware()


logging.basicConfig(level=logging.DEBUG)


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Hello, {}!'.format(message.from_user.first_name))


async def on_startup(dp: Dispatcher):
    dp.middleware.setup(auth_middleware)


async def on_shutdown(dp: Dispatcher):
    await auth_middleware.close()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
