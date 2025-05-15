from vkbottle.bot import BotLabeler, Message

from utils import get_today, get_tomorrow, get_dates_of_week
from db import db_get_user_group_name
from schedule import get_schedule
from keyboards import KEYBOARD_MENU
from rules import UserExist, UserDoesntExist
from .settings import start

schedule_labeler = BotLabeler()

@schedule_labeler.message(UserExist(), payload={"cmd":'next_week'})
async def next_week_handler(message: Message):
    group_name = db_get_user_group_name(message.from_id)
    week = get_dates_of_week(next=True)
    for day in week:
        await message.answer(get_schedule(day, group_name))

@schedule_labeler.message(UserExist(), payload={"cmd":'this_week'})
async def this_week_handler(message: Message):
    group_name = db_get_user_group_name(message.from_id)
    week = get_dates_of_week()
    for day in week:
        await message.answer(get_schedule(day, group_name))

@schedule_labeler.message(UserExist(), payload={"cmd":'tomorrow'})
async def get_schedule_tomorrow(message: Message):
    group_name = db_get_user_group_name(message.from_id)
    day = get_tomorrow()
    await message.answer(get_schedule(day, group_name), keyboard=KEYBOARD_MENU)

@schedule_labeler.message(UserExist(), payload={"cmd":'today'})
async def get_schedule_today(message: Message):
    group_name = db_get_user_group_name(message.from_id)
    day = get_today()
    await message.answer(get_schedule(day, group_name), keyboard=KEYBOARD_MENU)

@schedule_labeler.message(UserDoesntExist())
async def no_user_handler(message: Message):
    await start(message)

@schedule_labeler.message()
async def other_handler(message: Message):
    await get_schedule_today(message)
