import time
import datetime
import requests
import config
import telebot
from bs4 import BeautifulSoup
from typing import Optional


bot = telebot.TeleBot(config.BOT['access_token'])
week_l = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday']
week_d = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']


@bot.message_handler(commands=['help'])
def answer_help(message):
    resp = """<b>Комманды бота:</b>
        1) /(День недели)_(Неделя)_(Номер группы) - вывод расписания для группы в указанный день
        2) /near_(Номер группы) - вывод ближайшего расписания для группы
        3) /tomorrow_(Номер группы) - вывод расписания для группы на завтра
        4) /all_(Неделя)_(Номер группы) - вывод всего расписания для группы """
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


def get_page(group, week='') -> str:
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.BOT['domain'],
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на день недели
    if day in week_l:
        day_number = str(week_l.index(day) + 1) + "day"
    else:
        day_number = "1day"
    schedule_table = soup.find("table", attrs={"id": day_number})
    if not schedule_table:
        return

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text + ", " + room.dd.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_day(message):
    """ Получить расписание на указанный день """
    try:
        day, week, group = message.text.split()
    except:
        bot.send_message(message.chat.id, "ЧАВО? НЕ ПОНЯЛ. ПОВТОРИ")
        return None
    web_page = get_page(group, week)
    schedule = parse_schedule(web_page, day)
    if not schedule:
        bot.send_message(message.chat.id, "ЧАВО? НЕ ПОНЯЛ? ПОВТОРИ?(ВОЗМОЖНО, ЧТО ЗАВТРА ОТДЫХ")
        return None
    times_lst, locations_lst, lessons_lst =  schedule
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    try:
        _, group = message.text.split()
    except:
        bot.send_message(message.chat.id, "ЧАВО? НЕ ПОНЯЛ. ПОВТОРИ")
        return None
    today = datetime.datetime.now().weekday()
    if today != 6:
        today = week_l[today]
    else:
        bot.send_message(message.chat.id, 'СЕГОДНЯ ОТДЫХ, ДРУЖИЩЕ')
    while True:
        count = 0
        if int(datetime.datetime.today().strftime('%U')) % 2 == 1:
            week = '1'
        else:
            week = '2'
        web_page = get_page(group, week)
        schedule = parse_schedule(web_page, today)
        if not schedule:
            if today != '/saturday':
                today = week_list[week_list.index(today) + 1]
            else:
                today = '/monday'
            count += 1
        else:
            break
    times_lst, locations_lst, lessons_lst = schedule
    cnt = 0
    state = 0
    for i in times_lst:
        try:
            _, time = i.split('-')
        except:
            bot.send_message(message.chat.id, 'ЦК')
            return
        t1, t2 = time.split(':')
        time = int(t1 + t2)
        cur_time = int(str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute))
        if cur_time < time:
            resp = '<b>БЛИЖАЙШАЯ ПАРА, ДРУЖИЩЕ, В ' + week_d[week_l.index(today)] + ':</b>\n'
            resp += '<b>{}</b>, {}, {}\n'.format(times_lst[cnt], locations_lst[cnt], lessons_lst[cnt])
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
            state = 1
            break
        cnt += 1
    if not state:
        while True:
            today = datetime.datetime.now() + datetime.timedelta(days=count)
            tomorrow = today
            if today.weekday() == 5:
                tomorrow += datetime.timedelta(days=2)
            else:
                tomorrow += datetime.timedelta(days=1)
            tomorrow = week_l[tomorrow.weekday()]
            schedule = parse_schedule(web_page, tomorrow)
            if not schedule:
                count += 1
                continue
            times_lst, locations_lst, lessons_lst = schedule
            resp = '<b>{}</b>, {}, {}\n'.format(times_lst[0], locations_lst[0], lessons_lst[0])
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
            break


@bot.message_handler(commands=['tomorrow'])
def get_tomorrow(message):
    """ Получить расписание на следующий день """
    try:
        _, group = message.text.split()
    except:
        bot.send_message(message.chat.id, "ЧАВО? НЕ ПОНЯЛ. ПОВТОРИ")
        return None
    _, group = message.text.split()
    if int(datetime.datetime.today().strftime('%U')) % 2 == 1:
        week = 1
    else:
        week = 2
    web_page = get_page(group, str(week))
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    if tomorrow.weekday() == 7:
        tomorrow = tomorrow + datetime.timedelta(days=1)
    tomorrow = week_l[tomorrow.weekday()]
    schedule = parse_schedule(web_page, tomorrow)
    if not schedule:
        bot.send_message(message.chat.id, "ЧАВО? НЕ ПОНЯЛ. ПОВТОРИ(ВОЗМОЖНО, ЧТО ЗАВТРА ОТДЫХ")
        return None
    times_lst, locations_lst, lessons_lst = schedule
    resp = '<b>Расписание на завтра для ' + group + ':\n\n</b>'
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    try:
        _, week, group = message.text.split()
    except:
        bot.send_message(message.chat.id, "ЧАВО? НЕ ПОНЯЛ. ПОВТОРИ")
        return None
    web_page = get_page(group, week)
    if int(week) == 1:
        resp = '<b>Расписание для ' + str(group) + ' на четную неделю:</b>\n\n'
    elif int(week) == 2:
        resp = '<b>Расписание для ' + str(group) + ' на нечетную неделю:</b>\n\n'
    else:
        resp = '<b>ЛОВИ РАСПИСАНИЕ НА ВСЮ НЕДЕЛЮ, ДРУЖИЩЕ ' + str(group) + ':</b>\n\n'
    for day in week_l:
        resp += '<b>' + week_d[week_l.index(day)] + '</b>' + ':\n'
        schedule = parse_schedule(web_page, day)
        if not schedule:
            continue
        times_lst, locations_lst, lessons_lst = schedule
        for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
        resp += '\n'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
