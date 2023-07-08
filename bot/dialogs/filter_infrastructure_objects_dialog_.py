from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode, ChatEvent, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Checkbox, ManagedCheckboxAdapter, Group, Radio, SwitchTo
from aiogram_dialog.widgets.text import Format, Const

async def change_infrastructure_objects(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    state = not checkbox.is_checked()
    manager.current_context().start_data["infrastructure_objects"] = state

filter_infrastructure_objects_dialog = Checkbox(
    Format(f"✓  Объекты инраструктуры"),
    Format(f"Объекты инраструктуры"),
    id="infrastructure_objects",
    default=True,
    on_click=change_infrastructure_objects,
)