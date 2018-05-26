import sqlite3
import telebot
import datetime
from telebot import types

token = '592422673:AAHQjN-JyevhnnkrAZ01fvyIwlDuic50PXU'
bot = telebot.TeleBot(token)

conn=sqlite3.connect('usersDatabase.db')
cursor=conn.cursor()

user_data={'number':'','address':'','name':'','age':''}

@bot.message_handler(commands=['start'])
def start(message):
    get_number(message)
    
def get_number(message):
    bot.send_message(message.chat.id,'(добавить текст типо как мы рады вас видеть и попросить телефон):')
    bot.register_next_step_handler(message,get_address)

def get_address(message):
    user_data['number']=message.text
    bot.send_message(message.chat.id,'Введите адрес:')
    bot.register_next_step_handler(message,get_name)

def get_name(message):
    user_data['address']=message.text
    bot.send_message(message.chat.id,'Введите имя:')
    bot.register_next_step_handler(message,get_age)

def get_age(message):
    user_data['name']=message.text
    bot.send_message(message.chat.id,'Введите возраст:')
    bot.register_next_step_handler(message,get_check_info)

def get_check_info(message):
    user_data['age']=message.text
    keyboard=types.ReplyKeyboardMarkup(resize_keyboard=True)
    confirm_button=types.KeyboardButton('Подтвердить')
    back_button=types.KeyboardButton('Назад')
    keyboard.add(confirm_button)
    keyboard.add(back_button)
    bot.send_message(message.chat.id,'Подтвердите введенные Вами данные:'+'\n\n'
                     'Номер телефона: '+user_data['number']+'\n'
                     'Адрес: '+user_data['address']+'\n'
                     'Имя: '+user_data['name']+'\n'
                     'Возраст: '+user_data['age'],reply_markup=keyboard)
    
conn.commit()
conn.close()


bot.polling(none_stop=True)
