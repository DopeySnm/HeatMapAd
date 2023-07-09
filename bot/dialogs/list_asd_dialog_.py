from operator import itemgetter
from typing import Any
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button, Row, ScrollingGroup, Select, Group
from bot.dialogs.filter_infrastructure_objects_dialog_ import filter_infrastructure_objects_dialog
from bot.dialogs.filter_heat_map_dialogs.filter_repair_dialog_ import filter_repair_dialog
from bot.dialogs.filter_heat_map_dialogs.filter_type_housing_ import filter_type_housing
from controller.analytic_controller import AnalyticController
from bot.dialog_s_g import DialogSG
from db.db_users.db_users_helper import DBHelperUsers

async def ads_getter(dialog_manager: DialogManager, **kwargs):
    ads = dialog_manager.current_context().start_data.get("list_ad")
    data = []

    for ad in ads:
        data.append([ad.title, ad.id])
    return {"ads": data}

async def click_ad(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    ads = manager.current_context().start_data.get("list_ad")
    for ad in ads:
        if ad.id == int(item_id):
            manager.current_context().start_data["ad_title"] = ad.title
            manager.current_context().start_data["lick_ad"] = ad.link
            manager.current_context().start_data["full_address"] = ad.location.full_address
            test = manager.current_context().start_data.get("lick_ad")
            await manager.dialog().switch_to(DialogSG.selected_ad)


list_ads_dialog = Window(
    Format("Выберете Объявление"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            id="select_ad",
            items="ads",
            item_id_getter=itemgetter(1),
            on_click=click_ad,
        ),
        id="ads_group",
        width=1,
        height=6,
    ),
    getter=ads_getter,
    state=DialogSG.list_ads,
)
