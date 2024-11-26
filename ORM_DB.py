# import aiosqlite
# from config import get_db_connection
# import traceback
# from random import randint
# import sqlite3
# from config import username_bota
# from aiogram import types

# from tortoise import fields
# from tortoise.models import Model

# # Возможное использование tortose ORM

# # На данный момент здесь находится на стадии загатовка
# # однако её использование находится под вопросом
# # из-за сложности и ненадобности её интеграции в уже готовый проект

# class base_model (Model):
#     tg_user_id = fields.IntField()
#     name = fields.CharField(max_length=100)
    
#     @classmethod
#     async def get_all (cls, column:str):
#         return await cls.all().values_list(column, flat=True)

# # В column_poiska должен быть словарь с колонной и чем должны быть равна строка
# # {"name": "Вася"}, здесь name - название колонны, "Вася" - значение по которому мы ищем
#     @classmethod
#     async def get_all_if(cls,column_pol: str, column_poiska):
#         return await cls.filter(**column_poiska).values_list(column_pol, flat=True)
    
#     @classmethod 
#     async def setter_for_bd(
#         cls, column_value_set, 
#         column_value_usl
#     ):
#         try:
#             await cls.filter(**column_value_usl).update(**column_value_set)
#         except Exception as e:
#             print(f"Ошибка при обновленнии {e}")
    

# class starosta(base_model):
#     unic_kod = fields.IntField()
#     place = fields.CharField(max_length=100)
    
    

#     class Meta:
#         table = "Starst"

# class just_user(base_model):
#     unic_kod = fields.IntField()        
#     #username_US = fields.CharField(max_length=100, null = True)
#     unic_kod_strtsi = fields.IntField()

#     class Meta:
#         table = "Just_users"