from vkbottle import Bot
from config import api, state_dispenser, labeler
from handlers import menu_labeler, settings_labeler, schedule_labeler

labeler.load(settings_labeler)
labeler.load(menu_labeler)
labeler.load(schedule_labeler)

bot = Bot(
    api=api,
    labeler=labeler,
    state_dispenser=state_dispenser,
)

print('Bot is running.')
bot.run_forever()