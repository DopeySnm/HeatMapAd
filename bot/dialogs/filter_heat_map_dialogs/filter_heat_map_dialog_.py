import os
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button, Row
from bot.dialogs.filter_infrastructure_objects_dialog_ import filter_infrastructure_objects_dialog
from bot.dialogs.filter_heat_map_dialogs.filter_repair_dialog_ import filter_repair_dialog
from bot.dialogs.filter_heat_map_dialogs.filter_type_housing_ import filter_type_housing
from controller.analytic_controller import AnalyticController
from bot.dialog_s_g import DialogSG
from db.db_users.db_users_helper import DBHelperUsers


async def get_data_filter(dialog_manager: DialogManager, **kwargs):
    return {
        "user_name": {dialog_manager.current_context().start_data.get("user_name")},
        "role": {dialog_manager.current_context().start_data.get("role")},
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
        "repair": {dialog_manager.current_context().start_data.get("repair")},
        "not_repair": {dialog_manager.current_context().start_data.get("not_repair")}
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
    repair = manager.current_context().start_data.get("repair")
    not_repair = manager.current_context().start_data.get("not_repair")
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
                                                 max_total_area=max_total_area,
                                                 repair=repair,
                                                 not_repair=not_repair,
                                                 id_tg_user=c.from_user.id)
    # print(c.from_user.full_name, data)
    # await c.message.answer(data)
    user = DBHelperUsers().get_user_by_id_telegram(c.from_user.id)
    DBHelperUsers().add_tokens_user_by_id_telegram(-1, user.id_telegram)
    img = open(str(c.from_user.id) + '.png', 'rb')
    await c.bot.send_photo(chat_id=c.message.chat.id, photo=img)
    os.remove(str(c.from_user.id) + '.png')
    os.remove(str(c.from_user.id) + '.html')
    await manager.reset_stack()
    await manager.start(
        state=DialogSG.list_ads,
        data={
            "user": user,
            "list_ad": data,
            "role": "Админ",
            "city": "Челябинск",
        },
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT)

async def go_menu_city(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.menu_city)

async def go_filter_total_area(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.filter_total_area)

async def go_filter_price(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.filter_price)

async def go_filter_num_floor(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.filter_num_floor)

async def go_filter_analytical_map(c: CallbackQuery, button: Button, manager: DialogManager):
    manager.current_context().start_data["type_map"] = "AnalyticalMap"
    await manager.dialog().switch_to(DialogSG.analytical_map_filter)

async def close(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.reset_stack()

filter_heat_map_dialog = Window(
        Format("Привет {user_name}, Роль {role} Город: {city}"),
        Format("Тип карты: {type_map}"),
        Format("Объекты инфраструктуры: {infrastructure_objects}"),
        Format("Цена: от {min_price} до {max_price}"),
        Format("Этаж: от {min_floor} до {max_floor}"),
        Format("Площадь м²: от {min_total_area} до {max_total_area}"),
        Format("C ремонтом: {repair}"),
        Format("Без ремонта: {not_repair}"),
        Format("Новостройка: {new_building}"),
        Format("Вторичное жилье: {resale}"),
        Button(Format("Аналитическая карта"), id="go_filter_analytical_map", on_click=go_filter_analytical_map),
        filter_infrastructure_objects_dialog,
        filter_repair_dialog,
        filter_type_housing,
        Row(
            Button(Format("Площадь"), id="go_filter_total_area", on_click=go_filter_total_area),
            Button(Format("Цена"), id="go_filter_price", on_click=go_filter_price),
            Button(Format("Этаж"), id="go_filter_num_floor", on_click=go_filter_num_floor),
        ),
        Button(Format("Выбрать город"), id="go_city_menu", on_click=go_menu_city),
        Button(Format("Отправить запрос"), id="sendData", on_click=send_data),
        Button(Format("Close"), id="close", on_click=close),
        getter=get_data_filter,
        state=DialogSG.heat_map_filter,
)
