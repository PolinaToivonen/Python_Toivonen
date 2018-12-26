import requests
import config
import telebot
from bs4 import BeautifulSoup
import datetime as dt
from datetime import *

bot = telebot.TeleBot(config.access_token)

days = ['', '/monday', '/teusday', '/wednesday', '/thursday', '/friday', '/saturday', '/sunday']

def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_day(web_page, number_day):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на день
    schedule_table = soup.find("table", attrs={"id": str(number_day) + 'day'})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list

def current_week():
    cur_week = datetime.date.today().isocalendar()[1]
    if cur_week % 2 == 1:
        week = 2
    else:
        week = 1
    return week


@bot.message_handler(commands=['monday'])
def get_monday(message):
    """ Получить расписание на понедельник """
    _, group = message.text.split()
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_day(web_page, 1)
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    day, group = message.text.split()
    web_page = get_page(group)
    days = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday', '/sunday']
    day_number = str(int(days.index(day)) + 1)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule(web_page, day_number)
    resp = ' Лови расписание, дружище '
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')

@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    _, group = message.text.split()
    date_now = str(date.today().isoweekday())
    day_number = date_now + 'day'
    web_page = get_page(group, current_week())
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_day(web_page, day_number)
    now = datetime.datetime.now()
    now = datetime.strptime(now.strftime("%H:%M"), "%H:%M")
    resp = 'Лови своё ближайшие расписание, студентик'

    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        if datetime.strptime(time.split('-')[0], "%H:%M") > now:
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    else:
        if date.today().isoweekday() == 7:
            cur_week = datetime.date.today().isocalendar()[1]
    if cur_week % 2 == 1:
        week = 1
    else:
        week = 2
    day_number = '1day'
    web_page = get_page(group, week)
    times, locations, lessons = \
        parse_schedule_for_a_day(web_page, day_number)
    resp += '<b>{}</b>, {}, {}\n'.format(times[0], locations[0], lessons[0])
    else:
    date_now = str(date.today().isoweekday() + 1)
    day_number = date_now + 'day'
    web_page = get_page(group, current_week())
    times, locations, lessons = \
        parse_schedule_for_a_day(web_page, day_number)
    resp += '<b>{}</b>, {}, {}\n'.format(times[0], locations[0], lessons[0])
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    _, group = message.text.split()
    today = int(dt.datetime.today().weekday())
    if today == 6:
        week = int(dt.datetime.now().isocalendar()[1]) % 2
        today = 0
    else:
        today += 1
        week = (int(dt.datetime.now().isocalendar()[1]) + 1) % 2
    web_page = get_page(group, week)
    schedule = parse_schedule_for_a_day(web_page, today + 1)
    if schedule is None:
        resp = 'Расслабон,дружище. Отдыхай!'
    else:
        times_lst, locations_lst, rooms_lst, lessons_lst = schedule
        resp = ''
        for time, location, room, lession in zip(times_lst, locations_lst, rooms_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}, {}\n'.format(time, location, room, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    _, group = message.text.split()
    resp = ' Вот всё твоё расписание на неделю, дружище '
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    web_page = get_page(group)
    for day_number, day in enumerate(days):
        day_resp = ''
        times_lst, locations_lst, lessons_lst = \
            parse_schedule(web_page, day_number + 1)
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            day_resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        if day_resp:
            resp += '<b>{}:</b>\n\n{}'.format(day, day_resp)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
