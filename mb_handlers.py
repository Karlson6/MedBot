import random

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater

bot_user = set() #авторизированные пользователи (chat id)

#Приветствуем пользователя, проверяем автоматизирован ли он
#--------------------------------------------------------------
#         ПОТОМ ПОМЕНЯТЬ НА ЗАПРОС ИЗ БАЗЫ!!!!!!!!!!!!
#--------------------------------------------------------------
def greet_user (bot, update):
    update.message.reply_text(f'Привет, {update.message.chat.first_name}')
    user_chat = update.message.chat.id
    if user_chat in bot_user:
#--------------------------------------------------------------
#                       ЗАГЛУШКА!!!!!!!!!!!!!
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
    update.message.reply_text('Введите email')
    return 'user_get_email'


#Получаем email от пользователя
def user_get_email(bot, update):
    user_email = update.message.text
    if '@' in user_email:
        print(user_email)
    else:
        update.message.reply_text('Введите email')
        return 'user_get_email'


#Отправляем на email код авторизации
def send_email(bot, update):
    port = 465
    smtp_server = 'smtp.gmail.com'
    sender_email = mbs.email
    receiver_email = 'lena.korzinkina@mail.ru'
    password = mbs.email_password
    email_code = random.randint(1111,9999)
    massage = f'Код авторизации: {email_code}'
    massage = massage.encode('utf-8')
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, massage)

    
