from operator import itemgetter
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format

from bot.dialog_s_g import DialogSG
from controller.user_controller import UserController
from db.db_users.db_users_helper import DBHelperUsers
from models.users.user import User

async def get_data_filter(dialog_manager: DialogManager, **kwargs):
    selected_user: User = dialog_manager.current_context().start_data.get("selected_user")
    user = DBHelperUsers().get_user_by_id_telegram(selected_user.id_telegram)
    dialog_manager.current_context().start_data["user_name"] = user.user_name
    dialog_manager.current_context().start_data["count_token"] = DBHelperUsers().get_tokens_by_user_id(user.id).count_tokens
    dialog_manager.current_context().start_data["is_admin"] = user.is_admin
    return {
        "user_name": {dialog_manager.current_context().start_data.get("user_name")},
        "count_token": {dialog_manager.current_context().start_data.get("count_token")},
        "is_admin": {dialog_manager.current_context().start_data.get("is_admin")},
    }

async def back_admin(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.admin)

async def close_selected_user(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.reset_stack()

async def add_remove_admin(c: CallbackQuery, button: Button, manager: DialogManager):
    user: User = manager.current_context().start_data.get("selected_user")
    DBHelperUsers().add_remove_admin_user_by_telegram_id(user.id_telegram)

async def add_one_token(c: CallbackQuery, button: Button, manager: DialogManager):
    user: User = manager.current_context().start_data.get("selected_user")
    DBHelperUsers().add_tokens_user_by_id_telegram(1, user.id_telegram)

async def remove_one_token(c: CallbackQuery, button: Button, manager: DialogManager):
    user: User = manager.current_context().start_data.get("selected_user")
    DBHelperUsers().add_tokens_user_by_id_telegram(-1, user.id_telegram)

admin_click_user = Window(
    Format("Имя пользователя {user_name}"),
    Format("Токены {count_token}"),
    Format("Права админитратора {is_admin}"),
    Button(Format("Дать/Забрать администратора"), id="add_remove_admin", on_click=add_remove_admin),
    Button(Format("Добавить 1 токен"), id="add_one_token", on_click=add_one_token),
    Button(Format("Убрать 1 токен"), id="remove_one_token", on_click=remove_one_token),
    Button(Format("Назад"), id="back_list_ad", on_click=back_admin),
    Button(Format("Close"), id="close_selected_ad", on_click=close_selected_user),
    getter=get_data_filter,
    state=DialogSG.selected_user
)
