from vkbottle.bot import BotLabeler, Message
from keyboards import KEYBOARD_SETTINGS
from vkbottle import BaseStateGroup
from config import state_dispenser
from db import db_insert_new_user
from schedule import validate_group_name
from .menu import get_menu

settings_labeler = BotLabeler()

class SuperStates(BaseStateGroup):
    GROUP = 0  

@settings_labeler.message(payload={"cmd":"start"})
async def start(message: Message):
    await state_dispenser.set(message.peer_id, SuperStates.GROUP)
    text = "Привет! Прежде, чем начать, введи номер группы, например: 113-ПИвЭ."
    await message.answer(text, keyboard=KEYBOARD_SETTINGS)
    
@settings_labeler.message(payload={"cmd":"change_group"})
async def change_group(message: Message):
    await state_dispenser.set(message.peer_id, SuperStates.GROUP)
    text = "Введи номер группы, например: 121. Убедись, что используешь полное название: 103-ПИвЭ, а не 103. Если всё ещё не получается, значит, твоей группы нет в расписании на сайте вуза и мне негде его взять. Подожди :)"
    await message.answer(text, keyboard=KEYBOARD_SETTINGS)

@settings_labeler.message(payload={"cmd":"menu"}, state=SuperStates.GROUP)
async def exit(message: Message):
    await state_dispenser.delete(message.peer_id)
    await get_menu(message)

@settings_labeler.message(state=SuperStates.GROUP)
async def handle_group(message: Message):
    group = validate_group_name(message.text)
    if group:
        db_insert_new_user(message.from_id, group)
        await state_dispenser.delete(message.peer_id)
        text = "Группа введена успешно."
        await get_menu(message, text)
    else:
        return "Неправильный номер группы. Нужно ввести еще раз" 
    