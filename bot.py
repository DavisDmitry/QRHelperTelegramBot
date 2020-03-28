import os

from flask import Flask, request

import telebot

import pyqrcode

import messages as msg


token = os.environ.get('TOKEN')
domain = os.environ.get('DOMAIN')

app = Flask(__name__)
bot = telebot.TeleBot(token)


@app.route('/')
def index():
    return '<h1>Everything is work!</h1>'


@app.route('/' + token, methods=['POST'])
def getWH():
    bot.process_new_updates([telebot.types.Update.de_json(
    request.stream.read().decode('utf-8'))])
    return '!', 200


@app.route('/setwh/')
def setWH():
    bot.remove_webhook()
    bot.set_webhook(url=domain + token)
    return '!', 200


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, msg.en['start'])


@bot.message_handler(commands=['generate'])
def generate(message):
    text = msg.en['generate']
    answer = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(answer, generate_settings)


def generate_settings(message):
    chat_id_str = str(message.chat.id)
    string = message.text

    result = pyqrcode.create(string, error='H')

    modules = 17
    for i in range(1, result.version + 1):
        modules += 4
    
    if modules < 500:
        scale = 500 // modules
        if modules * scale < 500:
            scale += 1
    else:
        scale = 1

    result.png(chat_id_str + '.png', scale=scale, quiet_zone=1)
    result.svg(chat_id_str + '.svg', scale=scale, quiet_zone=1)

    png = open(chat_id_str + '.png', 'rb')
    svg = open(chat_id_str + '.svg', 'rb')

    bot.send_document(message.chat.id, png)
    bot.send_document(message.chat.id, svg)

    os.remove(chat_id_str + '.png')
    os.remove(chat_id_str + '.svg')


@bot.message_handler(content_types=['text'])
def act(message):
    chat_id_str = str(message.chat.id)
    string = message.text

    result = pyqrcode.create(string, error='H')

    modules = 17
    for i in range(1, result.version + 1):
        modules += 4
    
    if modules < 500:
        scale = 500 // modules
        if modules * scale < 500:
            scale += 1
    else:
        scale = 1
    
    text = msg.en['generate_parameters'].format(scale, '1', 'black', 'white')
    result.png(chat_id_str + '.png', scale=scale, quiet_zone=1)
    png = open(chat_id_str + '.png', 'rb')
    bot.send_photo(message.chat.id, png, text, parse_mode='html')
    os.remove(chat_id_str + '.png')