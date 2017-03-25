# -*- coding: utf-8 -*-
import config
import telebot
import random
import hashlib
import utils
import datetime
import codecs
from telebot import types
from SQLiteHelper import SQLightHelperForUsers
from SQLiteHelper import SQLightHelperForAchievements
from SQLiteHelper import SQLightHelperForSchedule

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def change_password(message):
    bot.send_message(message.chat.id, "Выберите режим: ", reply_markup=utils.markup)


@bot.message_handler(func=lambda message: message.text == "Изменить пароль")
def change_password(message):
    msg = bot.reply_to(message, 'Введите новый пароль: ')
    bot.register_next_step_handler(msg, change_admin_password)


@bot.message_handler(func=lambda message: message.text == "Администратор")
def admin(message):
    msg = bot.reply_to(message, 'Введите пароль: ')
    types.ReplyKeyboardRemove()
    bot.register_next_step_handler(msg, password_checker)


@bot.message_handler(func=lambda message: message.text == "Ученик")
def learner(message):
    db_helper = SQLightHelperForUsers(config.db_name)
    db_helper.add_new_user(message.from_user.id, message.chat.id, message.from_user.first_name,
                           message.from_user.last_name, 0)
    types.ReplyKeyboardRemove()
    name_of_user = message.from_user.first_name
    bot.send_message(message.chat.id,
                     'Привет, {name}. Рад тебя видеть. Я бот весенней школы GoTo.'.format(name=name_of_user),
                     reply_markup=utils.markup_for_learner)


#@bot.message_handler(func=lambda message: message.text == "Назад")
#def back(message):
#    bot.send_message(message.chat.id, 'Вы вышли из режима квеста', reply_markup=utils.markup_for_learner)


@bot.message_handler(func=lambda message: message.text == "Информация о текущем событии")
def current_event(message):
    db_helper = SQLightHelperForSchedule(config.db_name)
    current_hour = datetime.datetime.now().hour
    current_minute = datetime.datetime.now().minute
    event = db_helper.current_event(current_hour * 60 + current_minute)
    if event is None:
        bot.send_message(message.chat.id, 'В данное время ничего не происходит')
    else:
        bot.send_message(message.chat.id, 'В данное время проходит {event}, место проведения: {place}'.
                         format(event=event[0], place=event[1]))


#@bot.message_handler(func=lambda message: message.text == "Начать квест")
#def quest(message):
#    msg = bot.reply_to(message, 'Введите логин')
#    bot.register_next_step_handler(msg, begin_quest)


@bot.message_handler(func=lambda message: message.text == "Расписание на день")
def send_schedule(message):
    db_helper = SQLightHelperForSchedule(config.db_name)
    schedule = db_helper.get_schedule()
    if len(schedule) == 0:
        bot.send_message(message.chat.id, 'Пока нет расписания. ')
    else:
        list = 'Расписание на сегодня: \n'
        for row in schedule:
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
        bot.send_message(message.chat.id, list)


@bot.message_handler(func=lambda message: message.text == "Отправить срочное сообщение")
def send_message(message):
    msg = bot.reply_to(message, 'Введите срочное сообщение: ')
    bot.register_next_step_handler(msg, write_message)


@bot.message_handler(func=lambda message: message.text == "Добавить ачивку")
def achievement(message):
    msg = bot.reply_to(message, 'Введите Имя Фамилию и Ачивку: ')
    bot.register_next_step_handler(msg, send_new_achievement)


@bot.message_handler(func=lambda message: message.text == "Добавить расписание на день")
def add_schedule(message):
    msg = bot.reply_to(message, 'Текущее расписание удалено. Формат: \n'
                                'ЧЧ:ММ(начало) ЧЧ:ММ(конец) событие, место\n'
                                'Если закончили вводить расписание, то напишите всё.')
    db_helper = SQLightHelperForSchedule(config.db_name)

    db_helper.delete_schedule()
    bot.register_next_step_handler(msg, add_new_schedule)


@bot.message_handler(func=lambda message: message.text == "Список моих ачивок")
def my_achievements(message):
    db_helper_for_users = SQLightHelperForUsers(config.db_name)
    db_helper_for_achiev = SQLightHelperForAchievements(config.db_name)
    achievements = db_helper_for_achiev.achievements(db_helper_for_users.user_names(message.from_user.id)[0],
                                                     db_helper_for_users.user_names(message.from_user.id)[1])
    list_of_achiev = 'Количество ачивок: {n} \n'.format(n=len(achievements))
    for row in achievements:
        list_of_achiev += '-> ' + row[0] + '\n'
    if len(achievements) == 0:
        bot.send_message(message.chat.id, 'У вас нет ачивок')
    else:
        bot.send_message(message.chat.id, list_of_achiev)


@bot.message_handler(func=lambda message: message.text == "Где я живу?")
def living_room(message):
    file = codecs.open('room_allocation.txt', 'r', 'utf-8')
    msg = 'Вас нет в базе данных'
    for line in file.readlines():
        info = line.split(' ')
        address = info[3] + ' корпус ' + info[4] + ' комната'
        if info[2] == message.from_user.username:
            msg = address
            break
        elif info[0] == message.from_user.first_name and info[1] == message.from_user.last_name:
            msg = address
            break
    file.close()
    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda message: message.text == "Номера телефонов вожатых и преподователей")
def info(message):
    file = codecs.open('info.txt', 'r', 'utf-8')
    all_lines = ''
    for line in file.readlines():
        all_lines += line
    file.close()
    bot.send_message(message.chat.id, all_lines)


@bot.message_handler(commands=['help'])
def my_achievements(message):
    bot.send_message(message.chat.id, 'Нажмите 👉 /start для того, чтобы начать работу с ботом')


#def begin_quest(message):
#    db_helper = SQLightHelperForQuestions(config.db_name)
#    db_helper.delete_all(message.text)
#    array = []
#    with open('questions_for_quests.txt', 'r') as file:
#        line_1 = file.readline()
#        line_2 = file.readline()
#        line_3 = file.readline()
#        array.append([])
#        array[len(array) - 1].append(line_1)
#        array[len(array) - 1].append(line_2)
#        array[len(array) - 1].append(line_3)
#    random.shuffle(array)
#    for i in range(0, len(array) - 1):
#        answers = array[i][1].split('&')
#        db_helper.add_new_row(message.text, array[i][0], answers[0], answers[1], answers[3], array[i][2])
#    arr = db_helper.get_one_question(message.text)
#    bot.send_message(message.chat.id, arr[2] + '\n' + arr[3] + '\n' + arr[4] + '\n' + arr[5],
#                     reply_markup=utils.markup_for_quest)
#    bot.register_next_step_handler(message, continue_quest(message.text))


#def continue_quest(message, login):
#    db_helper = SQLightHelperForQuestions(config.db_name)
#    arr = db_helper.get_one_question(login)
#    login = arr[0][1]
#    question = arr[0][2]
#    if arr is None:
#        bot.send_message(message, 'Поздравляю, вы ответили на все вопросы правильно.')
#    elif message.text != arr[0][6]:
#        msg = bot.reply_to(message, 'Неправильный ответ. Попробуте ещё раз.')
#        bot.register_next_step_handler(msg, continue_quest)
#    elif message.text == arr[0][6]:
#        bot.send_message(message.chat.id, 'Ответ правильный. Следующий вопрос: ')
#        db_helper.delete_row(login, question)
#        arr = db_helper.get_one_question(login)
#        bot.send_message(message.chat.id, arr[0][2] + '\n' + arr[0][3] + '\n' + arr[0][4] + '\n' + arr[0][5])
#        bot.register_next_step_handler(message, continue_quest(login))

def add_new_schedule(message):
    array = message.text.split(' ')
    hour_1 = message.text[0:2]
    minute_1 = message.text[3:5]
    hour_2 = message.text[6:8]
    minute_2 = message.text[9:11]
    event = message.text[12:message.text.find(',')]
    place = message.text[message.text.find(',') + 1: len(message.text)]
    if 'всё' in message.text.lower():
        bot.send_message(message.chat.id, 'Расписание успешно обновлено')
    elif len(array) < 3 or len(message.text) < 13 or message.text[2] != ':' or message.text[8] != ':' \
            or not utils.representsInt(hour_1) or not utils.representsInt(minute_1) or not utils.representsInt(hour_2) \
            or not utils.representsInt(minute_2) or message.text.find(',') == -1:
        msg = bot.reply_to(message, 'Неправильный формат. Формат: \n'
                                    'ЧЧ:ММ(начало) ЧЧ:ММ(конец) событие, место\n'
                                    'Если закончили вводить расписание, то напишите всё.')
        bot.register_next_step_handler(msg, add_new_schedule)
    else:
        db_helper = SQLightHelperForSchedule(config.db_name)
        db_helper.add_new_row(int(hour_1) * 60 + int(minute_1), int(hour_2) * 60 + int(minute_2), event, place)
        msg = bot.reply_to(message, 'Событие добавлено успешно. Продолжайте вводить события или напишите всё.')
        bot.register_next_step_handler(msg, add_new_schedule)


def get_hash(password):
    h = hashlib.md5()
    h.update(password.encode())
    return h.hexdigest()


def change_admin_password(new_password):
    utils.set_password_hash(get_hash(new_password.text))
    bot.send_message(new_password.chat.id, 'Пароль успешно изменён.')


def send_urgent_message(message):
    db_helper = SQLightHelperForUsers(config.db_name)
    all_users = db_helper.select_all_users()
    for row in all_users:
        if row[1] != message.chat.id:
            bot.send_message(row[1], message.text)
    bot.reply_to(message, 'Сообщение успешно отправлено')


def write_message(message):
    db_helper = SQLightHelperForUsers(config.db_name)
    if db_helper.status_of_user(message.from_user.id) == 'User is admin':
        send_urgent_message(message)
    else:
        bot.send_message(message.chat.id, 'У вас недостаточно прав для этого.')


def send_new_achievement(message):
    temp = message.text.split(' ')
    if (len(temp) < 3):
        msg = bot.reply_to(message, 'Неправильный формат. Попробутйе ввести ещй раз Имя Фамилию и Ачивку: ')
        bot.register_next_step_handler(msg, send_new_achievement)
    db_helper = SQLightHelperForAchievements(config.db_name)
    achievement = temp[2]
    for i in range(3, len(temp)):
        achievement += ' ' + temp[i]
    db_helper.add_new_achievement(temp[0], temp[1], achievement)
    message.text = '{name} {surname} получил достижение: {achievement}'.format(name=temp[0],
                                                                               surname=temp[1], achievement=achievement)
    send_urgent_message(message)


def password_checker(message):
    if utils.get_password_hash() == get_hash(message.text):
        db_helper = SQLightHelperForUsers(config.db_name)
        if db_helper.status_of_user(message.from_user.id) == 'User is learner':
            db_helper.update_user_info(message.user.id, 1)
        elif db_helper.status_of_user(message.from_user.id) == 'No user found':
            db_helper.add_new_user(message.from_user.id, message.chat.id, message.from_user.first_name,
                                   message.from_user.last_name, 1)
        name_of_user = message.from_user.first_name
        bot.send_message(message.chat.id,
                         'Привет, {name}. Ты вошёл в режим администратора. Рад тебя видеть. '
                         'Я бот весенней школы GoTo.'.format(name=name_of_user), reply_markup=utils.markup_for_admin)
    elif message.text != 'Ученик':
        msg = bot.reply_to(message, 'Попробуйте ввести ещё раз или выберите режим ученика: ')
        bot.register_next_step_handler(msg, password_checker)


bot.polling()