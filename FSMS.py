from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class deistv_st(StatesGroup):
    name_st = State()

class FOR_Work_w_File(StatesGroup):
    waiting_file = State()

class edit_students(StatesGroup):
    command = State()
    name = State()
    new_value = State()

class Some_Students(StatesGroup):
    students = State()
    count = State()
    coment = State()

class File_with_balls(StatesGroup):
    file = State()

class NewUser(StatesGroup):
    text_cell = State()

class deistv_st(StatesGroup):
    name_st = State()

class FOR_Work_w_File(StatesGroup):
    waiting_file = State()

class edit_students(StatesGroup):
    command = State()
    name = State()
    new_value = State()

class Some_Students(StatesGroup):
    students = State()
    count = State()
    coment = State()

class File_with_balls(StatesGroup):
    file = State()
class NewStarosta(StatesGroup):
    Name_startosti = State()
 

class Edit_Starost(StatesGroup):
    comanda = State()
    choised_starosta = State()
    new_name_starosti = State()