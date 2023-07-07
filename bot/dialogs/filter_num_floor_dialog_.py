from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode, ChatEvent, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Checkbox, ManagedCheckboxAdapter, Group, Radio, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

from bot.dialog_s_g import DialogSG

async def get_data_filter(dialog_manager: DialogManager, **kwargs):
    return {
        "min_floor": {dialog_manager.current_context().start_data.get("min_floor")},
        "max_floor": {dialog_manager.current_context().start_data.get("max_floor")},
    }

async def change_filter_num_floor(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    if checkbox.widget.widget_id == "minFloor":
        checkbox_find: Checkbox = manager.dialog().find("maxFloor")
        checkbox_find.set_widget_data(manager=manager, value=checkbox.is_checked())

    elif checkbox.widget.widget_id == "maxFloor":
        checkbox_find: Checkbox = manager.dialog().find("minFloor")
        checkbox_find.set_widget_data(manager=manager, value=checkbox.is_checked())

async def set_filter_num_floor(c: CallbackQuery, button: Button, manager: DialogManager):
    num_floor_values_filter = {
        "plusTen": 10,
        "plusFive": 5,
        "plusTwo": 2,
        "plusOne": 1,
        "minusOne": -1,
        "minusTwo": -2,
        "minusFive": -5,
        "minusTen": -10
    }
    checkbox_min_floor: Checkbox = manager.dialog().find("minFloor")
    checkbox_max_floor: Checkbox = manager.dialog().find("maxFloor")
    if checkbox_min_floor.is_checked():
        num_floor = manager.current_context().start_data.get("min_floor") + num_floor_values_filter[button.widget_id]
        if 0 <= num_floor <= manager.current_context().start_data.get("max_floor"):
            manager.current_context().start_data["min_floor"] = num_floor

    if checkbox_max_floor.is_checked():
        num_floor = manager.current_context().start_data.get("max_floor") + num_floor_values_filter[button.widget_id]
        if 0 <= num_floor >= manager.current_context().start_data.get("min_floor"):
            manager.current_context().start_data["max_floor"] = num_floor

filter_change_floor_dialog = Row(
    Checkbox(
        Format(f"✓  Min Floor"),
        Format(f"Min Floor"),
        id="minFloor",
        default=True,
        on_click=change_filter_num_floor,
    ),
    Checkbox(
        Format(f"✓  Max Floor"),
        Format(f"Max Floor"),
        id="maxFloor",
        default=False,
        on_click=change_filter_num_floor,
    ),
)

filter_minus_value_floor_dialog = Row(
    Button(Format("-1"), id="minusOne", on_click=set_filter_num_floor),
    Button(Format("-2"), id="minusTwo", on_click=set_filter_num_floor),
    Button(Format("-5"), id="minusFive", on_click=set_filter_num_floor),
    Button(Format("-10"), id="minusTen", on_click=set_filter_num_floor),
)

filter_plus_value_floor_dialog = Row(
    Button(Format("+1"), id="plusOne", on_click=set_filter_num_floor),
    Button(Format("+2"), id="plusTwo", on_click=set_filter_num_floor),
    Button(Format("+5"), id="plusFive", on_click=set_filter_num_floor),
    Button(Format("+10"), id="plusTen", on_click=set_filter_num_floor),
)

async def go_filter_3(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.filter)

main_filter_num_floor = Window(
    Format("Min Num Floor: {min_floor}"),
    Format("Max Num Floor: {max_floor}"),
    filter_change_floor_dialog,
    filter_minus_value_floor_dialog,
    filter_plus_value_floor_dialog,
    Button(Format("Выбрать"), id="go_filter_3", on_click=go_filter_3),
    getter=get_data_filter,
    state=DialogSG.filter_num_floor,
)
