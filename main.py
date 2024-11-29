from typing import Any
from aiogram import types
from aiogram.filters import CommandStart
import logging
import asyncio
import traceback
from starosts_handls import *
from dotenv import load_dotenv, find_dotenv
from Db import *
from FSMS  import *
from adms import *
from general import *  # Импортируем обработчики
from config import dp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from googleSheet import reader


#-------- Общая часть ---------------------------------
dp.message.register(handler_start, CommandStart())
dp.message.register(handler_menu_strst, lambda message: message.text == "В меню")
dp.message.register(father_handler,lambda message: message.text == "/father" )
dp.message.register(handl_statistika, lambda message: message.text == "Статистика")


#-------- Конец общей части ------------------------------

#-------- Начала админской части ---------------------------
dp.message.register(handle_Edit_Starost_0, lambda message: message.text == "Изменение старост")
dp.message.register(handle_Edit_Starost_1, Edit_Starost.comanda)
dp.message.register(handle_Edit_Starost_2, Edit_Starost.choised_starosta)
dp.message.register(handle_Edit_Starost_3, Edit_Starost.new_name_starosti)
dp.message.register(handler_add_strst, lambda message: message.text == "Добавить старосту")
dp.message.register(proc_create_new_strst_2, NewStarosta.Name_startosti)
dp.message.register(handl_excel, lambda message: message.text == "Получить Excel таблицу")
#------- Конец админской части -------------------------------        

#---------- Часть для старосты ----------------------
#dp.message.register(edit_students_0, lambda message:message.text == "Изменить студентов" )
dp.message.register(edit_students_1, edit_students.command)
dp.message.register(edit_students_2, edit_students.name)
dp.message.register(edit_students_3, edit_students.new_value)
#dp.message.register(edit_st_bals_W_file_0,lambda message: message.text == "Изменить баллы" )
dp.message.register(edit_st_bals_W_file_1, File_with_balls.file)
#dp.message.register(add_students_with_file_0, lambda message: message.text == "Добавить студентов файлом")
dp.message.register(add_students_with_file, FOR_Work_w_File.waiting_file )
#dp.message.register(add_students_with_file_0, lambda message: message.text == "Добавить студентов файлом")
dp.message.register(add_students_with_file, FOR_Work_w_File.waiting_file)
dp.message.register(my_students, lambda message: message.text == "Мои студенты")
dp.message.register(my_students_1,deistv_st.name_st )
dp.message.register(add_students,lambda message: message.text == "Добавить студента" )
dp.message.register(proc_create_new_user2, NewUser.text_cell )
dp.message.register(get_urls, lambda message: message.text == "Получить ссылки для студентов")
dp.callback_query.register(clearer_tg_id, lambda c: c.data and c.data.startswith("clear_tg_id"))
#dp.message.register(handl_statistika, lambda message: message.text == "Статистика")                
#-------- Конец части для старосты -------------------------


async def main(message: types.Message = None):
    try:
        # Благодаря этому в консоли появлятся вся информации о работе тг бота
        logging.basicConfig(level=logging.INFO)
        # Назначение выполнение функции чтения данных с таблицы
        scheduler = AsyncIOScheduler()
        scheduler.add_job(reader, 'cron', hour=23, minute =30)
        scheduler.start()
        if scheduler:
            print ("---Задача назначена")

        # Этим мы опрашиваем тг на наличие уведомлений
        await dp.start_polling(bot)
        
    except Exception as e:
        # Получаем строку с информацией об ошибке
        error_message = traceback.format_exc()
        if message:
            await bot.send_message(chat_id=user_id_adm, text="Произошла ошибка:")
            await bot.send_message(chat_id=user_id_adm, text=error_message)
        else:
            logging.error(f"Произошла ошибка: {error_message}")

# Запуск ассинхронной функции main
if __name__ == "__main__":
    asyncio.run(main())