from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def language():
    markup = InlineKeyboardMarkup()
    en_btn = InlineKeyboardButton(u"\U0001F1EC" + u"\U0001F1E7" + ' en', callback_data='en')
    ru_btn = InlineKeyboardButton(u"\U0001F1F7" + u"\U0001F1FA" + ' ru', callback_data='ru')
    markup.add(en_btn, ru_btn)
    return markup


def settings(text):
    markup = InlineKeyboardMarkup()
    language_btn = InlineKeyboardButton(text, callback_data='change_language')
    markup.add(language_btn)
    return markup