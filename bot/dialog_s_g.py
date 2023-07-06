from aiogram.dispatcher.filters.state import StatesGroup, State

class DialogSG(StatesGroup):
    menu_city = State()
    filter = State()
    admin = State()
