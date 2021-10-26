from random import randint, random
import telebot
from telebot.apihelper import send_message
import msql
from settings import api_token
import text
import games
import random
import prikol

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('Вас приветствует Musya Bot')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
print('\nДанный бот создан с развлекательной целью\nи не может быть распространяться на платной основе\n\n')
print('Токен авторизации: ' + api_token)

tbot = telebot.TeleBot(api_token)

def get_text(message):
    print(message['from']['username'] + ' - ' + message['text'])
    sort_start(message)

def callback_query_sort(call):
    key = call['data']
    if key == 'kosti_from_menu':
        kosti_games(call)
    elif 'kosti_' in key:
        kosti_games_part2(call, key)
    elif 'contra' in key:
        kosti_games_part3(call, key)
    elif 'mine_game' in key:
        key_list = key.split('|')
        nickname = call['from']['username']
        if key_list[2] == nickname:
            mines_game_part2(call, key)
    elif key == 'mines_start':
        mines_start(call)
    elif key == 'mines_start_button':
        game_mines(call)

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
    elif message_text== '/contacts':
        cmd_about(data)
    elif message_split[0].lower() == 'перевод':
        perevod(message_split, data)
    elif message_text == '/prikol':
        cmd_prikol(data)
    elif message_text == '/top':
        cmd_top_10(data)
    else:
        razgovor(data)

def cmd_top_10(data):
    top_list = msql.get_top_10()
    text_message = """
    Топ-10 игроков по балансу:\n\n
    """
    for player in top_list:
        text_message = text_message + '@' + player[2] + ' - ' + str(player[1]) + '$\n'
    chat_id = data['from']['id']
    send_message(chat_id, text_message)

def razgovor(data):
    print('1')

def cmd_prikol(data):
    text_message = prikol.start()
    chat_id = data['from']['id']
    send_message(chat_id, text_message)

def cmd_start(data):
    if msql.cmd_start(data) == True:
        chat_id = data['from']['id']
        text_message = text.hello_text()
        send_message(chat_id, text_message)

def cmd_about(data):
    text_message = text.info()
    chat_id = data['from']['id']
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

        /top - топ-10 игроков по балансу
        /games - тут ты можешь потерять все свои деньги
        /perevod - подробнее о системе переводов
        /prikol - подключил что-то по API, но кажется херня

        /contacts - контакты разработчика
    """
    send_message(chat_id, text_message)
    
def cmd_games(data):
    text_message = """
    Список игр, которые я смог сделать\n\n
    """
    markup = telebot.types.InlineKeyboardMarkup()
    button_1 = telebot.types.InlineKeyboardButton(text='Кости', callback_data='kosti_from_menu')
    button_2 = telebot.types.InlineKeyboardButton(text='Подрывник', callback_data='mines_start_button')
    markup.add(button_1, button_2)
    tbot.send_message(chat_id=data['from']['id'], text=text_message, reply_markup=markup)

def kosti_games(data):
    text_message = 'Выбери число, на которое хочешь поставить:\n\n*нажми 1 раз и жди*'
    markup = games.kosti_gen6keys()
    tbot.edit_message_text(chat_id=data['from']['id'], text=text_message, message_id=data['message']['message_id'], reply_markup=markup)

def kosti_games_part2(data, key):
    key_id = key.replace('kosti_', '')
    answer = games.kosti_set_price(data, key_id)
    nickname = data['from']['username']
    money = msql.get_count(nickname)
    text_message = f"""
    Сейчас выбери ставку из предложенных:
    
    Твой баланс - {money}$

    *нажми 1 раз и жди*"""
    #tbot.send_message(data['chat']['id'], text_message, reply_markup=answer)
    tbot.edit_message_text(text=text_message, message_id=data['message']['message_id'], reply_markup=answer, chat_id=data['from']['id'])

def kosti_games_part3(data, key):
    price = int(key.replace('_contra', ''))
    stavka = int(msql.get_kosti_set(data['from']['username']))
    winner = random.randint(1, 6)
    old_count = int(msql.get_count(data['from']['username']))
    markup = telebot.types.InlineKeyboardMarkup()
    button_1 = telebot.types.InlineKeyboardButton(text='ХОЧУ ЕЩЕ!', callback_data='kosti_from_menu')
    markup.add(button_1)
    if stavka == winner:
        new_count = old_count + price * 8
        price_1 = price * 8
        if msql.set_new_count(data['from']['username'], new_count) == True:
            text_message = f"""
            Поздравлю тебя, друг.\n
            Ты выйграл {price_1} денег

            Твой баланс: {new_count}$

            главное меню - /menu
            """
            tbot.edit_message_text(chat_id=data['from']['id'], text=text_message, message_id=data['message']['message_id'], reply_markup=markup)
    else:
        new_count = old_count - price
        if msql.set_new_count(data['from']['username'], new_count) == True:
            text_message = f"""
            К сожалению, ты продул...\n
            Выпало {winner}, а ты поставил на {stavka}
            Ты проиграл {price} денег

            Твой баланс: {new_count}$

            главное меню - /menu
            """
            tbot.edit_message_text(chat_id=data['from']['id'], text=text_message, message_id=data['message']['message_id'], reply_markup=markup)

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

def game_mines(data):
    text_message = """
    В этой игре тебе нужно угадать
    в каких клетках нет мин.
    Режим по умолчанию хардкор
    Поле 3*3 клетки
    3 мины
    Как только ты отметишь все клетки без мин, получишь награду
    
    Играем?
    """
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text='Да!', callback_data='mines_start')
    markup.add(button)
    tbot.edit_message_text(chat_id=data['from']['id'], text=text_message, message_id=data['message']['message_id'], reply_markup=markup)
    #tbot.send_message(data['chat']['id'], text_message, reply_markup=markup)

def mines_start(data):
    mark = games.mines_start(data)
    text_message = 'Удачи!'
    tbot.edit_message_text(chat_id=data['from']['id'], text=text_message, message_id=data['message']['message_id'], reply_markup=mark)

def mines_game_part2(data, key):
    nickname = data['from']['username']
    all_pole_list = data['message']['reply_markup']['inline_keyboard']
    key_sort = key.split('|')
    shot = key_sort[1]
    mines_list_srting_version = key_sort[3]
    mines_list = mines_list_srting_version.split('!')
    count_ok = int(key_sort[4])
    if shot in mines_list:
        dop_money = 0
        count_new = msql.get_count(nickname)
        if count_ok > 0:
            dop_money = dop_money + (count_ok * 100)
            count_now = msql.get_count(nickname)
            count_new = int(count_now) + int(dop_money)
            msql.set_new_count(nickname, count_new)
        text_message = f"""
        Ты подорвался на мине!
        Повезет в другой раз.

        За открытые клетки даю тебе {dop_money}$
        Твой баланс: {str(count_new)}$

        /menu - основное меню
        """
        markup = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton(text='Еще раз подорваться', callback_data='mines_start_button')
        markup.add(button)
        tbot.edit_message_text(chat_id=data['from']['id'], text=text_message, message_id=data['message']['message_id'], reply_markup=markup)
    else:
        new_text = '⚪️'
        old_text = '❔'
        list1 = []
        list2 = []
        list3 = []
        for button_info in all_pole_list[0]:
            if button_info['callback_data'] == key:
                list1.append(telebot.types.InlineKeyboardButton(text=new_text, callback_data='123'))
            elif button_info['text'] == '⚪️':
                list1.append(telebot.types.InlineKeyboardButton(text=new_text, callback_data=button_info['callback_data']))
            else:
                list1.append(telebot.types.InlineKeyboardButton(text=old_text, callback_data=new_callback_data(button_info['callback_data'])))
        for button_info in all_pole_list[1]:
            if button_info['callback_data'] == key:
                list2.append(telebot.types.InlineKeyboardButton(text=new_text, callback_data='123'))
            elif button_info['text'] == '⚪️':
                list2.append(telebot.types.InlineKeyboardButton(text=new_text, callback_data=button_info['callback_data']))
            else:
                list2.append(telebot.types.InlineKeyboardButton(text=old_text, callback_data=new_callback_data(button_info['callback_data'])))
        for button_info in all_pole_list[2]:
            if button_info['callback_data'] == key:
                list3.append(telebot.types.InlineKeyboardButton(text=new_text, callback_data='123'))
            elif button_info['text'] == '⚪️':
                list3.append(telebot.types.InlineKeyboardButton(text=new_text, callback_data=button_info['callback_data']))
            else:
                list3.append(telebot.types.InlineKeyboardButton(text=old_text, callback_data=new_callback_data(button_info['callback_data'])))
        markup = telebot.types.InlineKeyboardMarkup(keyboard=(list1, list2, list3))
        tbot.edit_message_text(chat_id=data['from']['id'], text='Удачи!', message_id=data['message']['message_id'], reply_markup=markup)
        if int(count_ok) == 5:
            money = msql.get_count(nickname) + 5000
            msql.set_new_count(nickname, money)
            new_money = msql.get_count(nickname)
            text_message = f"""
            Поздравляю, ты победил!
            Приз 5000$ заслужил
            Твой баланс: {new_money}$
            """
            markup = telebot.types.InlineKeyboardMarkup()
            button = telebot.types.InlineKeyboardButton(text='Еще играем!', callback_data='mines_start_button')
            markup.add(button)
            tbot.edit_message_text(chat_id=data['from']['id'], text=text_message, message_id=data['message']['message_id'], reply_markup=markup)

def send_message(chat_id, text_message):
    tbot.send_message(chat_id, text_message)

def new_callback_data(old_keys):
    spisok_data = old_keys.split('|')
    old_count_data = spisok_data[4]
    new_count_data = int(old_count_data) + 1
    new_data = spisok_data[0] + '|' + spisok_data[1] + '|' + spisok_data[2] + '|' + spisok_data[3] + '|' + str(new_count_data)
    return(new_data)
    
def out_of_rande(data):
    text_message = 'Вы ввели неверный ID'
    chat_id = data['message']['from']['id']
    send_message(chat_id, text_message)