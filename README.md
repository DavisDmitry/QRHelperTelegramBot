# QRHelperTelegramBot
You can using this bot at this [link](https://t.me/qr_helper_bot).
## Feautures
- Generating QR codes from text and sending them in PNG and SVG formats
- Adjust the scale of the generated QR code
## Settings
For this bot to work, you will need to register several config vars in the settings of your Heroku application.

- DOMAIN - the address of your application (e.g. https://qrhelpertelegrambot.herokuapp.com/)
- JAWSDB_MARIA_URL - Address to connect to your database. It is issued when the add-on is installed, but it will be necessary to add a small part. (mysql+pymysql://user:password@host:port/database)
- TOKEN - token of your bot. It can be obtained from [BotFather](https://t.me/botfather).

To accept requests from the Telegram Bot API, you must go to the domain of your application and add /setwh (for example, https://qrhelpertelegrambot.herokuapp.com/setwh/).
## Solutions
- [PyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) for working with Telegram Bot API
- [Flask](https://github.com/pallets/flask) for receiving webhooks from Telegram Bot API
- [Heroku](https://heroku.com/) as a hosting
- [JawsDB Maria](https://elements.heroku.com/addons/jawsdb-maria) for storing data about users and QR codes
- [PyQRCode](https://github.com/mnooner256/pyqrcode) for generating QR codes
## Updates
### 26.03.2020
- The main function is implemented
### 29.03.2020
- Add language system
- Add QR code preview
### 10.04.2020
- Add registration and settings
### 13.04.2020
- Move the preview before the end result
- Add ability to change scale
- Fix unicode symbols