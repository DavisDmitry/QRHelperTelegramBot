import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

import telebot


token = os.environ.get('TOKEN')
domain = os.environ.get('DOMAIN')


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('JAWSDB_MARIA_URL')
db = SQLAlchemy(app)
bot = telebot.TeleBot(token)


@app.route('/')
def index():
    return '<h1>Everything is work!</h1>'


@app.route('/' + token, methods = ['POST'])
def getWH():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return '!', 200


@app.route('/setwh/')
def setWH():
    bot.remove_webhook()
    bot.set_webhook(url = domain + token)
    return '!', 200


from bot import *