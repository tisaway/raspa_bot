import os
from dotenv import load_dotenv
from vkbottle import API, BuiltinStateDispenser
from vkbottle.bot import BotLabeler

load_dotenv()
TOKEN = os.getenv("TOKEN")

api = API(TOKEN)
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()