"""Handler with main menu."""
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message

from screens import start as screen


async def start_cmd(message: Message, state: FSMContext):
    """By command."""
    await state.finish()
    screen['text'] = screen['text'].format(message.from_user.first_name)
    await message.answer(**screen)


async def start_cq(cq: CallbackQuery, state: FSMContext):
    """By callback query."""
    await state.finish()
    screen['text'] = screen['text'].format(cq.from_user.first_name)
    await cq.message.answer(**screen)
