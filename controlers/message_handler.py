from core import school
from data_loader import get_managers_df, get_programs_df, get_service_df, get_professors_df

def get_start_message(bot, message):
    pass


def update_data(bot, message):
    school.programs_df = get_programs_df()
    school.professors_df = get_professors_df()
    school.five_stars_df = get_service_df()
    school.managers_df = get_managers_df()

    bot.send_message(message.chat.id, "✅ оновлено")


def process_program_types(bot, message):
    program_type = message.text[1:]
    programs = school.get_programs_by_type(program_type=program_type)


def process_text(bot, message):
    pass