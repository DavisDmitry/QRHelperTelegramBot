from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import messages as msg


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


def preview(language):
    markup = InlineKeyboardMarkup()

    if language == 'en':
        scale = msg.en['scale']
        done = msg.en['done']
    elif language == 'ru':
        scale = msg.en['scale']
        done = msg.en['done']
    
    scale_minus_btn = InlineKeyboardButton(u"\u2796", callback_data='scale-')
    scale_btn = InlineKeyboardButton(scale, callback_data='scale')
    scale_plus_btn = InlineKeyboardButton(u"\u2795", callback_data='scale+')
    markup.add(scale_minus_btn, scale_btn, scale_plus_btn)
    
    done_btn = InlineKeyboardButton(done, callback_data='done')
    markup.add(done_btn)

    return markup