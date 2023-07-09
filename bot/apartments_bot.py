from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode, ChatEvent, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Checkbox, ManagedCheckboxAdapter, Group, Radio, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

from bot.dialog_s_g import DialogSG
from bot.dialogs.admin_dialog_ import admin_dialog
from bot.dialogs.filter_heat_map_dialog_ import filter_heat_map_dialog
from bot.dialogs.filter_num_floor_dialog_ import main_filter_num_floor
from bot.dialogs.filter_price_dialog_ import main_filter_price
from bot.dialogs.filter_total_area_dialog_ import main_filter_total_area
from bot.dialogs.filter_analytical_map_ import filter_analytical_map
from bot.dialogs.menu_city_dialog_ import menu_city_dialog
from bot.dialogs.user_personal_area_dialog_ import user_personal_area_dialog
from controller.user_controller import UserController

storage = MemoryStorage()
bot = Bot(token="6348872062:AAFFdDz1ZOPEEhf3RdBMnHD7Z5ubYjzEpRA")
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)
main_dialog = Dialog(
    menu_city_dialog,
    admin_dialog,
    filter_heat_map_dialog,
    main_filter_total_area,
    main_filter_price,
    main_filter_num_floor,
    filter_analytical_map,
    user_personal_area_dialog
)
registry.register(main_dialog)

@dp.message_handler(commands=['admin'])
async def start(m: Message, dialog_manager: DialogManager):
    if UserController().check_admin(id_telegram=m.from_user.id):
        tokens = UserController().get_user_by_telegram_id(id_telegram=m.from_user.id).count_token
        await dialog_manager.start(
            state=DialogSG.admin,
            data={
                "tokens": tokens,
                "role": "Админ",
                "city": "Челябинск",
                "min_price": 1000,
                "max_price": 10000000,
                "user_name": m.from_user.full_name,
                "infrastructure_objects": True,
                "type_map": "HeatMap",
                "new_building": True,
                "resale": True,
                "min_floor": 1,
                "max_floor": 10,
                "min_total_area": 20,
                "max_total_area": 50,
                "repair": True,
                "not_repair": True},
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.EDIT)

@dp.message_handler(commands=['user'])
async def start(m: Message, dialog_manager: DialogManager):
    if UserController().check_user(id_telegram=m.from_user.id):
        UserController().save_new_user(user_name=m.from_user.full_name, is_admin=False, id_telegram=m.from_user.id, count_tokens=10)

    role = "Админ" if UserController().check_admin(id_telegram=m.from_user.id) else "Пользователь"

    tokens = UserController().get_user_by_telegram_id(id_telegram=m.from_user.id).count_token

    await dialog_manager.start(
        state=DialogSG.user_personal_area,
        data={
            "tokens": tokens,
            "role": role,
            "city": "Челябинск",
            "min_price": 1000,
            "max_price": 10000000,
            "user_name": m.from_user.full_name,
            "infrastructure_objects": True,
            "type_map": "HeatMap",
            "new_building": True,
            "resale": True,
            "min_floor": 1,
            "max_floor": 10,
            "min_total_area": 20,
            "max_total_area": 50,
            "repair": True,
            "not_repair": True},
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT)

@dp.message_handler(commands=['start'])
async def start(m: Message, dialog_manager: DialogManager):
    if UserController().check_user(id_telegram=m.from_user.id):
        UserController().save_new_user(user_name=m.from_user.full_name, is_admin=False, id_telegram=m.from_user.id, count_tokens=10)

    role = "Админ" if UserController().check_admin(id_telegram=m.from_user.id) else "Пользователь"

    tokens = UserController().get_user_by_telegram_id(id_telegram=m.from_user.id).count_token

    await dialog_manager.start(
        state=DialogSG.menu_city,
        data={
            "tokens": tokens,
            "role": role,
            "city": "Челябинск",
            "min_price": 1000,
            "max_price": 10000000,
            "user_name": m.from_user.full_name,
            "infrastructure_objects": True,
            "type_map": "HeatMap",
            "new_building": True,
            "resale": True,
            "min_floor": 1,
            "max_floor": 10,
            "min_total_area": 20,
            "max_total_area": 50,
            "repair": True,
            "not_repair": True},
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
