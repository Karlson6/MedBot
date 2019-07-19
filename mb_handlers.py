import datetime
import os
import random
import re  # Регулярные выражения
import smtplib  # для работы с почтой
import sqlite3
import ssl

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, Updater

import db_peewee as dbp
import filetype
import mb_settings as mbs
from peewee import *  # Для работы с бд

#Стартовавшие бота пользователи
bot_not_user = set()
query_nu = dbp.User.select().where(dbp.User.id_status < 3)
for not_user in query_nu:
    bot_not_user.add(not_user.telegram_chat_id)

#Авторизированные пользователи
bot_user = set()
query = dbp.User.select().where(dbp.User.id_status >= 3)
for user in query:
    bot_user.add(int(user.telegram_chat_id))

#Статус пользователя в бд
# def user_status(user_data):
#     print(user_data['user_chat'])    
#     st_set = set()
#     user_st = dbp.User.select().where(dbp.User.telegram_chat_id == user_data['user_chat'])
#     for st in user_st:
#         st_set.add(st.id_status)
#     print(status_set)
    # user_status = status_set[0]
    # return user_status

#Определяем id_chat пользователя
def u_chat(bot, update, user_data):
    user_chat = int(update.message.chat.id)
    user_data['user_chat'] = user_chat
    user_name = update.message.chat.first_name
    user_data['user_name'] = user_name
    return user_data



#Приветствуем пользователя, проверяем автоматизирован ли он
def greet_user (bot, update, user_data):
    # user_chat = int(update.message.chat.id)
    # user_name = update.message.chat.first_name
    # user_data['user_chat'] = user_chat
    u_chat(bot=bot, update=update, user_data=user_data)
    user_chat = user_data['user_chat']
    user_name = user_data['user_name']
    update.message.reply_text(f'Привет, {user_name}')
    if user_chat in bot_user:
        user_menu(bot=bot, update=update, user_data=user_data)
    elif user_chat in bot_not_user:
        print('Пользователь уже есть')
        aut_start(bot,update,user_data=user_data)
    else:
        #Последний id пользователя
        max_user_id = dbp.User.select(fn.MAX(dbp.User.id)).scalar()
        dbp.User.create(id=max_user_id+1, name=user_name, telegram_chat_id=user_chat, id_status=0)
        aut_start(bot,update,user_data=user_data)

#Появление кнопки [Авторизация] у неавтоматизированного пользователя
def aut_start(bot, update, user_data):
    aut_keyboard = [['Авторизироваться']]
    update.message.reply_text('Необходимо пройти авторизацию в системе', 
                              reply_markup = ReplyKeyboardMarkup(aut_keyboard, 
                              one_time_keyboard=True, 
                              resize_keyboard=True))
    return 'user_email'
   

#Запрашиваем email у пользователя
def user_email(bot, update, user_data):
    update.message.reply_text('Введите email', reply_markup=ReplyKeyboardRemove())
    return 'user_get_email'


#Получаем email от пользователя
def user_get_email(bot, update, user_data):
    user_email = update.message.text
    if '@' in user_email:
        user_data['user_email']=user_email
        db_chat_id = dbp.User.telegram_chat_id
        # Обновляем id_status у пользователя в БД
        query = dbp.User.update(id_status = 1, email = user_email).where(dbp.User.telegram_chat_id == user_data['user_chat'])
        query.execute()
        send_code(bot=bot, update=update, user_data=user_data)
        # return 'send_code'
    else:
        update.message.reply_text('Некорректный email. Введите email')
        return 'user_get_email'
        

#Отправляем на email код авторизации
def send_code (bot, update, user_data):
    print(4.1)
    port = 465
    smtp_server = 'smtp.gmail.com'
    sender_email = mbs.email
    receiver_email = user_data['user_email']
    password = mbs.email_password
    email_code = random.randint(1111,9999)
    message = f'Код авторизации: {email_code}'
    message = message.encode('utf-8')
    context = ssl.create_default_context()
    print(4)
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    print(status)
    print('Введите код авторизации')
    # update.message.reply_text('Введите код авторизации')
    if status == 1:
        print(user_data)
        user_code(bot=bot, update=update, user_data=user_data)

    

def user_code(bot, update, user_data):
    query = dbp.User.update(id_status = 2).where(dbp.User.telegram_chat_id == user_data['user_chat'])
    query.execute()
    status = 2
    if status == 2:
        user_code = update.message.text
        user_data['user_code'] = user_code
        print(user_data)
        print('ага, я это сделал')
        test_code(bot=bot, update=update, user_data=user_data)
    # print(user_data)
    # return 'user_code'


#Проверяем соответствие присланного на почту кода введенного пользователем
def test_code(bot, update, user_data):
    print(user_data)

#Пользовательское меню
def user_menu(bot, update, user_data):
    mt_keyboard = [['Внести результат','Отправить PDF', 'Получить график']]
    update.message.reply_text('Выберите пункт меню', 
                              reply_markup = ReplyKeyboardMarkup(mt_keyboard, 
                              one_time_keyboard=True, 
                              resize_keyboard=True))   

#Просим пользователя ввести дату анализа
def user_mt_start(bot, update, user_data):
    update.message.reply_text('Введите дату и время анализа в формате "дд.мм.гггг_чч.мм"(например: 05.07.2019_10.51):')
    return 'value'

#Просим пользователя ввести значение анализа
def user_mt_value(bot, update, user_data):
    user_data['mt_date'] = update.message.text
    update.message.reply_text('Введите значение анализа (например: 51,01):')
    return 'user_mt'

# Просим прислать PDF

def document_handler(bot, update):
    file = bot.getFile(update.message.document.file_id)
    print ("file_id: " + str(update.message.document.file_id))

    # генерируем имя для сохраняемого файла (имя основывается на chat id и текущем времени)
    file_name = f'upcoming_data/{update.message.chat.id}_{datetime.datetime.now()}.pdf'
    file.download(file_name)

    # проверяем файл на PDF
    type_file = filetype.guess(file_name)
    if type_file.extension == 'pdf':
        update.message.reply_text('файл сохранен')
    else:
        update.message.reply_text('формат не распознан, пришлите PDF')
        os.remove(file_name)
        return


    
   


#Сохраняем результат в бд
def user_mt(bot, update, user_data):
    user_data['mt_value'] = update.message.text
    u_chat(bot=bot, update=update, user_data=user_data)

    max_test_id = dbp.UserMedTest.select(fn.MAX(dbp.UserMedTest.id)).scalar()
    user_id = dbp.User.get(dbp.User.telegram_chat_id==user_data['user_chat']) #Возвращаем из бд id пользователя  
    dbp.UserMedTest.create(id=max_test_id+1, 
                           id_med_test=1, 
                           id_user=user_id, 
                           med_test_date=user_data['mt_date'], 
                           med_test_value=user_data['mt_value'])

    return ConversationHandler.END
