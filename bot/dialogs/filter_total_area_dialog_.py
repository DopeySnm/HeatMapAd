from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode, ChatEvent, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Checkbox, ManagedCheckboxAdapter, Group, Radio, SwitchTo
from aiogram_dialog.widgets.text import Format, Const
from bot.dialog_s_g import DialogSG

async def get_data_filter(dialog_manager: DialogManager, **kwargs):
    return {
        "min_total_area": {dialog_manager.current_context().start_data.get("min_total_area")},
        "max_total_area": {dialog_manager.current_context().start_data.get("max_total_area")},
    }

async def change_filter_total_area(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    if checkbox.widget.widget_id == "minTotalArea":
        checkbox_find: Checkbox = manager.dialog().find("maxTotalArea")
        checkbox_find.set_widget_data(manager=manager, value=checkbox.is_checked())

    elif checkbox.widget.widget_id == "maxTotalArea":
        checkbox_find: Checkbox = manager.dialog().find("minTotalArea")
        checkbox_find.set_widget_data(manager=manager, value=checkbox.is_checked())

async def set_filter_total_area(c: CallbackQuery, button: Button, manager: DialogManager):
    num_floor_values_filter = {
        "plusTwenty": 20,
        "plusTen": 10,
        "plusFive": 5,
        "plusOne": 1,
        "minusOne": -1,
        "minusFive": -5,
        "minusTen": -10,
        "minusTwenty": -20
    }
    checkbox_min_total_area: Checkbox = manager.dialog().find("minTotalArea")
    checkbox_max_total_area: Checkbox = manager.dialog().find("maxTotalArea")
    if checkbox_min_total_area.is_checked():
        num_floor = manager.current_context().start_data.get("min_total_area") + num_floor_values_filter[button.widget_id]
        if 0 <= num_floor <= manager.current_context().start_data.get("max_total_area"):
            manager.current_context().start_data["min_total_area"] = num_floor

    if checkbox_max_total_area.is_checked():
        num_floor = manager.current_context().start_data.get("max_total_area") + num_floor_values_filter[button.widget_id]
        if 0 <= num_floor >= manager.current_context().start_data.get("min_total_area"):
            manager.current_context().start_data["max_total_area"] = num_floor

filter_change_total_area = Row(
    Checkbox(
        Format(f"✓  Минимальная площадь"),
        Format(f"Минимальная площадь"),
        id="minTotalArea",
        default=True,
        on_click=change_filter_total_area,
    ),
    Checkbox(
        Format(f"✓  Максимальная площадь"),
        Format(f"Максимальная площадь"),
        id="maxTotalArea",
        default=False,
        on_click=change_filter_total_area,
    ),
)

filter_minus_value_total_area = Row(
    Button(Format("-1"), id="minusOne", on_click=set_filter_total_area),
    Button(Format("-5"), id="minusFive", on_click=set_filter_total_area),
    Button(Format("-10"), id="minusTen", on_click=set_filter_total_area),
    Button(Format("-20"), id="minusTwenty", on_click=set_filter_total_area),
)

filter_plus_value_total_area = Row(
    Button(Format("+1"), id="plusOne", on_click=set_filter_total_area),
    Button(Format("+5"), id="plusFive", on_click=set_filter_total_area),
    Button(Format("+10"), id="plusTen", on_click=set_filter_total_area),
    Button(Format("+20"), id="plusTwenty", on_click=set_filter_total_area),
)

async def go_filter_1(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.heat_map_filter)

main_filter_total_area = Window(
    Format("Площадь м²: от {min_total_area} до {max_total_area}"),
    filter_change_total_area,
    filter_minus_value_total_area,
    filter_plus_value_total_area,
    Button(Format("Выбрать"), id="go_filter_1", on_click=go_filter_1),
    getter=get_data_filter,
    state=DialogSG.filter_total_area,
)
