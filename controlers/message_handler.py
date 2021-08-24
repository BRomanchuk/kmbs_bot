import numpy as np

from telebot.types import ReplyKeyboardMarkup

from core import school
from data_loader import get_managers_df, get_programs_df, get_service_df, get_professors_df

from settings.constants import START_MESSAGE
from settings.srting_processing import get_message_variants


# send start message
def get_start_message(bot, message):
    start_message = "Привіт, " + str(message.from_user.first_name) + "!\n\n" + START_MESSAGE
    bot.send_message(message.chat.id, start_message)


# update all dataframes from google sheets
def update_data(bot, message):
    school.programs_df = get_programs_df()
    school.professors_df = get_professors_df()
    school.five_stars_df = get_service_df()
    school.managers_df = get_managers_df()

    bot.send_message(message.chat.id, "✅ оновлено")


# get programs of the certain type and make reply markup of them
def process_program_type(bot, message):
    program_type = message.text[1:]
    programs = school.get_programs_by_type(program_type=program_type)

    reply_markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    for program in programs:
        reply_markup.add(program)

    bot.send_message(message.chat.id, "Програми типу " + message.text + ":", reply_markup=reply_markup)


def process_text(bot, message):
    programs_and_staff = np.concat([school.get_programs(), school.get_programs(), school.get_managers(), school.get_five_stars()])
    message_variants = get_message_variants(message, programs_and_staff)
