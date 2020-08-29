from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start():
    markup = InlineKeyboardMarkup(3)
    markup.add(
        InlineKeyboardButton(u'\U0001F517' + ' URL', callback_data='url_and_text'),
        InlineKeyboardButton(u'\U0001F4B3' + ' VCARD', callback_data='vcard'),
        InlineKeyboardButton(u'\U0001F4AC' + ' TEXT', callback_data='url_and_text'),
        InlineKeyboardButton(u'\U0001F4E7' + ' E-MAIL', callback_data='email'),
        InlineKeyboardButton(u'\U0001F4DF' + ' SMS', callback_data='sms'),
        InlineKeyboardButton(u'\U0001F4F6' + ' WIFI', callback_data='wifi')
    )
    return markup
