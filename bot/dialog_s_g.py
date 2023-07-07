from aiogram.dispatcher.filters.state import StatesGroup, State

class DialogSG(StatesGroup):
    menu_city = State()
    filter = State()
    admin = State()
    filter_total_area = State()
    filter_price = State()
    filter_num_floor = State()
