import sqlite3
import telebot
from datetime import datetime
from telebot import types

token = '592422673:AAHQjN-JyevhnnkrAZ01fvyIwlDuic50PXU'
bot = telebot.TeleBot(token)

conn=sqlite3.connect('usersDatabase.db')
cursor=conn.cursor()

def getTimeNow():
    return datetime.strftime(datetime.now(), '%d.%m.%Y %H:%M:%S')

def writeToLog(who,text):
    file=open('log.txt','a+',encoding='utf-8')
    file.write(getTimeNow()+" "+str(who)+" "+str(text)+'\n')
    file.close()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'(добавить текст типо как мы рады вас видеть и попросить телефон): ')
    writeToLog(message.from_user.id,'Пользователь начал использовать бота')

conn.commit()
conn.close()
