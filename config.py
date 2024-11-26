import os
from dotenv import load_dotenv, find_dotenv
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher, Bot
import sqlite3
from gspread import Worksheet, service_account 

load_dotenv(find_dotenv())

Bot_token= os.getenv('token_test')


# Получение ссылки на google таблицу
sheet_url = os.getenv('google_table')
# API бота гугл таблиц
gc = service_account(filename="api_for_google_sheet.json")
wks = gc.open("testTable")


if Bot_token is None:
    raise ValueError("Токен бота не найден. Убедитесь, что переменная окружения 'token_test' установлена.")

bot = Bot(token = Bot_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

user_id_adm = 1413674444
username_bota = os.getenv('name_test')

current_dir= os.path.dirname(os.path.abspath(__file__))
def get_db_connection():
    db_path = os.path.join(current_dir, 'bali.db')
    return db_path

conn = sqlite3.connect(get_db_connection())
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Starst (
    unic_kod INT,
    tg_user_id INT,
    name TEXT,
    place TEXT     
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Just_users (
    unic_kod INT,
    tg_user_id INT,
    name TEXT,
    count_b INT,
    comment MEDIUMTEXT,
    unic_kod_strtsi INT
)
''')