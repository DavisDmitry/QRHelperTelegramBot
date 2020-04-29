from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import messages as msg


def language():
    markup = InlineKeyboardMarkup()
    en_btn = InlineKeyboardButton(u"\U0001F1EC" + u"\U0001F1E7" + ' en', callback_data='en')
    ru_btn = InlineKeyboardButton(u"\U0001F1F7" + u"\U0001F1FA" + ' ru', callback_data='ru')
    markup.add(en_btn, ru_btn)
    return markup


def settings(user):
    markup = InlineKeyboardMarkup()
    language_btn = InlineKeyboardButton(msg.change_language[user.language],
                                        callback_data='change_language')
    markup.add(language_btn)
    return markup


def preview(user):
    markup = InlineKeyboardMarkup()
    
    scale_minus_btn = InlineKeyboardButton(u"\u2796", callback_data='scale-')
    scale_btn = InlineKeyboardButton(msg.scale[user.language], callback_data='scale')
    scale_plus_btn = InlineKeyboardButton(u"\u2795", callback_data='scale+')
    if user.scale <= 1:
        markup.add(scale_btn, scale_plus_btn)
    elif user.scale >= 100:
        markup.add(scale_minus_btn, scale_btn)
    else:
        markup.add(scale_minus_btn, scale_btn, scale_plus_btn)
    
    qz_minus_btn = InlineKeyboardButton(u"\u2796", callback_data='qz-')
    qz_btn = InlineKeyboardButton(msg.qz[user.language], callback_data='qz')
    qz_plus_btn = InlineKeyboardButton(u"\u2795", callback_data='qz+')
    if user.qz <= 0:
        markup.add(qz_btn, qz_plus_btn)
    elif user.qz >=4:
        markup.add(qz_minus_btn, qz_btn)
    else:
        markup.add(qz_minus_btn, qz_btn, qz_plus_btn)
    
    done_btn = InlineKeyboardButton(msg.done[user.language], callback_data='done')
    markup.add(done_btn)

    return markup