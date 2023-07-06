from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode, ChatEvent, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Checkbox, ManagedCheckboxAdapter, Group, Radio, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

async def change_type_map(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    state = not checkbox.is_checked()
    if state:
        manager.current_context().start_data["type_map"] = "HeatMap"
    else:
        manager.current_context().start_data["type_map"] = "AnalyticalMap"

filter_type_map_dialog = Checkbox(
            Format(f"✓  Тепловая карта"),
            Format(f"✓  Аналитическая карта"),
            id="type_map",
            default=True,
            on_click=change_type_map,
        )