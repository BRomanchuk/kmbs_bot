import numpy as np

from telebot.types import ReplyKeyboardMarkup
from telegram import ParseMode

from core import school
from data_loader import get_managers_df, get_programs_df, get_service_df, get_professors_df

from settings.constants import START_MESSAGE
from settings.srting_processing import get_message_variants


def get_start_message(bot, message):
    """
    send start message
    :param bot: telebot.Telebot
    :param message: str
    :return:
    """
    start_message = "Привіт, " + str(message.from_user.first_name) + "!\n\n" + START_MESSAGE
    bot.send_message(message.chat.id, start_message)


def update_data(bot, message):
    """
    update all dataframes from google sheets
    :param bot: telebot.Telebot
    :param message:
    :return:
    """
    school.programs_df = get_programs_df()
    school.professors_df = get_professors_df()
    school.five_stars_df = get_service_df()
    school.managers_df = get_managers_df()

    bot.send_message(message.chat.id, "✅ оновлено")


def process_program_type(bot, message):
    """
    send markup with programs of certain type
    :param bot: telebot.Telebot
    :param message:
    :return:
    """
    program_type = message.text[1:]
    programs = school.get_programs_by_type(program_type=program_type)

    reply_markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    for program in programs:
        reply_markup.add(program)

    bot.send_message(message.chat.id, "Програми типу " + message.text + ":", reply_markup=reply_markup)


def process_text(bot, message):
    """
    process text message from user
    :param bot: telebot.Telebot
    :param message:
    :return:
    """

    school_entities = [
        school.get_programs(),
        school.get_professors(),
        school.get_managers(),
        school.get_five_stars()
    ]

    school_entities_dataframes = [
        school.programs_df,
        school.professors_df,
        school.managers_df,
        school.five_stars_df
    ]

    programs_and_staff_flat = np.concatenate([x for x in school_entities])
    message_variants = get_message_variants(message, programs_and_staff_flat)

    reply_markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    reply_message = ""

    # for every variant of the message
    for msg in message_variants:
        # for every entity list in the school
        for i in range(len(school_entities)):
            indices_of_items = __get_indices_of_items(school_entities[i], msg)
            if indices_of_items.shape[0] == 1:
                reply_message = __construct_message_from_dataframe(school_entities_dataframes[i][indices_of_items[0]])
                break
            elif indices_of_items.shape[0] > 1:
                reply_message = "Choose your fighter:"
                for j in indices_of_items:
                    reply_markup.row(school_entities[i][j])
                break

        if len(reply_message) > 0:
            break

    bot.send_message(message.chat.id, reply_message, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


# get indices of items in array that contain substr as a substring
def __get_indices_of_items(arr, substr):
    indices = np.array(arr.shape[0])
    length_index = 0
    for i in range(arr.shape[0]):
        if substr in arr[i]:
            indices[length_index] = i
            length_index += 1
    return indices[:length_index]


# construct the message from the dataframe
def __construct_message_from_dataframe(df):
    message = ""
    for col in df.columns:
        message += "<b>" + col + ":</b>\n" + df[col] + "\n\n"
    return message