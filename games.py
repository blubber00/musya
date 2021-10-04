import telebot
from telebot.types import InlineKeyboardButton
import msql
import random


def kosti_gen6keys():
    markup = telebot.types.InlineKeyboardMarkup()
    button_1 = telebot.types.InlineKeyboardButton(text='1', callback_data='kosti_1')
    button_2 = telebot.types.InlineKeyboardButton(text='2', callback_data='kosti_2')
    button_3 = telebot.types.InlineKeyboardButton(text='3', callback_data='kosti_3')
    button_4 = telebot.types.InlineKeyboardButton(text='4', callback_data='kosti_4')
    button_5 = telebot.types.InlineKeyboardButton(text='5', callback_data='kosti_5')
    button_6 = telebot.types.InlineKeyboardButton(text='6', callback_data='kosti_6')
    markup.add(button_1, button_2, button_3, button_4, button_5, button_6)
    return markup

def kosti_set_price(data, set):
    username = data['chat']['username']
    count = msql.get_count(username)
    if msql.kosti_set_price(username, set) == True:
        price_1 = int(count) / 10
        price_2 = int(count) / 5
        price_3 = int(count) / 2
        markup = telebot.types.InlineKeyboardMarkup()
        button_1 = telebot.types.InlineKeyboardButton(text=str(int(price_1)), callback_data=str(int(price_1))+'_contra')
        button_2 = telebot.types.InlineKeyboardButton(text=str(int(price_2)), callback_data=str(int(price_2))+'_contra')
        button_3 = telebot.types.InlineKeyboardButton(text=str(int(price_3)), callback_data=str(int(price_3))+'_contra')
        markup.add(button_1, button_2, button_3)
        return markup

def mines_start(data):
    list1 = [
        telebot.types.InlineKeyboardButton(text='❔', callback_data='miness1-1'),
        telebot.types.InlineKeyboardButton(text='❔', callback_data='miness1-2'),
        telebot.types.InlineKeyboardButton(text='❔', callback_data='miness1-3')
    ]
    list2 = [
        telebot.types.InlineKeyboardButton(text='❔', callback_data='miness2-1'),
        telebot.types.InlineKeyboardButton(text='❔', callback_data='miness2-2'),
        telebot.types.InlineKeyboardButton(text='❔', callback_data='miness2-3')
    ]
    list3 = [
        telebot.types.InlineKeyboardButton(text='❔', callback_data='miness3-1'),
        telebot.types.InlineKeyboardButton(text='❔', callback_data='miness3-2'),
        telebot.types.InlineKeyboardButton(text='❔', callback_data='miness3-3')
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard=(list1, list2, list3))
    if add_mines_in_bd(data) == True:
        return(markup)

def add_mines_in_bd(data):
    nickname = data['chat']['username']
    list = ['1-1', '1-2', '1-3', '2-1', '2-2', '2-3', '3-1', '3-2', '3-3']
    random.shuffle(list)
    mines_list = list[0] + '!' + list[1] + '!' + list[2]
    if msql.set_new_mines(nickname, mines_list) == True:
        return True




#print(mines_list.split('!'))