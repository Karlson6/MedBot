import logging

from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, RegexHandler, Filters

from mb_chart import *
from mb_handlers import *
import mb_settings as mbs



PROXY = mbs.PROXY

#TODO ЗАЧАТКИ ЛОГИРОВАНИЯ!!!! СЮДА НУЖНО ВЕРНУТЬСЯ
#____________________________________________

logging.basicConfig(filename = 'mbot.log',
                    format = ('%(name)s - %(levelname)s - %(message)s'),
                    level = logging.INFO)


def main():

    mbot = Updater(mbs.MedBot_key, request_kwargs = PROXY)
    logging.info('Бот запустился')
    dp = mbot.dispatcher

    autorization = ConversationHandler(
        entry_points = [RegexHandler('^(Авторизироваться)$', user_email, pass_user_data=True)], #Вход в диалог
        states = {
            'user_email':[MessageHandler(Filters.text, user_email, pass_user_data=True)],
            'user_get_email':[MessageHandler(Filters.text, user_get_email, pass_user_data=True)],
            'user_code':[MessageHandler(Filters.text, user_code, pass_user_data=True)],
            'test_code':[MessageHandler(Filters.text, test_code, pass_user_data=True)]
        },#Состояние
        fallbacks = [] #TODO Обработка ошибок
    )

    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(autorization)
    dp.add_handler(CommandHandler('menu', user_menu, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Получить график)$', mt_chart, pass_user_data=True))
    
    mbot.start_polling() # начни ходить на платформу telegram и проверять наличие сообщений
    mbot.idle() #будет выполнять пока принудитлеьноне остановим



if __name__ == '__main__':
    main()

