from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode, ChatEvent, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Checkbox, ManagedCheckboxAdapter, Group, Radio, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

async def change_repair(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    state = not checkbox.is_checked()
    manager.current_context().start_data["repair"] = state

filter_repair_dialog = Checkbox(
    Format(f"✓  Ремонт"),
    Format(f"Ремонт"),
    id="repair",
    default=True,
    on_click=change_repair,
)
