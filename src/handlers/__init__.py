from aiogram import Dispatcher

from .start import start_cmd, start_cq
from .url_and_text import url_and_text_cq
from .vcard import vcard_cq
from .email import email_cq
from .sms import sms_cq
from .wifi import wifi_cq


def register_handlers(dp: Dispatcher):
    """
    Registration of all handlers before launching the bot.

    Handlers with state should be higher than others in their category.

    Categories must be registered in the following order:
    Callback Query
    Command
    Message
    """

    # Callback quieries handlers
    dp.register_callback_query_handler(start_cq, text='start', state='*')
    dp.register_callback_query_handler(url_and_text_cq, text='url_and_text')
    dp.register_callback_query_handler(vcard_cq, text='vcard')
    dp.register_callback_query_handler(email_cq, text='email')
    dp.register_callback_query_handler(sms_cq, text='sms')
    dp.register_callback_query_handler(wifi_cq, text='wifi')

    # Commands handlers
    dp.register_message_handler(start_cmd, commands=['start'], state='*')
