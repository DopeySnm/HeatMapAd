from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format

from bot.dialogs.filter_infrastructure_objects_dialog_ import filter_infrastructure_objects_dialog
from bot.dialogs.filter_type_housing_ import filter_type_housing
from bot.dialogs.filter_type_map_dialog_ import filter_type_map_dialog
from controller.analytic_controller import AnalyticController
from bot.dialog_s_g import DialogSG

async def get_data_filter(dialog_manager: DialogManager, **kwargs):
    return {
        "user_name": {dialog_manager.current_context().start_data.get("user_name")},
        "city": {dialog_manager.current_context().start_data.get("city")},
        "min_price": {dialog_manager.current_context().start_data.get("min_price")},
        "max_price": {dialog_manager.current_context().start_data.get("max_price")},
        "infrastructure_objects": {dialog_manager.current_context().start_data.get("infrastructure_objects")},
        "type_map": {dialog_manager.current_context().start_data.get("type_map")},
        "resale": {dialog_manager.current_context().start_data.get("resale")},
        "new_building": {dialog_manager.current_context().start_data.get("new_building")},
        "min_floor": {dialog_manager.current_context().start_data.get("min_floor")},
        "max_floor": {dialog_manager.current_context().start_data.get("max_floor")},
        "min_total_area": {dialog_manager.current_context().start_data.get("min_total_area")},
        "max_total_area": {dialog_manager.current_context().start_data.get("max_total_area")},
    }

async def send_data(c: CallbackQuery, button: Button, manager: DialogManager):
    city = manager.current_context().start_data.get("city")
    min_price = manager.current_context().start_data.get("min_price")
    max_price = manager.current_context().start_data.get("max_price")
    infrastructure_objects = manager.current_context().start_data.get("infrastructure_objects")
    type_map = manager.current_context().start_data.get("type_map")
    resale = manager.current_context().start_data.get("resale")
    new_building = manager.current_context().start_data.get("new_building")
    min_floor = manager.current_context().start_data.get("min_floor")
    max_floor = manager.current_context().start_data.get("max_floor")
    min_total_area = manager.current_context().start_data.get("min_total_area")
    max_total_area = manager.current_context().start_data.get("max_total_area")
    data = AnalyticController().get_img_heat_map(city=city,
                                                 min_price=min_price,
                                                 max_price=max_price,
                                                 infrastructure_objects=infrastructure_objects,
                                                 type_map=type_map,
                                                 resale=resale,
                                                 new_building=new_building,
                                                 min_floor=min_floor,
                                                 max_floor=max_floor,
                                                 min_total_area=min_total_area,
                                                 max_total_area=max_total_area)
    print(c.from_user.full_name, data)
    await c.message.answer(data)

async def go_menu_city(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.menu_city)

async def go_filter_total_area(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.filter_total_area)

async def go_filter_price(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.filter_price)

async def go_filter_num_floor(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.filter_num_floor)

filter_dialog = Window(
        Format("Привет {user_name}, Город: {city}"),
        Format("Min price: {min_price}"),
        Format("Max price: {max_price}"),
        Format("Infrastructure Objects: {infrastructure_objects}"),
        Format("Type Map: {type_map}"),
        Format("New Building: {new_building}"),
        Format("Resale: {resale}"),
        Format("Min Num Floor: {min_floor}"),
        Format("Max Num Floor: {max_floor}"),
        Format("Min Total Area: {min_total_area}"),
        Format("Max Total Area: {max_total_area}"),
        filter_type_map_dialog,
        Button(Format("Фильтр Площади"), id="go_filter_total_area", on_click=go_filter_total_area),
        Button(Format("Фильтр Цены"), id="go_filter_price", on_click=go_filter_price),
        Button(Format("Фильтр Этажей"), id="go_filter_num_floor", on_click=go_filter_num_floor),
        filter_type_housing,
        filter_infrastructure_objects_dialog,
        Button(Format("Выбрать город"), id="go_admin", on_click=go_menu_city),
        Button(Format("Отправить запрос"), id="sendData", on_click=send_data),
        getter=get_data_filter,
        state=DialogSG.filter,
)
