import aiosqlite
from config import get_db_connection
import traceback
from random import randint
import sqlite3
from config import username_bota

# Получение всех юзеров
async def get_all (Table: str, column_pol: str ):
    async with aiosqlite.connect(get_db_connection()) as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'''
            SELECT {column_pol} FROM {Table}
            ''')
            rows =await cursor.fetchall()
        return [row[0] for row in rows]

async def get_all_if (table: str, column_pol:str, column_poiska: str, sravn_znach: str):
    async with aiosqlite.connect(get_db_connection()) as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'''
            SELECT {column_pol} FROM {table}
            WHERE {column_poiska} = ?
            ''', (sravn_znach,))
            rows =await cursor.fetchall()
        return [row[0] for row in rows]

# Сеттер в БД
async def setter_for_bd (
        table: str, column:str, value_for_set,
        value_usl, column_usl
):
    try:
        async with aiosqlite.connect(get_db_connection()) as db:
            async with db.cursor() as cursor:
                await cursor.execute(f'''
                UPDATE {table} 
                SET {column} = ?
                WHERE {column_usl} =?
                ''', (value_for_set, value_usl))
                await db.commit()
    except Exception as e:
        # Получаем строку с информацией об ошибке
        error_message = traceback.format_exc()
        print("Произошла ошибка:")
        print(error_message)

# Созадние старосты
async def create_new_user(table:str, code:int, name:str, place:str):
    async with aiosqlite.connect(get_db_connection()) as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'''
            INSERT INTO {table} (unic_kod, name, place) 
            VALUES (?, ?, ?)
            ''', (code, name,place,))
            await db.commit()

# функция для проверки нахождения в БД tg_id
async def est_li_id(Table: str, user_id: int):
    async with aiosqlite.connect(get_db_connection()) as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'''
            SELECT tg_user_id FROM {Table}
            ''')
            rows =await cursor.fetchall()
            lst = [row[0] for row in rows]
        return user_id in lst

# Полчуение списка всех кодов
async def get_codes (Table: str):
    async with aiosqlite.connect(get_db_connection()) as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'''
            SELECT unic_kod FROM {Table}
            ''')
            rows =await cursor.fetchall()
            return [row[0] for row in rows] if rows else []

# СОздание уникального кода
async def create_code(table: str, diap1:int , diap2:int):
    while True:
        code = randint(diap1, diap2)
        lst = await get_codes(Table=table)
        lst=lst.sort()
        if lst is None:
            return code
            #return await create_new_user(table=table, code=code)
        if code not in lst:
            return code
            #return await create_new_user(table=table, code=code)

# Запись user_id
# Table - таблица; 
async def zap_user_id(Table: str, user_id: int, unic_kod: int):
    try:
        async with aiosqlite.connect(get_db_connection()) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f'''
                UPDATE {Table} 
                SET tg_user_id = ?
                WHERE unic_kod = ?
                ''', (user_id, unic_kod))
                await conn.commit()
    except sqlite3.Error as e:
        print(f"Произшла ошибка при обновлении базы данных {e}")
        conn.rollback()

async def get_value_just_users(
        column:str, conditioanl_column1: str, 
        conditinal_column2: str,
        conditioanl_value:str,
        conditioanal_value2:str
        ):
    async with aiosqlite.connect(get_db_connection()) as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'''
            SELECT {column} FROM Just_users 
            WHERE 
            {conditioanl_column1} = ? AND {conditinal_column2}=?
            ''',(conditioanl_value,conditioanal_value2,))
            result = await cursor.fetchone()
        
        return result[0] if result else None

# Функция для создания нового студента
async def create_new_just_user(code:int, name:str, strst_unic_code:int, count=0 ):
    async with aiosqlite.connect(get_db_connection()) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(f'''
            INSERT INTO Just_users (unic_kod, name, count_b, unic_kod_strtsi) 
            VALUES (?, ?, ?, ?)
            ''', (code, name, count , strst_unic_code,))
            await conn.commit()

# Функция для получения чего либо 
async def get_specific_value(table: str, column: str, condition_column: str, condition_value: int):
    async with aiosqlite.connect(get_db_connection()) as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'''
            SELECT {column} FROM {table} WHERE {condition_column} = ?
            ''', (condition_value,))
            result = await cursor.fetchone()
        
        return result[0] if result else None

async def full_add_student (full_name: str,unic_code: int, count=0 ):
    try:
        user2 = full_name.split(":")
        name = user2[0]
        _ = int(user2[1])
        code = await create_code(table="Just_users",diap1=1, diap2=499_999 )

        await create_new_just_user( name =full_name, code=code, strst_unic_code=unic_code, count=count )
        return f"Вот что получислось: \n{full_name} \nСсылка для вашего подопечного: \nhttps://t.me/{username_bota}?start={code}"
        #await message.answer(f"Вот что получислось: \n{user} \nСсылка для вашего подопечного: \nhttps://t.me/{username_bota}?start={code}")
    except:
        return "Ошибка при добавлении этого студента"

async def deleting_on_DB(table:str, column_usl_for_del:str, znach_usl):
    async with aiosqlite.connect(get_db_connection()) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(f'''
            DELETE FROM {table} WHERE {column_usl_for_del} = ?
            ''', (znach_usl,))
            await conn.commit()
