from core.routes import bot
from settings.constants import PROGRAMS_COMMANDS

from controllers.message_processor import get_start_message, update_data, process_program_type, process_text


@bot.message_handler(commands=["start", "help"])
def start(message):
    get_start_message(bot, message)


@bot.message_handler(commands=["update"])
def update_data(message):
    update_data(bot, message)


@bot.message_handler(commands=PROGRAMS_COMMANDS)
def programs_commands(message):
    process_program_type(bot, message)


@bot.message_handler(content_types=["text"])
def process_text(message):
    process_text(bot, message)
