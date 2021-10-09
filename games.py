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
    username = data['from']['username']
    count = msql.get_count(username)
    if msql.kosti_set_price(username, set) == True:
        price_1 = int(count) / 5
        price_2 = int(count) / 10
        price_3 = int(count) / 15
        price_4 = int(count) / 20
        price_5 = int(count) / 25
        price_6 = int(count) / 30
        price_7 = int(count) / 35
        price_8 = int(count) / 40
        price_9 = int(count) / 45
        price_10 = int(count) / 50
        markup = telebot.types.InlineKeyboardMarkup()
        button_1 = telebot.types.InlineKeyboardButton(text=str(int(price_1)) + '$', callback_data=str(int(price_1))+'_contra')
        button_2 = telebot.types.InlineKeyboardButton(text=str(int(price_2)) + '$', callback_data=str(int(price_2))+'_contra')
        button_3 = telebot.types.InlineKeyboardButton(text=str(int(price_3)) + '$', callback_data=str(int(price_3))+'_contra')
        button_4 = telebot.types.InlineKeyboardButton(text=str(int(price_4)) + '$', callback_data=str(int(price_4))+'_contra')
        button_5 = telebot.types.InlineKeyboardButton(text=str(int(price_5)) + '$', callback_data=str(int(price_5))+'_contra')
        button_6 = telebot.types.InlineKeyboardButton(text=str(int(price_6)) + '$', callback_data=str(int(price_6))+'_contra')
        button_7 = telebot.types.InlineKeyboardButton(text=str(int(price_7)) + '$', callback_data=str(int(price_7))+'_contra')
        button_8 = telebot.types.InlineKeyboardButton(text=str(int(price_8)) + '$', callback_data=str(int(price_8))+'_contra')
        button_9 = telebot.types.InlineKeyboardButton(text=str(int(price_9)) + '$', callback_data=str(int(price_9))+'_contra')
        button_10 = telebot.types.InlineKeyboardButton(text=str(int(price_10)) + '$', callback_data=str(int(price_10))+'_contra')
        markup.add(button_1, button_2, button_3, button_4, button_5, button_6, button_7, button_8, button_9, button_10)
        return markup

def mines_start(data):
    nickname = data['from']['username']
    mines_list = add_mines_in_bd(data)
    list1 = [
        telebot.types.InlineKeyboardButton(text='❔', callback_data='mine_game|1-1' + '|' + nickname + '|' + mines_list + '|' + '0'),
        telebot.types.InlineKeyboardButton(text='❔', callback_data='mine_game|1-2' + '|' + nickname + '|' + mines_list + '|' + '0'),
        telebot.types.InlineKeyboardButton(text='❔', callback_data='mine_game|1-3' + '|' + nickname + '|' + mines_list + '|' + '0')
    ]
    list2 = [
        telebot.types.InlineKeyboardButton(text='❔', callback_data='mine_game|2-1' + '|' + nickname + '|' + mines_list + '|' + '0'),
        telebot.types.InlineKeyboardButton(text='❔', callback_data='mine_game|2-2' + '|' + nickname + '|' + mines_list + '|' + '0'),
        telebot.types.InlineKeyboardButton(text='❔', callback_data='mine_game|2-3' + '|' + nickname + '|' + mines_list + '|' + '0')
    ]
    list3 = [
        telebot.types.InlineKeyboardButton(text='❔', callback_data='mine_game|3-1' + '|' + nickname + '|' + mines_list + '|' + '0'),
        telebot.types.InlineKeyboardButton(text='❔', callback_data='mine_game|3-2' + '|' + nickname + '|' + mines_list + '|' + '0'),
        telebot.types.InlineKeyboardButton(text='❔', callback_data='mine_game|3-3' + '|' + nickname + '|' + mines_list + '|' + '0')
    ]
    markup = telebot.types.InlineKeyboardMarkup(keyboard=(list1, list2, list3))
    return(markup)

def add_mines_in_bd(data):
    nickname = data['from']['username']
    list = ['1-1', '1-2', '1-3', '2-1', '2-2', '2-3', '3-1', '3-2', '3-3']
    random.shuffle(list)
    mines_list = list[0] + '!' + list[1] + '!' + list[2]
    print(nickname + ' - ' + mines_list)
    return mines_list


#print(mines_list.split('!'))