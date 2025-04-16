class Schedule:
    def __init__(self, date, group):
        self.date = date 
        self.group = group
        self.lessons = []

    def __str__(self):
        lines = [' '.join(['Расписание группы', self.group, 'на', self.date.strftime("%d.%m")])]
        lines.append('\n\n\n'.join(self.lessons))
        return '\n\n'.join(lines)

class Lesson:
    def __init__(self, time):
        self.time = time
        self.subjects = []
    
    def __str__(self):
        lines = []
        lines.append(' '.join(['⏰', self.time]))
        lines.append('\n\n'.join(self.subjects))
        return '\n'.join(lines)
    
class ValidateValue:
    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.private_name, None)

    def __set__(self, instance, value):
        if type(value) != str:
            raise TypeError("Значение атрибута должно быть строковым.")
        value = value.strip()
        value = value.replace('\n', '')
        setattr(instance, self.private_name, value)

class Subject:
    name = ValidateValue()
    type = ValidateValue()
    teacher = ValidateValue()
    classroom = ValidateValue()
    additional_info = ValidateValue()
    link = ValidateValue()

    def __init__(self):
        self._lesson_break = False
        self.name = ''
        self.type = ''
        self.teacher = ''
        self.classroom = ''
        self.additional_info = ''
        self.link = ''

    @property
    def lesson_break(self):
        return self._lesson_break
 
    @lesson_break.setter
    def lesson_break(self, value):
        if type(value) != bool:
            raise TypeError("Lesson_break должен быть bool.")
        self._lesson_break = value

    def __str__(self):
        if self.lesson_break:
            return 'Окно. Отдыхай :з'
        lines = []
        lines.append(', '.join([self.name, self.type]))
        lines.append(', '.join([self.teacher, self.classroom]))
        if self.additional_info: lines.append(self.additional_info) 
        if self.link: lines.append('Онлайн 🟢 ' + self.link)
        return '\n'.join(lines)