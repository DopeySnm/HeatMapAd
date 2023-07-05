from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode, ChatEvent, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Checkbox, ManagedCheckboxAdapter, Group, Radio, SwitchTo
from aiogram_dialog.widgets.text import Format, Const
from controller.analytic_controller import AnalyticController

storage = MemoryStorage()
bot = Bot(token="6351864281:AAGnD3Ij4UyF-oHQxScUDjc1iaW8tFueHzQ")
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)

class DialogSG(StatesGroup):
    filter = State()
    admin = State()

async def get_data_admin(dialog_manager: DialogManager, **kwargs):
    return {
        "admin_name": {dialog_manager.current_context().start_data.get("user_name")}
    }

async def get_data_filter(dialog_manager: DialogManager, **kwargs):
    return {
        "user_name": {dialog_manager.current_context().start_data.get("user_name")},
        "city": {dialog_manager.current_context().start_data.get("city")},
        "min_price": {dialog_manager.current_context().start_data.get("min_price")},
        "max_price": {dialog_manager.current_context().start_data.get("max_price")},
    }

async def send_data(c: CallbackQuery, button: Button, manager: DialogManager):
    city = manager.current_context().start_data.get("city")
    min_price = manager.current_context().start_data.get("min_price")
    max_price = manager.current_context().start_data.get("max_price")
    data = AnalyticController().get_img_heat_map(city=city, min_price=min_price, max_price=max_price)
    print(c.from_user.full_name, data)
    await c.message.answer(data)

async def set_filter_price(c: CallbackQuery, button: Button, manager: DialogManager):
    price_values_filter = {
        "plusMillion": 1000000,
        "plusOneHundredThousand": 100000,
        "plusTenThousand": 10000,
        "plusOneThousand": 1000,
        "minusOneThousand": -1000,
        "minusTenThousand": -10000,
        "minusOneHundredThousand": -100000,
        "minusMillion": -1000000
    }
    checkbox_min_price: Checkbox = manager.dialog().find("minPrice")
    checkbox_max_price: Checkbox = manager.dialog().find("maxPrice")
    if checkbox_min_price.is_checked():
        price = manager.current_context().start_data.get("min_price") + price_values_filter[button.widget_id]
        if 0 <= price <= manager.current_context().start_data.get("max_price"):
            manager.current_context().start_data["min_price"] = price

    if checkbox_max_price.is_checked():
        price = manager.current_context().start_data.get("max_price") + price_values_filter[button.widget_id]
        if 0 <= price >= manager.current_context().start_data.get("min_price"):
            manager.current_context().start_data["max_price"] = price

async def change_filter_price(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    if checkbox.widget.widget_id == "minPrice":
        checkbox_find: Checkbox = manager.dialog().find("maxPrice")
        checkbox_find.set_widget_data(manager=manager, value=checkbox.is_checked())

    elif checkbox.widget.widget_id == "maxPrice":
        checkbox_find: Checkbox = manager.dialog().find("minPrice")
        checkbox_find.set_widget_data(manager=manager, value=checkbox.is_checked())

async def go_admin(c: CallbackQuery, button: Button, manager: DialogManager):
    if c.from_user.id == 958962035:
        await manager.dialog().switch_to(DialogSG.admin)

async def go_filter(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.filter)

filter_dialog = Dialog(
    Window(
        Format("Привет, {admin_name}"),
        Format("Админка"),
        Button(Format("К фильтрации"), id="go_filter", on_click=go_filter),
        getter=get_data_admin,
        state=DialogSG.admin,
    ),
    Window(
        Format("Привет {user_name}, Город: {city}"),
        Format("Min price: {min_price}"),
        Format("Max price: {max_price}"),
        Format("Фильтр цены"),
        Row(
            Checkbox(
                Format(f"✓  Min price"),
                Format(f"Min price"),
                id="minPrice",
                default=True,
                on_click=change_filter_price,
            ),
            Checkbox(
                Format(f"✓  Max price"),
                Format(f"Max price"),
                id="maxPrice",
                default=False,
                on_click=change_filter_price,
            ),
        ),
        Row(
            Button(Format("-1к"), id="minusOneThousand", on_click=set_filter_price),
            Button(Format("-10к"), id="minusTenThousand", on_click=set_filter_price),
            Button(Format("-100к"), id="minusOneHundredThousand", on_click=set_filter_price),
            Button(Format("-1м"), id="minusMillion", on_click=set_filter_price),
        ),
        Row(
            Button(Format("+1к"), id="plusOneThousand", on_click=set_filter_price),
            Button(Format("+10к"), id="plusTenThousand", on_click=set_filter_price),
            Button(Format("+100к"), id="plusOneHundredThousand", on_click=set_filter_price),
            Button(Format("+1м"), id="plusMillion", on_click=set_filter_price),
        ),
        Button(Format("Отправить данные"), id="sendData", on_click=send_data),
        Button(Format("К Админке"), id="go_admin", on_click=go_admin),
        getter=get_data_filter,
        state=DialogSG.filter,
    ),
)

registry.register(filter_dialog)

admin_id_list = [958962035]

@dp.message_handler(content_types=['text'])
async def start(m: Message, dialog_manager: DialogManager):
    if m.from_user.id in admin_id_list:
        await dialog_manager.start(state=DialogSG.admin,
                                   data={"city": m.text,
                                         "min_price": 1000,
                                         "max_price": 10000,
                                         "user_name": m.from_user.full_name},
                                   mode=StartMode.RESET_STACK,
                                   show_mode=ShowMode.EDIT)
    else:
        # if m.text == "/start":
        #     await m.answer("Введите название города")
        # else:
        #     if AnalyticController().check_city(m.text):
        await dialog_manager.start(state=DialogSG.filter,
                                   data={"city": m.text,
                                         "min_price": 1000,
                                         "max_price": 10000,
                                         "user_name": m.from_user.full_name},
                                   mode=StartMode.RESET_STACK,
                                   show_mode=ShowMode.EDIT)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
