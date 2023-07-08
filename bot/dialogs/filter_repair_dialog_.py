from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode, ChatEvent, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Checkbox, ManagedCheckboxAdapter, Group, Radio, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

async def change_repair(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    state = not checkbox.is_checked()
    # manager.current_context().start_data["repair"] = state
    if checkbox.widget.widget_id == "repair":
        manager.current_context().start_data["repair"] = state
    if checkbox.widget.widget_id == "not_repair":
        manager.current_context().start_data["not_repair"] = state


filter_repair_dialog = Row(
    Checkbox(
        Format(f"✓  Ремонт"),
        Format(f"Ремонт"),
        id="repair",
        default=True,
        on_click=change_repair,
    ),
    Checkbox(
        Format(f"✓  Без ремонта"),
        Format(f"Без ремонта"),
        id="not_repair",
        default=True,
        on_click=change_repair,
    )
)
