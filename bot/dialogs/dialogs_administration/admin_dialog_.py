from operator import itemgetter
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format

from bot.dialog_s_g import DialogSG
from controller.user_controller import UserController

# async def get_data_admin(dialog_manager: DialogManager, **kwargs):
#     return {
#         "user_name": {dialog_manager.current_context().start_data.get("user_name")}
#     }
#
# def user_list_city():
#     return UserController().get_list_user()
#
# async def click_by_user(c: CallbackQuery, button: Button, manager: DialogManager):
#     id = int(button.widget_id)
#     UserController().add_tokens_user_by_id_telegram(1, user_list_city()[id].id_telegram)
#
# def user_buttons_creator(btn_quantity):
#     buttons = []
#     counter = 0
#     for i in btn_quantity:
#         user_name = user_list_city()[counter].user_name
#         user_token = user_list_city()[counter].count_token
#         info = user_name + " " + str(user_token)
#         counter = str(counter)
#         buttons.append(Button(Format(info), id=counter, on_click=click_by_user))
#         counter = int(counter)
#         counter += 1
#     return buttons
#
# user_buttons = user_buttons_creator(user_list_city())
#
# async def close(c: CallbackQuery, button: Button, manager: DialogManager):
#     await manager.reset_stack()
#
# admin_dialog = Window(
#     Format("Привет, {user_name}"),
#     Format("Админка"),
#     Format("Нажмите чтобы добавить +1 токен"),
#     ScrollingGroup(
#         Select(
#             Format("{item[0]}"),
#             id="select_ad",
#             items="ads",
#             item_id_getter=itemgetter(1),
#             on_click=click_ad,
#         ),
#         id="city_group",
#         width=4,
#         height=4,
#     ),
#     Button(Format("Close"), id="close", on_click=close),
#     getter=get_data_admin,
#     state=DialogSG.admin,
# )


async def admin_getter(dialog_manager: DialogManager, **kwargs):
    users = dialog_manager.current_context().start_data.get("user_list")
    data = []
    for user in users:
        data.append([user.user_name, user.id_telegram])
    return {"users": data}

async def click_user(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    users = manager.current_context().start_data.get("user_list")
    for user in users:
        if user.id_telegram == int(item_id):
            manager.current_context().start_data["selected_user"] = user
            await manager.dialog().switch_to(DialogSG.selected_user)

async def close_admin(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.reset_stack()

admin_dialog = Window(
    Format("Выберете Пользователя"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            id="select_ad",
            items="users",
            item_id_getter=itemgetter(1),
            on_click=click_user,
        ),
        id="user_group",
        width=1,
        height=6,
    ),
    Button(Format("Close"), id="close_admin", on_click=close_admin),
    getter=admin_getter,
    state=DialogSG.admin,
)
