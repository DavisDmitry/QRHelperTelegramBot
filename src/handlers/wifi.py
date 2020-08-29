from aiogram.types import CallbackQuery


async def wifi_cq(cq: CallbackQuery):
    await cq.answer('This feature is not yet available.')
