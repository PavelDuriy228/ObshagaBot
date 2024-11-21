from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

keyboard =[
        [KeyboardButton(text="В меню")]
    ]

menu_keyboard_for_strst =[
    [KeyboardButton(text="Добавить студента")],
    [KeyboardButton(text="Изменить баллы")],
    [KeyboardButton(text="Мои студенты")],
    [KeyboardButton(text="Статистика")],
    [KeyboardButton(text="Добавить студентов файлом")],
    [KeyboardButton(text="Изменить студентов")]
]
menu_keyboard_for_admin =[
    [KeyboardButton(text="Добавить старосту")],
    [KeyboardButton(text="Статистика")],
    [KeyboardButton(text="Изменение старост")],
    [KeyboardButton(text="Получить Excel таблицу")]
]

menu_keyboard_for_user = [
    [KeyboardButton(text="Статистика")]
]

markup_for_menu_user = ReplyKeyboardMarkup(
    keyboard=menu_keyboard_for_user,
    resize_keyboard= True
)

markup_for_menu_strst= ReplyKeyboardMarkup(
    keyboard=menu_keyboard_for_strst,
    resize_keyboard=True
)
markup_for_menu_admn= ReplyKeyboardMarkup(
    keyboard=menu_keyboard_for_admin,
    resize_keyboard=True
)

markup_menu = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )