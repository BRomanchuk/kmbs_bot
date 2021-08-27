from flask import request

import telebot

from settings.constants import TOKEN, HEROKU_APP


def init_routes(app, bot):
    @app.route('/' + TOKEN, methods=['POST'])
    def get_message():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200

    @app.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url=HEROKU_APP+TOKEN)
        return "!", 200
