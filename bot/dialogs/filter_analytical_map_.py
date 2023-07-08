from aiogram.types import CallbackQuery
from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode, ChatEvent, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Checkbox, ManagedCheckboxAdapter, Group, Radio, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

from bot.dialog_s_g import DialogSG
from bot.dialogs.filter_infrastructure_objects_dialog_ import filter_infrastructure_objects_dialog
from controller.analytic_controller import AnalyticController


async def get_data_filter(dialog_manager: DialogManager, **kwargs):
    return {
        "user_name": {dialog_manager.current_context().start_data.get("user_name")},
        "city": {dialog_manager.current_context().start_data.get("city")},
        "infrastructure_objects": {dialog_manager.current_context().start_data.get("infrastructure_objects")},
        "type_map": {dialog_manager.current_context().start_data.get("type_map")},
    }

async def send_data(c: CallbackQuery, button: Button, manager: DialogManager):
    city = manager.current_context().start_data.get("city")
    infrastructure_objects = manager.current_context().start_data.get("infrastructure_objects")
    type_map = manager.current_context().start_data.get("type_map")
    data = AnalyticController().get_img_analytical_map(
        city=city,
        infrastructure_objects=infrastructure_objects,
        type_map=type_map)

    print(c.from_user.full_name, data)
    await c.message.answer(data)

async def go_menu_city(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.menu_city)

async def go_heat_map_filter(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.heat_map_filter)

async def close(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.reset_stack()

filter_analytical_map = Window(
    Format("Привет {user_name}, Город: {city}"),
    Format("Тип карты: {type_map}"),
    Format("Объекты инфраструктуры: {infrastructure_objects}"),
    Button(Format("Тепловая карта"), id="go_heat_map_filter", on_click=go_heat_map_filter),
    filter_infrastructure_objects_dialog,

    Button(Format("Выбрать город"), id="go_city_menu", on_click=go_menu_city),
    Button(Format("Отправить запрос"), id="sendData", on_click=send_data),
    Button(Format("Close"), id="close", on_click=close),
    getter=get_data_filter,
    state=DialogSG.analytical_map_filter
)
