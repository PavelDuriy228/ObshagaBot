from config import wks, bot, user_id_adm
from Db import get_specific_value, setter_for_bd, full_add_student, deleting_on_DB
from Db import get_all

# Изменения баллов и коментариев
async def setter_bals_coms(name, comment, all_count):
    # Вставка коментариев
    await setter_for_bd(
        table="Just_users",
        column="comment",
        value_for_set=comment,
        column_usl="name",
        value_usl=name
    )
    # Вставка баллов
    await setter_for_bd(
        table="Just_users",
        column="count_b",
        value_for_set=all_count,
        column_usl="name",
        value_usl=name
    )

# Создание юзера
async def creat_user(name_sheet, name, u_code_strsti, comment, all_count):
    print(f"sheet {name_sheet}")
    tg_user_id_strst = await get_specific_value(
         table= "Starst",
         column="tg_user_id", 
         condition_column="place",
         condition_value=str(name_sheet)
    )
    
    if not( tg_user_id_strst is None):

        url = await full_add_student(
            full_name= name,
            unic_code= int(u_code_strsti),                    
        )                       
        await bot.send_message(tg_user_id_strst, "Этого человека не было в БД")
        await bot.send_message(tg_user_id_strst, url)
    await setter_bals_coms(
        name=name,
        comment=comment,
        all_count=all_count
    )

async def reader ():
    print ("----- Функция reader была вызвана ----")
    mess= "Обновление БД - было совершено"
    #Отпарвление сообщении админу об обновлении БД
    await bot.send_message(user_id_adm, mess)
    # список листов
    sheet_names = wks.worksheets()    
    for sheet in sheet_names:                
        name_sheet = sheet.title
        print (f"----Был открыт лист -{str(name_sheet)}")
        cur_wks = wks.worksheet(name_sheet)
        name_sheet = str(name_sheet).strip()
        # Получение первой строки
        title = sheet.row_values(1)        
        title = title[5:]
        rows = cur_wks.get_all_values()
        rows = rows[1:]
# ------------------------
        places = await get_all (
            Table="Starst",
            column_pol="place"
        )
        print(places)
        # Получение ю-кода старосты
        u_code_strsti = await get_specific_value(
            table= "Starst",
            column="unic_kod", 
            condition_column="place",
            condition_value=name_sheet
        )
        print(f"Code STRST: {u_code_strsti}")
        for row in rows:
            name = f"{str(row[1]).strip()}: {str(row[2]).strip()}"
            print(f"name: {name}")
            all_count = 0
            row= row[5:]
            comment = ""
            for i in range(len(title)):
                zasl= title[i]
                count = row[i]
                if count!="" or count!='0': 
                    all_count= all_count + int(count)
                    if comment=="": comment= f"{zasl}: {count};"
                    else : comment= f"{comment}\n{zasl}: {count};"
            print()
            
            print (f"comment: {comment}")
            print(f"---ful: {all_count}")
            print (row)
            print("--------------------------------------")
            u_code_stud = await get_specific_value(
                table="Just_users",
                column="unic_kod_strtsi",
                condition_column="name",
                condition_value=name
            )
            print(f"u_str_sud^ {u_code_stud}")
            if u_code_strsti == u_code_stud and not( u_code_stud is None):
                await setter_bals_coms(
                    name=name,
                    comment=comment,
                    all_count=all_count
                )
            elif (u_code_stud is None):
                print("Такого целиком нету")
                await creat_user(
                    name=name,
                    name_sheet=str(name_sheet),
                    u_code_strsti= u_code_strsti,
                    comment=comment,
                    all_count=all_count
                )
            elif u_code_strsti != u_code_stud and not( u_code_stud is None):                
                print("ЕСть не совпадение")
                # Удаление клона
                await deleting_on_DB(
                    table="Just_users",
                    column_usl_for_del="name",
                    znach_usl=name
                )                
                await creat_user(
                    name=name,
                    name_sheet=name_sheet,
                    u_code_strsti= u_code_strsti,
                    comment=comment,
                    all_count=all_count
                )


            
            