from aiogram.dispatcher.filters.state import StatesGroup, State

class DialogSG(StatesGroup):
    menu_city = State()
    heat_map_filter = State()
    analytical_map_filter = State()
    admin = State()
    filter_total_area = State()
    filter_price = State()
    filter_num_floor = State()
    user_personal_area = State()
    list_ads = State()
    selected_ad = State()
    selected_user = State()
