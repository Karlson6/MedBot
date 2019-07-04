import db_peewee as dbp
from glob import glob
import matplotlib.pyplot as plt
import os
from peewee import *
import sqlite3

from telegram.ext import Updater

import mb_settings as mbs
from mb_handlers import *

#Медицинские показатели пользователей
def mt_chart (bot, update, user_data):
    u_chat(bot=bot, update=update, user_data=user_data)
    user_chat = user_data['user_chat']

    query = dbp.UserMedTest.select(dbp.User.telegram_chat_id,
                                dbp.UserMedTest.med_test_date,
                                dbp.UserMedTest.med_test_value).join(dbp.User, on=(dbp.UserMedTest.id_user == dbp.User.id)).where(dbp.User.telegram_chat_id == user_chat).order_by(dbp.UserMedTest.med_test_date)

    user_mt = [e for e in query.tuples()] #Создаем кортежи из запроса
    if len(user_mt)==0:
        update.message.reply_text('Нет данных')
    else:
        mt_time = []
        mt_value = []
        for mt in user_mt:
            mt_time.append(mt[1])
            mt_value.append(mt[2])

        folder_name = mbs.result_folder
        chart = plt.plot(mt_time, mt_value)
        file_name = str(user_chat)+'.png'
        chart_pic = os.path.join(folder_name, file_name)
        plt.savefig(chart_pic)
        bot.send_photo(chat_id=user_chat, photo=open(chart_pic, 'r+b'))
    
    

