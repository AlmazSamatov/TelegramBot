import datetime
import schedule
import time
import config
import os
from SQLiteHelper import SQLightHelperForSchedule, SQLightHelperForUsers
import telebot

bot = telebot.TeleBot(config.token)


def send_schedule_to_everyone():
    db_helper = SQLightHelperForSchedule(config.db_name)
    schedule_of_day = db_helper.get_schedule()
    set_next()
    if len(schedule_of_day) != 0:
        list = 'Расписание на сегодня: \n'
        for row in schedule_of_day:
            start_hours = str(row[0] // 60)
            start_minutes = str(row[0] % 60)
            end_hours = str(row[1] // 60)
            end_minutes = str(row[1] % 60)
            if len(start_minutes) == 1:
                start_minutes = '0' + start_minutes
            if len(end_minutes) == 1:
                end_minutes = '0' + end_minutes
            list += start_hours + ':' + start_minutes + ' - ' + end_hours + ':' + end_minutes \
                    + ' ' + row[2] + ',' + row[3] + '\n'
        send_message_to_all_users(list)


def send_message_to_all_users(text):
    db_helper = SQLightHelperForUsers(config.db_name)
    all_users = db_helper.select_all_users()
    for row in all_users:
        bot.send_message(row[1], text)


def send_notifier():
    next_event = get_next_event()
    event_name = next_event[0]
    event_place = next_event[1]
    send_message_to_all_users('Сейчас идёт {event}, место проведения: '
                              '{place}'.format(event=event_name, place=event_place))
    set_next()
    return schedule.CancelJob


def set_next():
    db_helper = SQLightHelperForSchedule(config.db_name)
    next_event = db_helper.next_event(datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
    if next_event is not None:
        event_time = next_event[0]
        hours = str(event_time // 60)
        minutes = str(event_time % 60)
        if len(hours) == 1:
            hours = '0' + hours
        if len(minutes) == 1:
            minutes = '0' + minutes
        next_event_name = next_event[1]
        next_event_place = next_event[2]
        os.remove('next_event.txt')
        file = open('next_event.txt', 'w')
        file.write(next_event_name + '&' + next_event_place)
        file.close()
        schedule.every().day.at(hours + ':' + minutes).do(send_notifier).tag('daily-tasks')


def get_next_event():
    file = open('next_event.txt', 'r')
    line = file.readline().split('&')
    file.close()
    return line


schedule.every().day.at("08:00").do(send_schedule_to_everyone)

while True:
    schedule.run_pending()
    time.sleep(1)