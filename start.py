from random import randint, random
import telebot
from telebot.apihelper import send_message
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
    print(message['from']['username'] + ' - ' + message['text'])
    answer = sort_start(message)

@tbot.callback_query_handler(func=lambda call: True)
def callback(call):
    key = call.data
    if key == 'kosti_from_menu':
        kosti_games(call)
    elif 'kosti_' in key:
        kosti_games_part2(call, key)
    elif 'contra' in key:
        kosti_games_part3(call, key)

def sort_start(data):
    message_text = data['text']
    message_split = message_text.split(' ')
    if message_text == '/start':
        cmd_start(data)
    elif message_text == '/menu':
        cmd_menu(data)
    elif message_text == '/games':
        cmd_games(data)
    elif message_text == '/perevod':
        perevod_help(data)
    elif message_split[0].lower() == 'перевод':
        perevod(message_split, data)

def cmd_start(data):
    if msql.cmd_start(data) == True:
        chat_id = data['from']['id']
        text_message = text.hello_text()
        send_message(chat_id, text_message)

def cmd_menu(data):
    nickname = data['from']['username']
    count = msql.get_count(nickname)
    id = msql.get_id(nickname)
    chat_id = data['from']['id']
    text_message = f"""
        Привет, @{nickname}.
        
        ID - {id}
        Баланс - {count}$ 

        /games - тут ты можешь потерять все свои деньги
        /perevod - подробнее о системе переводов
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
    key_id = key.replace('kosti_', '')
    answer = games.kosti_set_price(data, key_id)
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

            Твой баланс: {new_count}$

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

            Твой баланс: {new_count}$

            главное меню - /menu
            """
            tbot.edit_message_text(chat_id=data['chat']['id'], text=text_message, message_id=data['message_id'], reply_markup=markup)

def perevod(message_split, data):
    name1 = data['from']['username']
    try:
        user_out = data['from']['id']
        user_to = int(message_split[1])
        count = int(message_split[2])
    except Exception as e:
        print (e)
    count_user_out = msql.get_count(data['from']['username'])
    if count > 0:
        if int(count_user_out) >= int(count):
            out_count = int(count_user_out) - int(count)
            from_id = msql.get_chat_id(user_to)
            user_out_id = msql.get_id(data['from']['username'])
            if msql.set_new_count_by_id(user_out_id, out_count) == True:
                to_count = msql.get_count_by_id(user_to)
                new_count = int(to_count) + int(count)
                if msql.set_new_count_by_id(user_to, new_count) == True:
                    send_message(chat_id=user_out, text_message=f'{count}$ были отправлены челику с ID - {user_to}')
                    send_message(chat_id=from_id, text_message=f'@{name1} перевел вам {count}$')
        else:send_message(chat_id=user_out, text_message='Возвращайся с деньгами!')

    else:
        send_message(chat_id=user_out, text_message='Слыш, ты че? Самый умный?')

def perevod_help(data):
    text_message = """
    Сейчас я научу тебя делать переводы.
    Чтобы перевести кому-то деньги, тебе нужно узнать ID этого персонажа
    Узнать ты можешь, просто спросив его. Он указан в /menu
    Нужно написать "перевод", затем ID и далее сумму
    Сумма пишется без точек, запятых и сокращений по типу 10к, 25кк и т.д.

    Пример отправки:

    Перевод 1 15000
    """
    send_message(data['from']['id'], text_message)

def send_message(chat_id, text_message):
    tbot.send_message(chat_id, text_message)

try:
    tbot.infinity_polling()
except Exception:
    print('reload')