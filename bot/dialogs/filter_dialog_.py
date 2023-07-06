from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager, ChatEvent
from aiogram_dialog.widgets.kbd import Button, Row, Checkbox, ManagedCheckboxAdapter
from aiogram_dialog.widgets.text import Format

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
    }

async def send_data(c: CallbackQuery, button: Button, manager: DialogManager):
    city = manager.current_context().start_data.get("city")
    min_price = manager.current_context().start_data.get("min_price")
    max_price = manager.current_context().start_data.get("max_price")
    infrastructure_objects = manager.current_context().start_data.get("infrastructure_objects")
    type_map = manager.current_context().start_data.get("type_map")
    resale = manager.current_context().start_data.get("resale")
    new_building = manager.current_context().start_data.get("new_building")
    data = AnalyticController().get_img_heat_map(city=city,
                                                 min_price=min_price,
                                                 max_price=max_price,
                                                 infrastructure_objects=infrastructure_objects,
                                                 type_map=type_map,
                                                 resale=resale,
                                                 new_building=new_building)
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

async def go_menu_city(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.menu_city)

async def change_infrastructure_objects(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    state = not checkbox.is_checked()
    manager.current_context().start_data["infrastructure_objects"] = state

async def change_type_housing(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    state = not checkbox.is_checked()
    if checkbox.widget.widget_id == "new_building":
        manager.current_context().start_data["new_building"] = state
    if checkbox.widget.widget_id == "resale":
        manager.current_context().start_data["resale"] = state

filter_dialog = Window(
        Format("Привет {user_name}, Город: {city}"),
        Format("Min price: {min_price}"),
        Format("Max price: {max_price}"),
        Format("Infrastructure Objects: {infrastructure_objects}"),
        Format("Type Map: {type_map}"),
        Format("New Building: {new_building}"),
        Format("Resale: {resale}"),
        filter_type_map_dialog,
        Row(
            Checkbox(
                Format(f"✓  New Building"),
                Format(f"New Building"),
                id="new_building",
                default=True,
                on_click=change_type_housing,
            ),
            Checkbox(
                Format(f"✓  Resale"),
                Format(f"Resale"),
                id="resale",
                default=True,
                on_click=change_type_housing,
            ),
        ),
        Checkbox(
            Format(f"✓  Объекты инраструктуры"),
            Format(f"Объекты инраструктуры"),
            id="infrastructure_objects",
            default=True,
            on_click=change_infrastructure_objects,
        ),
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
        Button(Format("Отправить запрос"), id="sendData", on_click=send_data),
        Button(Format("Выбрать город"), id="go_admin", on_click=go_menu_city),
        getter=get_data_filter,
        state=DialogSG.filter,
    )
