from vkbottle.bot import BotLabeler, Message
from keyboards import KEYBOARD_MENU, KEYBOARD_SETTINGS
from db import db_get_user_group_name
from rules import UserExist

menu_labeler = BotLabeler()

@menu_labeler.message(UserExist(), payload={"cmd":'menu'})
async def get_menu(message: Message, text='Тыкай'):
    await message.answer(text, keyboard=KEYBOARD_MENU)

@menu_labeler.message(UserExist(), payload={"cmd":'settings'})
async def open_settings(message: Message):
    user_group = db_get_user_group_name(message.from_id)
    text_settings = 'Выбранная группа: ' + user_group + '\nВыбери, что хочешь изменить, или нажми кнопку назад:'
    await message.answer(text_settings, keyboard=KEYBOARD_SETTINGS)

@menu_labeler.message(UserExist(), payload={"cmd":'resourses'})
async def open_resourses(message: Message):
    text_resourses = '🔗 Сайт с расписанием:\nhttp://inet.ibi.spb.ru/raspisan\n\n🔗 Группа МБИ в Вконтакте:\nhttps://vk.com/ibispb\n\n🔗 Группа МБИ в Telegram:\nhttps://t.me/ibispb_ru'
    await message.answer(text_resourses, keyboard=KEYBOARD_MENU)

