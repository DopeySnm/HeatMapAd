from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup
from aiogram_dialog.widgets.text import Format
from bot.dialog_s_g import DialogSG
from controller.analytic_controller import AnalyticController

def select_city():
    #return AnalyticController().get_list_city()
    return ["Челябинск", "Москва", "Екатеринбург"]

async def go_filter(c: CallbackQuery, button: Button, manager: DialogManager):
    id = int(button.widget_id)
    manager.current_context().start_data["city"] = select_city()[id]
    await manager.dialog().switch_to(DialogSG.filter)

def test_buttons_creator(btn_quantity):
    buttons = []
    counter = 0
    for i in btn_quantity:
        counter = str(counter)
        buttons.append(Button(Format(i), id=counter, on_click=go_filter))
        counter = int(counter)
        counter += 1
    return buttons

test_buttons = test_buttons_creator(select_city())

menu_city_dialog = Window(
    Format("Выберете город"),
    ScrollingGroup(
        *test_buttons,
        id="city_group",
        width=4,
        height=4,
    ),
    state=DialogSG.menu_city,
)
