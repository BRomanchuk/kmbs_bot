from settings.constants import PROGRAMS_COMMANDS

from controllers.message_processor import get_start_message, get_updated_data, process_program_type, get_processed_text


def init_message_handlers(bot, school):

    @bot.message_handler(commands=["start", "help"])
    def start(message):
        get_start_message(bot, message)

    @bot.message_handler(commands=["update"])
    def update_data(message):
        get_updated_data(bot, message, school)

    @bot.message_handler(commands=PROGRAMS_COMMANDS)
    def programs_commands(message):
        process_program_type(bot, message, school)

    @bot.message_handler(content_types=["text"])
    def process_text(message):
        get_processed_text(bot, message, school)
