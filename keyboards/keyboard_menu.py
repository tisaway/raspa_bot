from vkbottle import Keyboard, KeyboardButtonColor, Text

KEYBOARD_MENU = Keyboard(one_time=False, inline=False)
KEYBOARD_MENU.add(Text("Сегодня", payload={"cmd":'today'}), color=KeyboardButtonColor.POSITIVE)
# KEYBOARD_MENU.row()
KEYBOARD_MENU.add(Text("Завтра", payload={"cmd":'tomorrow'}), color=KeyboardButtonColor.SECONDARY)
KEYBOARD_MENU.row()
KEYBOARD_MENU.add(Text("Вся неделя", payload={"cmd":'this_week'}), color=KeyboardButtonColor.SECONDARY)
KEYBOARD_MENU.add(Text("Следующая неделя", payload={"cmd":'next_week'}), color=KeyboardButtonColor.SECONDARY)
KEYBOARD_MENU.row()
KEYBOARD_MENU.add(Text("📌 Полезное", payload={"cmd":'resourses'}), color=KeyboardButtonColor.SECONDARY)
KEYBOARD_MENU.add(Text("⚙️ Настройки", payload={"cmd":'settings'}), color=KeyboardButtonColor.SECONDARY)
KEYBOARD_MENU = KEYBOARD_MENU.get_json()  