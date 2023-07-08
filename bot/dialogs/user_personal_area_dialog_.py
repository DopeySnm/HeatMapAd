from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format

from bot.dialog_s_g import DialogSG

async def get_data_admin(dialog_manager: DialogManager, **kwargs):
    return {
        "user_name": {dialog_manager.current_context().start_data.get("user_name")},
        "role": {dialog_manager.current_context().start_data.get("role")},
        "tokens": {dialog_manager.current_context().start_data.get("tokens")},
    }

async def close(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.reset_stack()

user_personal_area_dialog = Window(
    Format("Привет, {user_name}"),
    Format("У вас {tokens} токенов"),
    Format("Роль {role}"),
    Button(Format("Close"), id="close", on_click=close),
    getter=get_data_admin,
    state=DialogSG.user_personal_area,
)
