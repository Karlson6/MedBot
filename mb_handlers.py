import random
import smtplib, ssl #для работы с почтой
import sqlite3


from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, ConversationHandler

import mb_settings as mbs

#Запрос к бд
conn = sqlite3.connect(mbs.sqlite_file)
cursor = conn.cursor()
cursor.execute('''select distinct 'telegram_chat_id' from user where autorization = 'True' ''')
bot_user = cursor.fetchall() #авторизированные пользователи (chat id)
print(bot_user)


#Приветствуем пользователя, проверяем автоматизирован ли он
def greet_user (bot, update):
    update.message.reply_text(f'Привет, {update.message.chat.first_name}')
    user_chat = update.message.chat.id
    if user_chat in bot_user:
#--------------------------------------------------------------
#TODO                    ЗАГЛУШКА!!!!!!!!!!!!!
#--------------------------------------------------------------
        print(0)    
    else:
        aut_start(bot,update,user_chat=user_chat)

#Появление кнопки [Авторизация] у неавтоматизированного пользователя
def aut_start(bot, update, user_chat):
    aut_keyboard = [['Авторизироваться']]
    update.message.reply_text('Необходимо пройти авторизацию в системе', 
                              reply_markup = ReplyKeyboardMarkup(aut_keyboard, 
                              one_time_keyboard=True, 
                              resize_keyboard=True))
    return 'user_email'
    

#Запрашиваем email у пользователя
def user_email(bot, update):
    update.message.reply_text('Введите email', reply_markup=ReplyKeyboardRemove())
    return 'user_get_email'


#Получаем email от пользователя
def user_get_email(bot, update, user_data):
    user_email = update.message.text
    print(update.message)
    if '@' in user_email:
        print(2)
        update.message.reply_text('Введите код авторизации')
        send_code(bot=bot, update=update, user_data=user_data)
        # return 'send_code'
    else:
        update.message.reply_text('Некорректный email. Введите email')
        print(3)
        print(user_data)
        return 'user_get_email'
        

#Отправляем на email код авторизации
def send_code (bot, update, user_data):
    print(4.1)
    port = 465
    smtp_server = 'smtp.gmail.com'
    sender_email = mbs.email
    receiver_email = 'lena.korzinkina@mail.ru'
    password = mbs.email_password
    email_code = random.randint(1111,9999)
    massage = f'Код авторизации: {email_code}'
    massage = massage.encode('utf-8')
    context = ssl.create_default_context()
    print(4)
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, massage)
    user_code(bot=bot, update=update, user_data=user_data, email_code= email_code)


def user_code(bot, update, user_data, email_code): 
    user_data['user_code'] = update.message.text
    print(user_data)
    print('ага, я это сделал')
    return ConversationHandler.END
    test_code(bot=bot, update=update, user_data=user_data, email_code=email_code)
    # print(user_data)
    # return 'user_code'


#Проверяем соответствие присланного на почту кода введенного пользователем
def test_code(bot, update, user_data, email_code):
    print(user_data)






    

    
    
