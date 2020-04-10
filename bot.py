import os

from app import bot, db, token
from models import User

import pyqrcode

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
        if call.data == 'change_language':
            bot.edit_message_text(msg.en['choose_language'], chat_id=chat_id, message_id=message_id, reply_markup=kb.language())
        if call.data == 'en':
            change_language(chat_id, message_id, 'en')
        elif call.data == 'ru':
            change_language(chat_id, message_id, 'ru')


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
def generate(message):
    chat_id = message.chat.id

    @auth(chat_id)
    def func():
        text = msg.en['generate']
        answer = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(answer, generate_settings)
    
    func()


def generate_settings(message):
    chat_id = message.chat.id

    @auth(chat_id)
    def func():
        chat_id_str = str(chat_id)
        string = message.text

        result = pyqrcode.create(string, error = 'H')

        modules = 17
        for i in range(1, result.version + 1):
            modules += 4

        if modules < 500:
            scale = 500 // modules
        if modules * scale < 500:
            scale += 1
        else :
            scale = 1

        result.png(chat_id_str + '.png', scale = scale, quiet_zone = 1)
        result.svg(chat_id_str + '.svg', scale = scale, quiet_zone = 1)

        png = open(chat_id_str + '.png', 'rb')
        svg = open(chat_id_str + '.svg', 'rb')

        bot.send_document(message.chat.id, png)
        bot.send_document(message.chat.id, svg)

        os.remove(chat_id_str + '.png')
        os.remove(chat_id_str + '.svg')
    
    func()


@bot.message_handler(content_types = ['text'])
def act(message):
    chat_id = message.chat.id

    @auth(chat_id)
    def func():
        chat_id_str = str(chat_id)
        string = message.text

        result = pyqrcode.create(string, error = 'H')

        modules = 17
        for i in range(1, result.version + 1):
            modules += 4

        if modules < 500:
            scale = 500 // modules
        if modules * scale < 500:
            scale += 1
        else :
            scale = 1

        text = msg.en['generate_parameters'].format(scale, '1', 'black', 'white')
        result.png(chat_id_str + '.png', scale = scale, quiet_zone = 1)
        png = open(chat_id_str + '.png', 'rb')
        bot.send_photo(message.chat.id, png, text, parse_mode = 'html')
        os.remove(chat_id_str + '.png')
    
    func()