import telebot
import msql

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