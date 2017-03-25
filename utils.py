# -*- coding: utf-8 -*-
from telebot import types
import os

markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
markup.row("Ученик")
markup.row("Администратор")

markup_for_admin = types.ReplyKeyboardMarkup(one_time_keyboard=True)
markup_for_admin.row("Добавить расписание на день")
markup_for_admin.row("Добавить ачивку")
markup_for_admin.row("Отправить срочное сообщение")
markup_for_admin.row("Изменить пароль")

markup_for_learner = types.ReplyKeyboardMarkup(one_time_keyboard=True)
markup_for_learner.row("Список моих ачивок", "Где я живу?")
markup_for_learner.row("Расписание на день", "Начать квест")
markup_for_learner.row("Информация о текущем событии")
markup_for_learner.row("Номера телефонов вожатых и преподователей")

markup_for_quest = types.ReplyKeyboardMarkup(one_time_keyboard=True)
markup_for_quest.row("Закончить квест")

def get_password_hash():
    file = open('pass.txt', 'r')
    hash = file.readline()
    file.close()
    return hash

def set_password_hash(new_pass):
    os.remove("pass.txt")
    file = open('pass.txt', 'w')
    file.write(str(new_pass))
    file.close()

def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False