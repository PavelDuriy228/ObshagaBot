from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import types
from config import user_id_adm, current_dir, bot
from aiogram.types.input_file import FSInputFile
import pandas as pd
from markups import markup_menu
from Db import *
from FSMS import *


async def handle_Edit_Starost_0 (message: types.Message, state: FSMContext):
    keyboard=[
        [KeyboardButton(text="Сменить старосту")],
        [KeyboardButton(text= "Целиком удалить старосту")]
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
    await state.set_state(Edit_Starost.comanda)
    await message.answer("Выберите команду: \nПри смене старосты все данные его студентов будут сохаранены \n\n ПРИ УДАЛЕНИИ СТАРОСТЫ, ВЫ УДАЛЯЕТЕ И СТАРОСТУ И ВСЕХ СТУДЕНТОВ СВЯЗАННЫХ С НИМ", reply_markup=markup)


async def handle_Edit_Starost_1 (message: types.Message, state: FSMContext):
    keyboard =[
        [KeyboardButton(text="В меню")]
    ]
    list_strst = await get_all(
        Table="Starst",
        column_pol="name"
    )
    for i in range(len(list_strst)):
        st_in_button = f"{list_strst[i]}"
        keyboard.append([KeyboardButton(text=f"{st_in_button}")])
    
    markup = ReplyKeyboardMarkup(
        keyboard= keyboard,
        resize_keyboard=True
    )
    mes_from_user = message.text
    if mes_from_user == "Сменить старосту":
        await  state.update_data(com = mes_from_user )
        await message.answer("Выберите кого вы хотите изменить", reply_markup=markup)

    if mes_from_user == "Целиком удалить старосту":
        await  state.update_data(com = mes_from_user )
        await message.answer("ВНИМАНИЕ!! \n\n Выбранный вами староста и его студенты будут удалены", reply_markup=markup)

    if mes_from_user != "Целиком удалить старосту" and  mes_from_user != "Сменить старосту":
        await message.answer("Неверная команда", reply_markup=markup)
        await state.update_data(com = "Неверная команда")

    await state.set_state(Edit_Starost.choised_starosta)

async def handle_Edit_Starost_2 (message: types.Message, state: FSMContext):
    data = await state.get_data()
    com = data.get('com')

    keyboard_adm= [
        [KeyboardButton(text="В меню")],
    ]
    
    
    await state.update_data(user = message.text)
    if com == "Сменить старосту":    
        text = "Введите ФИО (Отчество необязательно) нового старосты, который будет на его месте:\nРоманов Кирилл"
        
    
    if com == "Целиком удалить старосту":
        keyboard_adm.append([KeyboardButton(text = "Да")])
        text = "Введите << Да >>, если вы уверены, что хотите его удалить"

    markup = ReplyKeyboardMarkup(
        keyboard=keyboard_adm,
        resize_keyboard=True
    )   
    await message.answer(
        text= text,
        reply_markup=markup
        )
    await state.set_state(Edit_Starost.new_name_starosti)

async def handle_Edit_Starost_3(message: types.Message, state: FSMContext):
    mes_from_user = message.text
    await state.update_data(new_name = mes_from_user)

    data = await state.get_data()
    name = data['user']
    comand = data['com']
    new_name = data['new_name']

    splited_name = name.split(":")
    just_name = splited_name[0]

    u_code = await get_specific_value(
                table="Starst",
                column="unic_kod", condition_column="name",
                condition_value=name
            )
    if comand == "Сменить старосту":
        await setter_for_bd(
            table="Starst",
            column="tg_user_id", value_for_set=0,
            value_usl=name,
            column_usl="name"
        )
        await setter_for_bd(
            table="Starst",
            column="name", value_for_set=new_name,
            value_usl=name,
            column_usl="name"
        )

        

        await message.answer(f"Теперь староста {splited_name[1]} не {just_name}, а {new_name}", reply_markup=markup_menu)
        await message.answer(f"https://t.me/{username_bota}?start={u_code}")
    
    elif comand == "Целиком удалить старосту" and new_name=="Да":
        
        await deleting_on_DB(
            table="Just_users",
            column_usl_for_del="unic_kod_strtsi",
            znach_usl=u_code
        )
        await deleting_on_DB(
            table="Starst",
            column_usl_for_del="unic_kod",
            znach_usl=u_code
        )
        await message.answer (f"{name} и его студенты удалены", reply_markup=markup_menu )
    else:
        await message.answer("Что то пошло не так")

# Переделать добавление старост, и изменить всё что с этим связано, обработать ошибка
# -----------------------------------------------------------------------------------


async def handler_add_strst(message: types.Message, state: FSMContext):
    await message.answer("Напишите этаж и крыло нового старосты как в примере. \nНапример для  Романова Ромы Романовича - старостыПервого этажа Левого крыла: Романова Ромы Романовича 1Лк")
    await state.set_state(NewStarosta.Name_startosti)

async def proc_create_new_strst_2 (message: types.Message, state: FSMContext):
    if message.from_user.id == user_id_adm:
        await state.update_data(name =  message.text)
        data = await state.get_data()
        name_place = data['name']
        splited = name_place.split(":")
        place = splited[1].strip()

        code = await create_code(table="Starst", diap1=500_000, diap2=1_000_000)
        result = f"{name_place}"
        await message.answer(f"Вот что у вас получилось: {result}")

        await create_new_user(table="Starst", code=code, name=name_place, place=place)
        await message.answer("Ниже будет ссылка, для добавления старосты. Отправьте эту ссылку старосте")
        await message.answer(f"https://t.me/{username_bota}?start={code}")
    else:
        await message.answer("У вас нет на это прав")

async def handl_excel( message: types.Message):
    try:

        list_strsts = await get_all(
            Table="Starst",
            column_pol="name"
        )
        list_ucode_strst = await get_all(
            Table="Starst",
            column_pol="unic_kod"
        )
        print (list_strsts)
        path = f'{current_dir}\общая сводка.xlsx'
        with pd.ExcelWriter(path=path) as writer:
            for i in range(len(list_strsts)):
                list_students = await get_all_if(
                    table="Just_users",
                    column_poiska="unic_kod_strtsi",
                    column_pol="name",
                    sravn_znach= list_ucode_strst[i]
                )
                list_bals_stdnts = await get_all_if(
                    table="Just_users",
                    column_poiska="unic_kod_strtsi",
                    column_pol="count_b",
                    sravn_znach= list_ucode_strst[i]
                )
                list_cmnts_st = await get_all_if(
                    table="Just_users",
                    column_poiska="unic_kod_strtsi",
                    column_pol="comment",
                    sravn_znach= list_ucode_strst[i]
                )
                data = {
                    'Имя':[g.replace(":","-") for g in list_students],
                    'Баллы': [k for k in list_bals_stdnts],
                    'Коментарии': [j for j in list_cmnts_st]
                }
                print(data)
                df1 = pd.DataFrame(data)
                name_lista_exc = list_strsts[i].replace(":","-")
                df1.to_excel(writer, sheet_name=name_lista_exc, index=False)

        document = FSInputFile(path=path)
        if message.from_user.id == user_id_adm:
            await bot.send_document(chat_id=message.chat.id, document=document)
    except Exception as e:
        # Получаем строку с информацией об ошибке
        error_message = traceback.format_exc()
        await message.answer("Произошла ошибка:")
        await message.answer (error_message)

