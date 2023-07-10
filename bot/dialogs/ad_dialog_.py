from operator import itemgetter
from typing import Any
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row, ScrollingGroup, Select, Group, Url
from bot.dialogs.filter_infrastructure_objects_dialog_ import filter_infrastructure_objects_dialog
from bot.dialogs.filter_heat_map_dialogs.filter_repair_dialog_ import filter_repair_dialog
from bot.dialogs.filter_heat_map_dialogs.filter_type_housing_ import filter_type_housing
from controller.analytic_controller import AnalyticController
from bot.dialog_s_g import DialogSG
from db.db_users.db_users_helper import DBHelperUsers
from models.users.favourites import Favourites
from models.users.user import User


async def button_ad_favourites(c: CallbackQuery, button: Button, manager: DialogManager):
    link_ad = manager.current_context().start_data.get("link_ad")
    user: User = DBHelperUsers().get_user_by_id_telegram(c.from_user.id)
    favorites = Favourites(link_ad, user)
    DBHelperUsers().insert_favourites(favorites)

async def back_list_ad(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to(DialogSG.list_ads)

async def close_selected_ad(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.reset_stack()

async def get_data_filter(dialog_manager: DialogManager, **kwargs):
    return {
        "ad_title": {dialog_manager.current_context().start_data.get("ad_title")},
        "link_ad": {dialog_manager.current_context().start_data.get("link_ad")},
        "full_address": {dialog_manager.current_context().start_data.get("full_address")},
    }

selected_ad_dialog = Window(
    Format("{ad_title}"),
    Format("{full_address}"),
    Format("{link_ad}"),
    Button(Format("Добавить в избранное"), id="button_ad_favourites", on_click=button_ad_favourites),
    Button(Format("Назад"), id="back_list_ad", on_click=back_list_ad),
    Button(Format("Close"), id="close_selected_ad", on_click=close_selected_ad),
    getter=get_data_filter,
    state=DialogSG.selected_ad
)
