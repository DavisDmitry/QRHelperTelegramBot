import os

from flask import Flask, request

import telebot

import pyqrcode


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


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Send me a text, so I turned it into a QR code.')


@bot.message_handler(content_types=['text'])
def act(message):
    chat_id_str = str(message.chat.id)
    result = pyqrcode.create(message.text)

    result.png(chat_id_str + '.png')
    result.svg(chat_id_str + '.svg')

    png = open(chat_id_str + '.png', 'rb')
    svg = open(chat_id_str + '.svg', 'rb')

    bot.send_document(message.chat.id, png)
    bot.send_document(message.chat.id, svg)

    os.remove(chat_id_str + '.png')
    os.remove(chat_id_str + '.svg')