from aiogram.types import CallbackQuery


async def url_and_text_cq(cq: CallbackQuery):
    await cq.answer('This feature is not yet available.')
