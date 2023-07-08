from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode, ChatEvent, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Checkbox, ManagedCheckboxAdapter, Group, Radio, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

async def change_type_housing(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    state = not checkbox.is_checked()
    if checkbox.widget.widget_id == "new_building":
        manager.current_context().start_data["new_building"] = state
    if checkbox.widget.widget_id == "resale":
        manager.current_context().start_data["resale"] = state

filter_type_housing = Row(
    Checkbox(
        Format(f"✓  Новостройка"),
        Format(f"Новостройка"),
        id="new_building",
        default=True,
        on_click=change_type_housing,
    ),
    Checkbox(
        Format(f"✓  Вторичное жилье"),
        Format(f"Вторичное жилье"),
        id="resale",
        default=True,
        on_click=change_type_housing,
    )
)
