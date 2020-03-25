# QRHelperTelegramBot
This program is a Telegram bot that converts text into a black and white QR code in PNG and SVG formats. It is designed to work on [Heroku](https://heroku.com/ "Heroku"). You can try using this bot at this [link](https://t.me/qr_helper_bot "t.me/qr_helper_bot/").
## Solutions
This program works using the [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI "pyTelegramBotAPI") module and uses webhook method.
To receive POST requests from Telegram API, the web framework [Flask](https://github.com/pallets/flask "Flask") is used.
## Updates
### 26.03.2020
- The main function is implemented.