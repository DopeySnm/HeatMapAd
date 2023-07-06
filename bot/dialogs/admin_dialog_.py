from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format

from bot.dialog_s_g import DialogSG


async def get_data_admin(dialog_manager: DialogManager, **kwargs):
    return {
        "admin_name": {dialog_manager.current_context().start_data.get("user_name")}
    }

async def go_filter(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.filter)

admin_dialog = Window(
    Format("Привет, {admin_name}"),
    Format("Админка"),
    # Button(Format("Начать Запрос"), id="go_filter", on_click=go_filter),
    getter=get_data_admin,
    state=DialogSG.admin,
)
