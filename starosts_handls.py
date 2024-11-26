from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import types
from config import bot, current_dir, user_id_adm
import pandas as pd
from Db import *
from config import dp
from FSMS import *
from markups import *
import os



async def edit_students_0 (message: types.Message, state: FSMContext):
    keyboard_edit = [
        [KeyboardButton(text="В меню")],
        [KeyboardButton(text="Удалить студента")],
        [KeyboardButton(text="Изменить имя и комнату")],
        [KeyboardButton(text="Поменять старосту студента")]
    ]

    cur_markup = ReplyKeyboardMarkup(
        keyboard=keyboard_edit,
        resize_keyboard=True
    )
    await message.answer("Выберите команду",reply_markup=cur_markup) 
    await state.set_state(edit_students.command)


async def edit_students_1(message: types.Message, state: FSMContext):
    unik_kod_strsti = await get_specific_value(
            table = "Starst", column="unic_kod", 
            condition_column="tg_user_id", 
            condition_value=message.from_user.id
    )
    list_students = await get_all_if(
        table="Just_users",
        column_poiska="unic_kod_strtsi",
        column_pol= "name",
        sravn_znach=unik_kod_strsti
    )
    keyboard = [
        [KeyboardButton(text="В меню")]
    ]

    edit2_keyboard = keyboard
    for i in list_students:
        edit2_keyboard.append([KeyboardButton(text=i)])
    
    
    await message.answer("Прочтите условия", reply_markup=ReplyKeyboardRemove())
    cur_text = message.text
    if cur_text == "Удалить студента":
        otv_text = "ВНИМАНИЕ! \n\nВы полностью и безвозвартно удаляете данные выбранного вами студента "

    elif cur_text == "Изменить имя и комнату":
        otv_text = "Выберите студента, имя которого вы хотите изменить"
    
    elif cur_text == "Поменять старосту студента":
        otv_text ="Выберите студента, старосту которого вы хотите изменить" 

    else:
        otv_text = "Неизвестная команда"    
        edit2_keyboard = keyboard
        cur_text = otv_text
    
    cur_markup = ReplyKeyboardMarkup(
        keyboard=edit2_keyboard,
        resize_keyboard=True
    )
    await state.update_data(com = cur_text)
    await message.answer(text=otv_text, reply_markup=cur_markup)
    await state.set_state(edit_students.name)


async def edit_students_2 (message: types.Message, state: FSMContext):
    await state.update_data(first_value = message.text)
    data = await state.get_data()
    com = data.get('com') 
    name = data.get('first_value')
    keyboard=[
        [KeyboardButton(text="В меню")]
    ]

    if com == "Удалить студента":
        otv_text= f"Отправьте << Да >>, если вы уверены, что хотите удалить студента {name}"
        keyboard.append([KeyboardButton(text="Да")])
    
    elif com == "Изменить имя и комнату":
        otv_text= "Если вы хотите просто поменять комнату введите то же самое имя, но с другой комнатой \n\nОтправьте новые ФИО и № комнаты по образцу: Петя Васильев: 221"

    elif com == "Поменять старосту студента":
        otv_text = "Что бы переназначить старосту студента, вам достаточно просто переслать любое сообщение новой старосты, остальное сделает бот. Если вы отправите свое сообещние, то ничего не изменится"
    
    else:
        otv_text = "Что то пошло не так, начните заново"
    cur_markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard= True
    )
    await message.answer(text= otv_text, reply_markup=cur_markup)
    await state.set_state(edit_students.new_value)


async def edit_students_3 (message: types.Message, state: FSMContext):
    otv_text = "Ошибка изменения студента"
    try:
        await state.update_data(new_value = message.text)

        data = await state.get_data()

        com = data.get('com') 
        name = data.get('first_value')
        new_value = message.text

        if com == "Удалить студента" and new_value=="Да":
            last_comment = await get_specific_value(
                table="Just_users",
                column="comment",
                condition_column="name",
                condition_value= name
            )

            last_bals = await get_specific_value(
                table="Just_users",
                column="count_b",
                condition_column="name",
                condition_value= name
            )
            await deleting_on_DB(
                table="Just_users",
                column_usl_for_del="name",
                znach_usl= name
            )
            otv_text = f"Студент {name} безвозвартно удален. У него было {last_bals} баллов, вот его история: \n{last_comment}"
        
        elif com == "Изменить имя и комнату":
            splited_name = new_value.split(":")
            _ = int(splited_name[1])

            await setter_for_bd(
                table="Just_users", column="name",
                column_usl="name", value_usl=name,
                value_for_set=new_value
            )
            
            otv_text= f"Теперь вместо {name}, будет   {new_value}"
        
        elif com == "Поменять старосту студента":
            unic_code_new_strst= await get_specific_value(
                table = "Starst", column="unic_kod", 
                condition_column="tg_user_id", 
                condition_value= message.from_user.id
            )
            
            if unic_code_new_strst != None:
                await setter_for_bd(
                    table="Just_users", column="unic_kod_strtsi",
                    column_usl="name",
                    value_usl=name, value_for_set=unic_code_new_strst
                )

                name_new_strst = await get_specific_value(
                    table = "Starst", column="name", 
                    condition_column="unic_kod", 
                    condition_value= unic_code_new_strst
                )
                otv_text = f"Теперь староста студента {name} - это {name_new_strst}"
        await message.answer(text = otv_text, reply_markup=markup_menu)
    except Exception as e:
        # Получаем строку с информацией об ошибке
        error_message = traceback.format_exc()
        await message.answer("Произошла ошибка:",reply_markup=  markup_menu )
        await message.answer (error_message)
        

# ------------------------------------------------------------------------
async def edit_st_bals_W_file_0 (message : types.Message, state: FSMContext):
    nal_strst = await est_li_id( 
        Table="Starst", user_id=message.from_user.id
    )
    if nal_strst == True:
        text = "Отправьте файл xls или xlsx, который вы обычно вводите"
        await state.set_state(File_with_balls.file)
    else:
        text = "У вас нет на это прав"
        await state.clear()
    await message.answer(text=text, reply_markup=markup_menu)

async def edit_st_bals_W_file_1 (message: types.Message, state: FSMContext):
    try:
        await state.clear()
        document = message.document
            
        doc_name = document.file_name
        # split полностью всего имени файла: _ - само имя, file_rashirenie - расширение файла
        print(doc_name)
        d_name = doc_name.split(".")
        file_rashirenie = d_name[1]
        print(file_rashirenie)
        # Допустимые расширения
        dopust_rassh = ['xlsx', 'xls']
        # ПРоверка расширения
        if file_rashirenie in dopust_rassh:
            # Получение id документа, отправленного сообщением боту
            file_if = document.file_id
            # 
            file = await bot.get_file (file_if)
            # Куда будет скаан файл
            path_in_lib = f'{current_dir}/download/{doc_name}'
            # Скачивание файла
            await bot.download_file(file.file_path, path_in_lib)
            await message.answer("файл загружен на сервер")

            unic_code_strst = await get_specific_value(
                        table="Starst", column= "unic_kod", 
                        condition_column="tg_user_id", 
                        condition_value=message.from_user.id
            )
            lst_all_users = await get_all_if(
                Table="Just_users",
                column_pol="name",
                column_poiska="unic_kod_strtsi",
                sravn_znach=unic_code_strst
            )
                    
            df = pd.read_excel(path_in_lib)
            for index, row in df.iterrows():
            # row — это Series, представляющий строку
                count_b = 0
                text_info = ""
                # Добавление в список происходит слева на право по столбцам в строке
                for column in df.columns:
                    cur_value= row[column]
                    if column == "ФИО":
                        name = f"{cur_value}"
                    elif column == "Номер комнаты":
                        place = str(cur_value)
                    elif column == "Факультет" or column == "Номер группы" or column == "№":
                        pass
                    elif column == "ИТОГО":
                        count_b = int(row[column])
                    else:
                        if row[column] != 0:
                            text_info = f"{text_info}\n {column}: {row[column]}"
                        else:
                            pass
                name_db = f"{name}: {place}"
                if name_db in lst_all_users:
                    print("Пользователь найден")
                    text = f"{name}:{place} имеет {count_b}, баллов. Вот его история: {text_info}"
                    # Обновление коментариев
                    await setter_for_bd(
                        table="Just_users", column="comment",
                        value_for_set=text_info,
                        value_usl=name_db,
                        column_usl="name"
                    )
                    # Обновление кол-ва баллов
                    await setter_for_bd(
                        table="Just_users", column="count_b",
                        value_for_set=count_b,
                        value_usl=name_db,
                        column_usl="name"
                    )
                    await message.answer(f"Обновление БД:\n\nИнформация о{name_db} обновлена")
                else:
                    await message.answer(f"{name_db}-- не найден")
        os.remove(path_in_lib)
    except Exception as e:
        # Получаем строку с информацией об ошибке
        error_message = traceback.format_exc()
        await message.answer("Произошла ошибка:")
        await message.answer (error_message)


async def add_students_with_file_0(message: types.Message, state: FSMContext):
    
    await message.answer("Отправьте xls или xlsx файл в котором:", reply_markup=markup_menu)
    await message.answer("1) Первый ряд ФИО \n2) Второй ряд комната \n3) Кол-во его балов на данный момент")
    await state.set_state(FOR_Work_w_File.waiting_file)

async def add_students_with_file(message: types.Message, state:FSMContext):
    try:
        await state.clear()
        document = message.document
        
        doc_name = document.file_name
        # split полностью всего имени файла: _ - само имя, file_rashirenie - расширение файла
        print(doc_name)
        d_name = doc_name.split(".")
        file_rashirenie = d_name[1]
        print(file_rashirenie)
        dopust_rassh = ['xlsx', 'xls']
        if file_rashirenie in dopust_rassh:
            #Загрузка файла
            
            file_if = document.file_id
            file = await bot.get_file (file_if)
            path_in_lib = f'{current_dir}/download/{doc_name}'
            await bot.download_file(file.file_path, path_in_lib)
            await message.answer("файл загружен на сервер")

            unic_code_strst = await get_specific_value(
                    table="Starst", column= "unic_kod", 
                    condition_column="tg_user_id", 
                    condition_value=message.from_user.id
            )
            lst_all_users = await get_all(
                Table="Just_users",
                column_pol="name"
            )
                
            df = pd.read_excel(path_in_lib)
            print(df)
            for index, row in df.iterrows():
                    # row — это Series, представляющий строку
                print(f"Строка {index}:")
                user = []
                    # Добавление в список происходит слева на право по столбцам в строке
                for column in df.columns:
                    print(f"{column}: {row[column]}")
                    user.append(row[column])
                if len(user)== 3:
                    name =f"{user[0]}: {str(user[1])}"
                    if name in lst_all_users:
                        await message.answer(f"{name} -уже есть в базе данных")
                    else:
                        bals = user[2]
                        otv = await full_add_student(
                                full_name=name,
                                unic_code=unic_code_strst,
                                count=bals
                        )
                        await message.answer(otv)
            os.remove(path_in_lib)
    except Exception as e:
        # Получаем строку с информацией об ошибке
        error_message = traceback.format_exc()
        await message.answer("Произошла ошибка:")
        await message.answer (error_message)

async def my_students (message: types.Message, state: FSMContext):
    await state.set_state(deistv_st.name_st)
    keyboard =[
        [KeyboardButton(text="В меню")]
    ]
    cur_user_id = message.from_user.id
    unic_kod_strst = await get_specific_value(table="Starst", column="unic_kod", condition_column="tg_user_id", condition_value=cur_user_id)
    names_stndts = await get_all_if(table="Just_users", column_pol="name", column_poiska="unic_kod_strtsi", sravn_znach=unic_kod_strst)
    names_stndts.sort()
    for i in names_stndts:
        keyboard.append([KeyboardButton(text=f"{i}")])
    
    markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
    await message.answer("Выберите студента, историю которого вы хотите посмотреть",reply_markup= markup)
                
#   await message.answer("Если вы передумали на каком-либо этапе нажмити на кнопку под этим сообщением", reply_markup=markup_menu)

# Хуй хуй пизда пизда PEP8 соблюдай
async def my_students_1(message: types.Message, state: FSMContext):
    comm_from_text = message.text
    await state.update_data(name = comm_from_text)
    data = await state.get_data()
        
    name = data['name']
    
        # Добавить асснхронность к БД
    count_b = await get_specific_value(
        table = "Just_users", column="count_b", 
        condition_column="name", 
        condition_value=name
    )
    coment = await get_specific_value(
        table = "Just_users", column="comment", 
        condition_column="name", 
        condition_value=name
    )

        
    await state.clear()
    await message.answer(f"У {name} {count_b} баллов. Вот его история:{coment}",reply_markup=markup_menu)
    


#_____________ Добавление студента ___________________

async def add_students (message: types.Message, state: FSMContext):
    await message.answer ("Введите ФИО и комнаты ваших студентов по образцу Иванов Иван Иванович: ", reply_markup=ReplyKeyboardRemove())
    await message.answer(
        "Иванов Иван Иванович: 345; Романов Алексей Петрович: 221; ... \n После ввода имени поставьте << : >>, затем укажите номер комнаты и после этого добавьте << ; >>, так вы разделите информацию о студентах",
        reply_markup=markup_menu
    )
    await state.set_state(NewUser.text_cell)

async def proc_create_new_user2(message: types.Message, state:FSMContext):
    # Завершение машины состояния
    await state.update_data(text = message.text)
    data = await state.get_data()
    cur_user_id = message.from_user.id
    unic_code_strst = await get_specific_value(table="Starst", column= "unic_kod", condition_column="tg_user_id", condition_value=cur_user_id)
    if type(unic_code_strst) == int:
        big_text = data['text']
        split_for_users = big_text.split(";")
        
        for i in range (0, len(split_for_users)-1):
            # user = split_for_users[i]
            otv = await full_add_student(
                full_name=split_for_users[i],
                unic_code=unic_code_strst,
            )
            await message.answer(otv)
            
    else:
        await message.answer("Вы не можете добавлять студентов! \n/start")

# -----------------------------------

# ----------------------------------
# async def handl_statistika(message: types.Message):
#     cur_user_id = message.from_user.id
#     list_stdnts_name = await get_all(
#         Table="Just_users",
#         column_pol="name"
#     )
        
#     list_stdnts_balls =await get_all(
#         Table="Just_users",
#         column_pol="count_b"
#     )
#     list_stdnts_balls= [0 if x is None else x for x in list_stdnts_balls]

#     stdnts_with_balls = {}
#     for i in range(len(list_stdnts_name)):
#         stdnts_with_balls[list_stdnts_name[i]] = list_stdnts_balls[i]

#     sorted_dict ={key : value for key, value in sorted(stdnts_with_balls.items(), key=lambda item: item[1], reverse=True)}

#     top_of_bals = ""
#     i=1
#     for key in sorted_dict:
#         top_of_bals= top_of_bals+ f"\n\n{i}. {key}: {sorted_dict[key]}"
#         if (i==100): break
#         i+=1
#     await message.answer(f"Топ студентов по их баллам:{top_of_bals}")
#     # ННужно проверить на соответсвтие типов 
#     # Для простого юзера
#     bool_student = await est_li_id(Table="Just_users", user_id=cur_user_id)
    
#     if  bool_student== True:
#         stats = await get_all_if(
#             table="Just_users",
#             column_pol="comment",
#             column_poiska="tg_user_id",
#             sravn_znach=cur_user_id
#         )
#         count_b =await get_all_if(
#             table="Just_users",
#             column_pol="count_b",
#             column_poiska="tg_user_id",
#             sravn_znach=cur_user_id
#         )
#         text = stats[0]
#         #text = text.replace("None", "")
#         await message.answer (f"У вас {count_b} баллов. Вот ваша история:\n{text}")
    
#     bool_strst = await est_li_id(Table="Starst", user_id=cur_user_id)

#     if bool_strst == True:

#         unic_code = await get_specific_value(
#             table= "Starst",
#             column= "unic_kod", condition_column="tg_user_id",
#             condition_value=cur_user_id
#         )

#         list_comments = await get_all_if(
#             table="Just_users", 
#             column_poiska="unic_kod_strtsi",
#             column_pol="comment", sravn_znach=unic_code
#         )

#         list_balls = await get_all_if(
#             table="Just_users", 
#             column_poiska="unic_kod_strtsi",
#             column_pol="count_b", sravn_znach=unic_code
#         )

#         list_names =await get_all_if(
#             table="Just_users", 
#             column_poiska="unic_kod_strtsi",
#             column_pol="name", sravn_znach=unic_code
#         )
#         text = "Статистика, ваших студентов:"
#         for i in range(len(list_names)):
#             cur_name = list_names[i]
#             text = f"{text} \n\n{cur_name}-- {list_balls[i]}б."
            
#         await message.answer(text, reply_markup=markup_menu)
        
#     if cur_user_id == user_id_adm:
        
#         list_strst_name =await get_all(Table="Starst", column_pol="name")
#         list_strst_place =await get_all(Table="Starst", column_pol="place")
        
#         text_about_strst = "Старосты:"
#         for i in range(len(list_strst_name)):
#             text_about_strst= text_about_strst +f"\n{list_strst_name[i]} - {list_strst_place[i]}"
#         await message.answer(text= text_about_strst)

