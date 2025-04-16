from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule
from db import db_user_exist

class UserExist(ABCRule[Message]):
    async def check(self, message: Message) -> bool:
        return db_user_exist(message.from_id)
    
class UserDoesntExist(ABCRule[Message]):
    async def check(self, message: Message) -> bool:
        return not db_user_exist(message.from_id)