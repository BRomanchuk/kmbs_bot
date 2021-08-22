from routes import bot
from settings.constants import PROGRAMS_COMMANDS


@bot.message_handler(commands=["start", "help"])
def start(message):
    pass


@bot.message_handler(commands=["update"])
def update_data(command):
    pass


@bot.message_handler(commands=PROGRAMS_COMMANDS)
def programs_commands(command):
    pass


@bot.message_handler(content_types=["text"])
def process_text(message):
    pass
