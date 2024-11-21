from aiogram import types
from Db import get_all, est_li_id, zap_user_id, get_all_if, get_specific_value
from config import user_id_adm
from aiogram.filters import CommandStart
from markups import *
from FSMS import *
from aiogram.fsm.context import FSMContext  # Импортируйте FSMContext

async def handler_start(message: types.Message, command: CommandStart,state:FSMContext):
    print ("хэндлер вызван")
    unic_code = command.args
    await state.clear()

    cur_user_id = message.from_user.id
    await message.answer("Этот бот создан для учета баллов в общежитии")
    
    if not ( unic_code  is None ):
        # Перевод в int command.args
        await message.answer(unic_code)
        unic_code = int(unic_code)
    
    just_users_lst = await get_all(Table="Just_users", column_pol="unic_kod")
    starost_lst = await get_all(Table="Starst",  column_pol="unic_kod")

    nalichie_strst = await est_li_id(Table="Starst", user_id=cur_user_id)
    nalichie_usrs = await est_li_id(Table="Just_users", user_id=cur_user_id)

    # Простые пользователи
    if (unic_code in just_users_lst) or (nalichie_usrs==True):
        if nalichie_usrs == False:
            await zap_user_id(Table="Just_users",user_id= cur_user_id, unic_kod=unic_code )
            await message.answer("tg_user_id был добавлен")
        await message.answer("Вы пользователь", reply_markup=markup_for_menu_user)
    
    # Старосты
    if (unic_code in starost_lst) or (nalichie_strst == True) :
        if nalichie_strst == False:
            await zap_user_id(Table="Starst", user_id= cur_user_id, unic_kod=unic_code)
            await message.answer("tg_user_id был добавлен")
        await message.answer("ВЫ староста", reply_markup=markup_for_menu_strst)
    
    # Админ
    if cur_user_id == user_id_adm:
        await message.answer("Здравствуйте, администратор", reply_markup=markup_for_menu_admn)

async def handler_menu_strst (message: types.Message, state: FSMContext):
    #await state.reset_state(with_data = True)
    await state.clear()
    cur_id = message.from_user.id
    list_strst = await get_all(
        Table="Starst",
        column_pol="tg_user_id"
    )

    
    if cur_id in list_strst:
        await message.answer ("Меню для старосты", reply_markup= markup_for_menu_strst)
    elif cur_id == user_id_adm:
        await message.answer("Меню для админа", reply_markup=markup_for_menu_admn)
    else :
        await message.answer("Вас здесь быть не должно: \n /start", reply_markup=ReplyKeyboardRemove)


async def father_handler(message: types.Message):
    await message.answer("Меня создал великолепниший человек, человек с большой буквы, лучший из своего вида @Dan4oke")

async def handl_statistika(message: types.Message):
    cur_user_id = message.from_user.id
    list_stdnts_name = await get_all(
        Table="Just_users",
        column_pol="name"
    )
        
    list_stdnts_balls =await get_all(
        Table="Just_users",
        column_pol="count_b"
    )
    list_stdnts_balls= [0 if x is None else x for x in list_stdnts_balls]

    stdnts_with_balls = {}
    for i in range(len(list_stdnts_name)):
        stdnts_with_balls[list_stdnts_name[i]] = list_stdnts_balls[i]

    sorted_dict ={key : value for key, value in sorted(stdnts_with_balls.items(), key=lambda item: item[1], reverse=True)}

    top_of_bals = ""
    i=1
    for key in sorted_dict:
        top_of_bals= top_of_bals+ f"\n\n{i}. {key}: {sorted_dict[key]}"
        if (i==100): break
        i+=1
    await message.answer(f"Топ студентов по их баллам:{top_of_bals}")
    # ННужно проверить на соответсвтие типов 
    # Для простого юзера
    bool_student = await est_li_id(Table="Just_users", user_id=cur_user_id)
    
    if  bool_student== True:
        stats = await get_all_if(
            table="Just_users",
            column_pol="comment",
            column_poiska="tg_user_id",
            sravn_znach=cur_user_id
        )
        count_b =await get_all_if(
            table="Just_users",
            column_pol="count_b",
            column_poiska="tg_user_id",
            sravn_znach=cur_user_id
        )
        text = stats[0]
        #text = text.replace("None", "")
        await message.answer (f"У вас {count_b} баллов. Вот ваша история:\n{text}")
    
    bool_strst = await est_li_id(Table="Starst", user_id=cur_user_id)

    if bool_strst == True:

        unic_code = await get_specific_value(
            table= "Starst",
            column= "unic_kod", condition_column="tg_user_id",
            condition_value=cur_user_id
        )

        list_comments = await get_all_if(
            table="Just_users", 
            column_poiska="unic_kod_strtsi",
            column_pol="comment", sravn_znach=unic_code
        )

        list_balls = await get_all_if(
            table="Just_users", 
            column_poiska="unic_kod_strtsi",
            column_pol="count_b", sravn_znach=unic_code
        )

        list_names =await get_all_if(
            table="Just_users", 
            column_poiska="unic_kod_strtsi",
            column_pol="name", sravn_znach=unic_code
        )
        text = "Статистика, ваших студентов:"
        for i in range(len(list_names)):
            cur_name = list_names[i]
            text = f"{text} \n\n{cur_name}-- {list_balls[i]}б."
            
        await message.answer(text, reply_markup=markup_menu)
        
    if cur_user_id == user_id_adm:
        
        list_strst_name =await get_all(Table="Starst", column_pol="name")
        list_strst_place =await get_all(Table="Starst", column_pol="place")
        
        text_about_strst = "Старосты:"
        for i in range(len(list_strst_name)):
            text_about_strst= text_about_strst +f"\n{list_strst_name[i]} - {list_strst_place[i]}"
        await message.answer(text= text_about_strst)
