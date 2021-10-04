from random import randint, random
import telebot
import msql
from settings import api_token
import text
import games
import random

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('Вас приветствует Musya Bot')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
print('\nДанный бот создан с развлекательной целью\nи не может быть распространяться на платной основе\n\n')
print('Токен авторизации: ' + api_token)

tbot = telebot.TeleBot(api_token)

@tbot.message_handler(content_types='text')
def get_text(message):
    message = message.json
    answer = sort_start(message)
    print(message['from']['username'] + ' - ' + message['text'])

@tbot.callback_query_handler(func=lambda call: True)
def callback(call):
    key = call.data
    if key == 'kosti_from_menu':
        kosti_games(call)
    elif key == 'kosti_1':
        kosti_games_part2(call, key)
    elif key == 'kosti_2':
        kosti_games_part2(call, key)
    elif key == 'kosti_3':
        kosti_games_part2(call, key)
    elif key == 'kosti_4':
        kosti_games_part2(call, key)
    elif key == 'kosti_5':
        kosti_games_part2(call, key)
    elif key == 'kosti_6':
        kosti_games_part2(call, key)
    elif 'contra' in key:
        kosti_games_part3(call, key)


def sort_start(data):
    message_text = data['text']
    if message_text == '/start':
        cmd_start(data)
    elif message_text == '/menu':
        cmd_menu(data)
    elif message_text == '/games':
        cmd_games(data)

def cmd_start(data):
    if msql.cmd_start(data) == True:
        chat_id = data['from']['id']
        text_message = text.hello_text()
        send_message(chat_id, text_message)

def cmd_menu(data):
    nickname = data['from']['username']
    count = msql.get_count(nickname)
    chat_id = data['from']['id']
    text_message = f"""
        Привет, @{nickname}.

        Баланс - {count}$ 

        /games
    """
    send_message(chat_id, text_message)
    
def cmd_games(data):
    text_message = """
    Список игр, которые я смог сделать\n\n
    """
    markup = telebot.types.InlineKeyboardMarkup()
    button_1 = telebot.types.InlineKeyboardButton(text='Кости', callback_data='kosti_from_menu')
    markup.add(button_1)
    tbot.send_message(chat_id=data['from']['id'], text=text_message, reply_markup=markup)

def kosti_games(call):
    data = call.message.json
    text_message = 'Выбери число, на которое хочешь поставить:\n\n*нажми 1 раз и жди*'
    markup = games.kosti_gen6keys()
    tbot.send_message(data['chat']['id'], text_message, reply_markup=markup)

def kosti_games_part2(call, key):
    data = call.message.json
    if key == 'kosti_1':
        answer = games.kosti_set_price(data, '1')
    elif key == 'kosti_2':
        answer = games.kosti_set_price(data, '2')
    elif key == 'kosti_3':
        answer = games.kosti_set_price(data, '3')
    elif key == 'kosti_4':
        answer = games.kosti_set_price(data, '4')
    elif key == 'kosti_5':
        answer = games.kosti_set_price(data, '5')
    elif key == 'kosti_6':
        answer = games.kosti_set_price(data, '6')
    text_message = 'Сейчас выбери ставку из предложенных:\n\n*нажми 1 раз и жди*'
    #tbot.send_message(data['chat']['id'], text_message, reply_markup=answer)
    tbot.edit_message_text(text=text_message, message_id=data['message_id'], reply_markup=answer, chat_id=data['chat']['id'])

def kosti_games_part3(call, key):
    data = call.message.json
    price = int(key.replace('_contra', ''))
    stavka = int(msql.get_kosti_set(data['chat']['username']))
    winner = random.randint(1, 6)
    old_count = int(msql.get_count(data['chat']['username']))
    markup = telebot.types.InlineKeyboardMarkup()
    button_1 = telebot.types.InlineKeyboardButton(text='ХОЧУ ЕЩЕ!', callback_data='kosti_from_menu')
    markup.add(button_1)
    if stavka == winner:
        new_count = old_count + price * 8
        price_1 = price * 8
        if msql.set_new_count(data['chat']['username'], new_count) == True:
            text_message = f"""
            Поздравлю тебя, друг.\n
            Ты выйграл {price_1} денег

            Твой новый баланс: {new_count}$

            главное меню - /menu
            """
            tbot.edit_message_text(chat_id=data['chat']['id'], text=text_message, message_id=data['message_id'], reply_markup=markup)
    else:
        new_count = old_count - price
        if msql.set_new_count(data['chat']['username'], new_count) == True:
            text_message = f"""
            К сожалению, ты продул...\n
            Выпало {winner}, а ты поставил на {stavka}
            Ты проиграл {price} денег

            Твой новый баланс: {new_count}$

            главное меню - /menu
            """
            tbot.edit_message_text(chat_id=data['chat']['id'], text=text_message, message_id=data['message_id'], reply_markup=markup)


    

def send_message(chat_id, text_message):
    tbot.send_message(chat_id, text_message)

try:
    tbot.infinity_polling()
except Exception:
    print('reload')