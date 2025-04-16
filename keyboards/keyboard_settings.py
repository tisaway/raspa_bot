from vkbottle import Keyboard, KeyboardButtonColor, Text

KEYBOARD_SETTINGS = Keyboard(one_time=False, inline=False)
KEYBOARD_SETTINGS.add(Text("❌ Отписаться от рассылки"), color=KeyboardButtonColor.SECONDARY)
KEYBOARD_SETTINGS.add(Text("⚙️ Изменить группу", payload={"cmd":"change_group"}), color=KeyboardButtonColor.SECONDARY)
KEYBOARD_SETTINGS.row()
KEYBOARD_SETTINGS.add(Text("⬅️ Назад", payload={"cmd":'menu'}), color=KeyboardButtonColor.SECONDARY)
KEYBOARD_SETTINGS = KEYBOARD_SETTINGS.get_json()  