from flask import Flask

import telebot

from core.routes import init_routes
from core.message_handlers import init_message_handlers

from settings.constants import TOKEN
from structure.school import School


bot = telebot.TeleBot(TOKEN)
school = School()


def create_app():
    """Construct the core application."""
    app = Flask(__name__)

    with app.app_context():
        init_routes(app, bot)
        init_message_handlers(bot, school)
        return app
