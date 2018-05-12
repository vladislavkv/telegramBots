import telebot
from datetime import datetime
from telebot import types
import wikipedia
import requests
  
token = '569481488:AAFEuJuynoOvJPB6aznybtW_KCeO9DctWas'

bot = telebot.TeleBot(token)

def getTimeNow():
    return datetime.strftime(datetime.now(), '%d.%m.%Y %H:%M:%S')

def writeToLog(who,text):
    file = open('log.txt','a+',encoding='utf-8')
    file.write(getTimeNow()+" "+str(who)+" "+str(text)+'\n')
    file.close()
    
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Привет, друг!')
    writeToLog(message.from_user.id,'Пользователь начал использовать бота')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    wordButton = types.KeyboardButton('Узнать слово')
    keyboard.add(wordButton)
    
    translateButton = types.KeyboardButton('Перевести слово')
    keyboard.add(translateButton)
    
    kursButton = types.KeyboardButton('Курс валют')
    keyboard.add(kursButton)
    
    weatherButton = types.KeyboardButton('Узнать погоду')
    keyboard.add(weatherButton)
    bot.send_message(message.from_user.id,'Выбери вариант: ',reply_markup=keyboard)
    bot.register_next_step_handler(message,choiseUser)

def choiseUser(message):
    if message.text == 'Узнать слово':
        writeToLog(message.from_user.id,'Пользователь выбрал "узнать слово"')
        bot.send_message(message.from_user.id,'Введите слово:')
        bot.register_next_step_handler(message,searchWord)
    elif message.text == 'Перевести слово':
        bot.send_message(message.from_user.id,'Введите слово:')
        writeToLog(message.from_user.id,'Пользователь ввел в переводчик '+message.text)
        bot.register_next_step_handler(message,messageTranslate)
    else:
        bot.send_message(message.from_user.id,'Ошибка (такого варианта нет)')
        bot.register_next_step_handler(message,choiseUser)

def messageTranslate(message):
    respone=requests.post('https://translate.yandex.net/api/v1.5/tr.json/translate',
                 data={'key':'trnsl.1.1.20180428T041521Z.072966e4a243b04b.40f01b187f24cfe83251005676e3620fc70c3b2d',
                       'text':message.text,'lang':'ru-en'}).json()
    bot.send_message(message.from_user.id,respone['text'])
    bot.register_next_step_handler(message,choiseUser)

def searchWord(message):
    try:
        wikipedia.set_lang('ru')
        bot.send_message(message.from_user.id,wikipedia.summary(message.text))
        writeToLog(message.from_user.id,'user search'+message.text)
        bot.register_next_step_handler(message,choiseUser)
    except:
        bot.send_message(message.from_user.id,'Ошибка (слово не найдено)')
        bot.register_next_step_handler(message,choiseUser)
    
try:
    bot.polling(none_stop=True)
except:
    writeToLog('','ошибка запуска')


