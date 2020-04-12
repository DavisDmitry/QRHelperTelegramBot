import os

from app import bot, db, token
from models import User

from telebot import types
import pyqrcode
from PIL import Image

import messages as msg
import keyboards as kb


def reg(chat_id, language):
    user = User(id=chat_id, language=language)
    db.session.add(user)
    db.session.commit()
    bot.send_message(chat_id, msg.en['reg'])


def auth(chat_id):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if User.query.filter_by(id=chat_id).count() == 0:
                text = msg.en['choose_language'] + '\n\n' + msg.ru['choose_language']
                bot.send_message(chat_id, text, reply_markup=kb.language(), parse_mode='html')
            else:
                func(*args, **kwargs)
        return wrapper
    return decorator


def change_language(chat_id, message_id, language):
    User.query.filter_by(id=chat_id).update({'language': language})
    db.session.commit()

    language = User.query.filter_by(id=chat_id).first().language
    if language == 'en':
        language = u"\U0001F1EC" + u"\U0001F1E7"
    elif language == 'ru':
        language = u"\U0001F1F7" + u"\U0001F1FA"
    text = msg.en['settings'].format(chat_id, language)
    
    bot.edit_message_text(text, chat_id=chat_id, message_id=message_id, parse_mode='html', reply_markup=kb.settings(msg.en['change_language']))


def generate(chat_id):
    chat_id_str = str(chat_id)
    user = User.query.filter_by(id=chat_id).first()

    result = pyqrcode.create(user.string, error='H')

    class Result():
        language = user.language

        if not user.scale:
            scale = 1
            User.query.filter_by(id=chat_id).update({'scale': scale})
        else:
            scale = user.scale
        
        if not user.qz:
            qz = 1
        else:
            qz = user.qz
        
        if not user.color:
            color = 'black'
        else:
            color = user.color
        
        if not user.bg:
            bg = 'white'
        else:
            bg = user.bg

        db.session.commit()
        
        result.png(chat_id_str + '.png', scale=scale, quiet_zone=qz)
        result.svg(chat_id_str + '.svg', scale=scale, quiet_zone=qz)

        (width, height) = Image.open(chat_id_str + '.png').size

        png = open(chat_id_str + '.png', 'rb')
        svg = open(chat_id_str + '.svg', 'rb')

    return Result


@bot.callback_query_handler(func=lambda call: True)
def get_callback(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if User.query.filter_by(id=chat_id).count() == 0:
        if call.data == 'en':
            reg(chat_id, 'en')
        elif call.data == 'ru':
            reg(chat_id, 'ru')
        else:
            text = msg.en['choose_language'] + '\n\n' + msg.ru['choose_language']
            bot.send_message(chat_id, text, reply_markup=kb.language(), parse_mode='html')
    else:
        if call.data == 'change_language':
            bot.edit_message_text(msg.en['choose_language'], chat_id=chat_id, message_id=message_id, reply_markup=kb.language())
        if call.data == 'en':
            change_language(chat_id, message_id, 'en')
        elif call.data == 'ru':
            change_language(chat_id, message_id, 'ru')
        if call.data == 'scale-':
            chat_id_str = str(chat_id)
            user = User.query.filter_by(id=chat_id).first()
            scale = user.scale - 1

            User.query.filter_by(id=chat_id).update({'scale': scale})
            db.session.commit()

            data = generate(chat_id)
            text = text = msg.en['generate_parameters'].format(data.width, data.height, data.scale, data.qz, data.color, data.bg)

            bot.edit_message_media(types.InputMediaPhoto(data.png, caption=text, parse_mode='html'),
                                                         chat_id=chat_id, message_id=message_id,
                                                         reply_markup=kb.preview(data.language))

            os.remove(chat_id_str + '.png')
            os.remove(chat_id_str + '.svg')
        elif call.data == 'scale+':
            chat_id_str = str(chat_id)
            user = User.query.filter_by(id=chat_id).first()
            scale = user.scale + 1

            User.query.filter_by(id=chat_id).update({'scale': scale})
            db.session.commit()

            data = generate(chat_id)
            text = text = msg.en['generate_parameters'].format(data.width, data.height, data.scale, data.qz, data.color, data.bg)

            bot.edit_message_media(types.InputMediaPhoto(data.png, caption=text, parse_mode='html'),
                                                         chat_id=chat_id, message_id=message_id,
                                                         reply_markup=kb.preview(data.language))

            os.remove(chat_id_str + '.png')
            os.remove(chat_id_str + '.svg')
        if call.data == 'done':
            chat_id_str = str(chat_id)

            bot.delete_message(chat_id, message_id)

            data = generate(chat_id)
            
            bot.send_document(chat_id, data.png)
            bot.send_document(chat_id, data.svg)

            os.remove(chat_id_str + '.png')
            os.remove(chat_id_str + '.svg')

            User.query.filter_by(id=chat_id).update({'string': None,
                                                     'scale': None,
                                                     'qz': None,
                                                     'color': None,
                                                     'bg': None})
            db.session.commit()


@bot.message_handler(commands = ['start', 'help'])
def start(message):
    chat_id = message.chat.id

    @auth(chat_id)
    def func():
        bot.send_message(chat_id, msg.en['start'])
    
    func()


@bot.message_handler(commands = ['settings'])
def settings(message):
    chat_id = message.chat.id

    @auth(chat_id)
    def func():
        language = User.query.filter_by(id=chat_id).first().language
        if language == 'en':
            language = u"\U0001F1EC" + u"\U0001F1E7"
        elif language == 'ru':
            language = u"\U0001F1F7" + u"\U0001F1FA"
        
        text = msg.en['settings'].format(chat_id, language)
        bot.send_message(chat_id, text, reply_markup=kb.settings(msg.en['change_language']), parse_mode='html')
    
    func()


@bot.message_handler(commands = ['generate'])
def generate_command(message):
    chat_id = message.chat.id

    @auth(chat_id)
    def func():
        text = msg.en['generate']
        answer = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(answer, preview)
    
    func()


def preview(message):
    chat_id = message.chat.id
    chat_id_str = str(chat_id)

    @auth(chat_id)
    def func():
        message_text = u'{}'.format(message.text)
        User.query.filter_by(id=chat_id).update({'string': message_text, 'scale': 1})
        db.session.commit()

        data = generate(chat_id)
        text = msg.en['generate_parameters'].format(data.width, data.height, data.scale, data.qz, data.color, data.bg)
        bot.send_photo(chat_id, data.png, caption=text, reply_markup=kb.preview(data.language), parse_mode='html')
        
        os.remove(chat_id_str + '.png')
        os.remove(chat_id_str + '.svg')
    
    func()