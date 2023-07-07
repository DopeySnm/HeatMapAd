from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode, ChatEvent, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Checkbox, ManagedCheckboxAdapter, Group, Radio, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

from bot.dialog_s_g import DialogSG
from bot.dialogs.admin_dialog_ import admin_dialog
from bot.dialogs.filter_dialog_ import filter_dialog
from bot.dialogs.filter_num_floor_dialog_ import main_filter_num_floor
from bot.dialogs.filter_price_dialog_ import main_filter_price
from bot.dialogs.filter_total_area_dialog_ import main_filter_total_area
from bot.dialogs.filter_type_map_dialog_ import filter_analytical_map
from bot.dialogs.menu_city_dialog_ import menu_city_dialog


storage = MemoryStorage()
bot = Bot(token="6351864281:AAGnD3Ij4UyF-oHQxScUDjc1iaW8tFueHzQ")
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)

main_dialog = Dialog(
    menu_city_dialog,
    admin_dialog,
    filter_dialog,
    main_filter_total_area,
    main_filter_price,
    main_filter_num_floor,
    filter_analytical_map
)
registry.register(main_dialog)

@dp.message_handler(commands=['start'])
async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=DialogSG.menu_city,
        data={
            "city": "Челябинск",
            "min_price": 1000,
            "max_price": 10000,
            "user_name": m.from_user.full_name,
            "infrastructure_objects": True,
            "type_map": "HeatMap",
            "new_building": True,
            "resale": True,
            "min_floor": 1,
            "max_floor": 10,
            "min_total_area": 20,
            "max_total_area": 50,
            "repair": True},
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
