from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode, ChatEvent, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Checkbox, ManagedCheckboxAdapter, Group, Radio, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

from bot.dialog_s_g import DialogSG

async def get_data_filter(dialog_manager: DialogManager, **kwargs):
    return {
        "min_price": {dialog_manager.current_context().start_data.get("min_price")},
        "max_price": {dialog_manager.current_context().start_data.get("max_price")},
    }

async def change_filter_price(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    if checkbox.widget.widget_id == "minPrice":
        checkbox_find: Checkbox = manager.dialog().find("maxPrice")
        checkbox_find.set_widget_data(manager=manager, value=checkbox.is_checked())

    elif checkbox.widget.widget_id == "maxPrice":
        checkbox_find: Checkbox = manager.dialog().find("minPrice")
        checkbox_find.set_widget_data(manager=manager, value=checkbox.is_checked())

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

filter_change_price_dialog = Row(
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
)

filter_minus_value_price_dialog = Row(
    Button(Format("-1к"), id="minusOneThousand", on_click=set_filter_price),
    Button(Format("-10к"), id="minusTenThousand", on_click=set_filter_price),
    Button(Format("-100к"), id="minusOneHundredThousand", on_click=set_filter_price),
    Button(Format("-1м"), id="minusMillion", on_click=set_filter_price),
)

filter_plus_value_price_dialog = Row(
    Button(Format("+1к"), id="plusOneThousand", on_click=set_filter_price),
    Button(Format("+10к"), id="plusTenThousand", on_click=set_filter_price),
    Button(Format("+100к"), id="plusOneHundredThousand", on_click=set_filter_price),
    Button(Format("+1м"), id="plusMillion", on_click=set_filter_price),
)

async def go_filter_2(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.filter)

main_filter_price = Window(
    Format("Min price: {min_price}"),
    Format("Max price: {max_price}"),
    filter_change_price_dialog,
    filter_minus_value_price_dialog,
    filter_plus_value_price_dialog,
    Button(Format("Выбрать"), id="go_filter_2", on_click=go_filter_2),
    getter=get_data_filter,
    state=DialogSG.filter_price,
)
