import numpy as np

from telebot.types import ReplyKeyboardMarkup
from telegram import ParseMode

from settings.data_loader import get_managers_df, get_programs_df, get_service_df, get_professors_df

from settings.constants import START_MESSAGE, programs_columns, managers_columns
from settings.srting_processing import get_message_variants


def get_start_message(bot, message):
    """
    send start message
    :param bot: telebot.Telebot
    :param message:
    :return:
    """
    start_message = "Привіт, " + str(message.from_user.first_name) + "!\n\n" + START_MESSAGE
    bot.send_message(message.chat.id, start_message)


def get_updated_data(bot, message, school):
    """
    update all dataframes from google sheets
    :param bot: telebot.Telebot
    :param message:
    :param school
    :return:
    """
    school.programs_df = get_programs_df()
    school.professors_df = get_professors_df()
    school.five_stars_df = get_service_df()
    school.managers_df = get_managers_df()

    bot.send_message(message.chat.id, "✅ оновлено")


def process_program_type(bot, message, school):
    """
    send markup with programs of certain type
    :param bot: telebot.Telebot
    :param message:
    :param school
    :return:
    """
    program_type = message.text[1:]
    programs = school.get_programs_by_type(program_type=program_type)

    reply_markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    for program in programs:
        reply_markup.add(program)

    bot.send_message(message.chat.id, "Програми типу " + message.text + ":", reply_markup=reply_markup)


def get_processed_text(bot, message, school):
    """
    process text message from user
    :param bot: telebot.Telebot
    :param message:
    :param school
    :return:
    """
    # list of arrays of names of school entities
    school_entities = [
        school.get_programs(),
        school.get_professors(),
        school.get_managers(),
        school.get_five_stars()
    ]

    # list of dataframes of school entities
    school_dataframes = [
        school.programs_df,
        school.professors_df,
        school.managers_df,
        school.five_stars_df
    ]

    # flat array of every program and person in the school
    programs_and_staff_flat = np.concatenate([x for x in school_entities])

    # list of all message variants
    message_variants = get_message_variants(message.text, programs_and_staff_flat)

    # init reply message and markup
    reply_markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    reply_message = ""

    # for every variant of the message
    for msg in message_variants:
        # for every entity list in the school
        for i in range(len(school_entities)):
            indices_of_items = __get_indices_of_items(school_entities[i], msg)
            if indices_of_items.shape[0] == 1:
                # construct the str message from the dataframe row
                reply_message = __construct_message_from_dataframe(school_dataframes[i].iloc[[indices_of_items[0]]])
                # get items for the markup (if the dataframe is either programs or managers
                items_for_markup = __get_items_for_markup(school_dataframes[i], indices_of_items[0], school)
                for item in items_for_markup:
                    reply_markup.row(item)
                break
            elif indices_of_items.shape[0] > 1:
                reply_message = "Choose your fighter:"
                for j in indices_of_items:
                    reply_markup.row(school_entities[i][j])
                break

        if len(reply_message) > 0:
            break

    if len(reply_message) == 0:
        reply_message = 'Nothing to show :('

    bot.send_message(message.chat.id, reply_message, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


# get indices of items in array that contain substr as a substring
def __get_indices_of_items(arr, substr):
    indices = np.zeros(arr.shape[0], dtype=int)
    length_index = 0
    for i in range(arr.shape[0]):
        if substr.lower() in arr[i].lower():
            indices[length_index] = i
            length_index += 1
    return indices[:length_index]


# construct the message from the dataframe
def __construct_message_from_dataframe(df):
    message = ""
    for col in df.columns:
        message += "<b>" + str(col) + ":</b>\n" + str(df.iloc[0][col]) + "\n\n"
    return message


# get items for the markup from the dataframe
def __get_items_for_markup(df, index, school):
    if df.columns.shape[0] == len(programs_columns) and np.all(df.columns == school.programs_df.columns):
        return df[programs_columns['professors']].iloc[index].split('\n')
    if df.columns.shape[0] == len(managers_columns) and np.all(df.columns == school.managers_df.columns):
        manager = df[managers_columns['name']].iloc[index]
        programs_of_manager = []
        for row in school.programs_df:
            if manager.lower() in row[programs_columns['manager']].lower():
                programs_of_manager.append(row[programs_columns['name']])
        return programs_of_manager
    return []
