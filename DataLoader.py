import numpy as np
import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from config.constants import SCOPE, JSON_ROUTE, MAIN_TABLE


# open main table
credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_ROUTE, SCOPE)
client = gspread.authorize(credentials)
table = client.open(MAIN_TABLE)


# get programs DataFrame
def get_programs_df():
    return get_df('Programs')


# get professors DataFrame
def get_professors_df():
    return get_df('Professors')


# get managers DataFrame
def get_managers_df():
    return get_df('Managers')


# get 5stars DataFrame
def get_service_df():
    return get_df('Five Stars')


# get DataFrame from google sheet
def get_df(sheet_name):
    sheet = table.worksheet(sheet_name)

    data = np.array(sheet.get_all_values())
    records = data[1:]
    columns = data[0]

    df = pd.DataFrame(records, columns=columns)

    return df
