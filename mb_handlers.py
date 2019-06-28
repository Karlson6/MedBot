from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater

bot_user = set() #авторизированные пользователи (chat id)

def greet_user (bot, update):
    user_chat = update.message.chat.id
    print(bot_user)
    if user_chat in bot_user:

#..............................................................
#............................ЗАГЛУШКА!!!!!!!!!!!!!.............
#..............................................................

        print(0)    
    else:
        aut_keyboard = [['Авторизироваться']]
        update.message.reply_text('Пройдите авторизацию', reply_markup = ReplyKeyboardMarkup(aut_keyboard, 
                                                                     one_time_keyboard=True, 
                                                                     resize_keyboard=True)
        ) 