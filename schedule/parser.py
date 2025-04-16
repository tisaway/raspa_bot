import requests
from bs4 import BeautifulSoup
from re import search, sub
from .schedule_class import *

URL = 'http://inet.ibi.spb.ru/raspisan/menu.php?tmenu=1'


# Возвращает с сайта вуза словарь, где ключ - наименование группы, а значение - ее код
def get_groups(level='0'):
    response = requests.get(URL + '/menu.php?tmenu=12&cod=' + level)
    soup = BeautifulSoup(response.text, 'html.parser')
    option_tags = soup.find_all('option')
    groups = {tag.text: tag.get('value') for tag in option_tags}
    return groups

# Удаляет из строки все символы кроме латиницы, цифр или нижнего подчёркивания и преобразует в нижний регистр
# Принимает и возвращает строку
def clean_string(text):
    return sub(r'\W', '', text).lower()

# Получает строковое наименование группы, возвращает строковый ид группы
# Возвращает None, если такой группы нет
def get_group_id(group_name):
    groups = get_groups()
    groups = {clean_string(k): groups[k] for k in groups}
    group_name = clean_string(group_name)   
    return groups.get(group_name)

# Получает строковое наименование группы
# Возвращает правильно написанное строковое наименование группы
# Возвращает None, если такой группы нет
def validate_group_name(group_name):
    response = requests.get(URL + '/menu.php?tmenu=12&cod=0')
    soup = BeautifulSoup(response.text, 'html.parser')
    option_tags = soup.find_all('option')
    for tag in option_tags:
        if clean_string(tag.text) == clean_string(group_name):
            return tag.text
    return None

# Получает нужную дату и номер группы (строка)
# Возвращает результат HTTP запроса с сайта вуза
def get_schedule_response(date, group_id):
    full_url = URL + '/rasp.php'
    date = date.strftime("%d.%m.%Y")
    response = requests.post(full_url, data = {
            'rtype': 1, 
            'group' : group_id,
            'datafrom' : date,
            'dataend' : date}
        )
    return response

# Принимает строку типа предмета, возвращает более читаемую строку
def type_beautifier(subject_type):
    subject_type = subject_type.replace('-Экз', '❗️ ЭКЗАМЕН ❗️')
    subject_type = subject_type.replace('-Конс', '(Консультация)')
    subject_type = subject_type.replace('-ДифЗ', '❗️ ДИФ ЗАЧЕТ ❗️')
    subject_type = subject_type.replace('-Зач', '❗️ ЗАЧЕТ ❗️')
    subject_type = subject_type.replace('-Собр', '(Собрание)')
    subject_type = subject_type.replace('-Лекц', '(Лекция)')
    subject_type = subject_type.replace('-Прак', '(Практика)')
    return subject_type

# Принимает строку, преобразовывает и возвращает объект Subject
def get_subject(text): 
    subject = Subject()

    subject_data = text.split(', ')

    # Окно между занятиями
    if subject_data[0] == u'\xa0':
        subject.lesson_break = True
    else:
        # Тип предмета начинается с "-", до этого название
        tmp = subject_data.pop(0)
        type_idx = tmp.rfind('-')
        subject_name = tmp[:type_idx]
        subject_type = tmp[type_idx:]

        subject.name = subject_name
        subject.type = type_beautifier(subject_type) # make pretty
        subject.teacher = subject_data.pop(0)
        subject.classroom = subject_data.pop(0)
        
        # Вся остальная информация хранитя в additional_info
        additional_info = ' '.join(subject_data)
        # Поиск ссылки на онлайн занятие
        link_match = search(r'ОНЛАЙН! \n\S+', additional_info)
        # Если ссылка существует, то ее нужно перенести из строки additional_info в link
        if link_match:
            link = link_match.group()
            additional_info = additional_info.replace(link, '')
            subject.link = link.replace('ОНЛАЙН! \n', '')

        subject.additional_info = additional_info
        
    return subject

# Принимает строку, преобразовывает и вовзращает список предметов на одну пару
def get_subjects(text):
    subjects = []

    # Во время пары может быть несколько занятий (у разных подгрупп)
    # Они раздеяются '--------'
    for subject_text in text.split('--------'):
        subjects.append(str(get_subject(subject_text)))
    
    return subjects

# HTML-response to list of Lesson objects
def get_lessons(response):
    soup = BeautifulSoup(response.text, 'html.parser')

    # Список с текстовым временем
    time = [tag.get_text() for tag in soup.select('td > b')]
    time = time[2:]
    
    lesson_tags = soup.select("td[style='border-color: Black;']")[1:]

    lesson_count = len(time)
    lessons = []

    for num in range(lesson_count):
        tag = lesson_tags[num]
        text = tag.get_text()

        # Преобразование элемента ссылка в текст
        link_tag = tag.find("a")
        if link_tag:
            text = text.replace(link_tag.string, link_tag.get("href", 1)) 

        lesson = Lesson(time[num])
        lesson.subjects = get_subjects(text)
        lessons.append(str(lesson))

    return lessons
 
def get_schedule(dt, group):
    group_id = get_group_id(group) 
    schedule = Schedule(dt, group) 

    if group_id:
        response = get_schedule_response(dt, group_id)
        if response.status_code == 200:
            if response.text  == '<h3>Информации для отображения отчета не обнаружено! Измените период.</h3>':
                schedule.lessons = ['Нет занятий. Отдыхай :з']
            else:
                schedule.lessons = get_lessons(response)
        else:
            schedule.lessons = ['Не удалось получить информацию. Попробуй позже']
    else:
            schedule.lessons = ['Не знаю такой группы! Попробуй изменить в нсатройках']

    return schedule