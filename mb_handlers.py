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

def user_email(bot, update):
    print(1)
