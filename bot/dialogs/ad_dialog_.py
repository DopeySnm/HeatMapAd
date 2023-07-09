from operator import itemgetter
from typing import Any
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button, Row, ScrollingGroup, Select, Group, Url
from bot.dialogs.filter_infrastructure_objects_dialog_ import filter_infrastructure_objects_dialog
from bot.dialogs.filter_heat_map_dialogs.filter_repair_dialog_ import filter_repair_dialog
from bot.dialogs.filter_heat_map_dialogs.filter_type_housing_ import filter_type_housing
from controller.analytic_controller import AnalyticController
from bot.dialog_s_g import DialogSG
from db.db_users.db_users_helper import DBHelperUsers

async def button_ad_favourites(c: CallbackQuery, button: Button, manager: DialogManager):
    pass

async def get_data_filter(dialog_manager: DialogManager, **kwargs):
    return {
        "ad_title": {dialog_manager.current_context().start_data.get("ad_title")},
        'lick_ad': {dialog_manager.current_context().start_data.get("lick_ad")},
        "full_address": {dialog_manager.current_context().start_data.get("full_address")},
    }

selected_ad_dialog = Window(
    Format("{ad_title}"),
    Format("{full_address}"),
    Url(
        url=Format("{link_ad}"),
        text=Format("{ad_title}"),
    ),
    Button(Format("Добавить в избраное"), id="button_ad_favourites", on_click=button_ad_favourites),
    getter=get_data_filter,
    state=DialogSG.selected_ad
)
