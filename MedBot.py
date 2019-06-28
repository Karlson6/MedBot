import logging

from telegram.ext import Updater, CommandHandler, RegexHandler, ConversationHandler

from mb_handlers import *
import mb_settings as mbs


PROXY = mbs.PROXY

#ЗАЧАТКИ ЛОГИРОВАНИЯ!!!! СЮДА НУЖНО ВЕРНУТЬСЯ
#____________________________________________

logging.basicConfig(filename = 'mbot.log',
                    format = ('%(name)s - %(levelname)s - %(message)s'),
                    level = logging.INFO)


def main():

    mbot = Updater(mbs.MedBot_key, request_kwargs = PROXY)
    logging.info('Бот запустился')
    dp = mbot.dispatcher

    autorization = ConversationHandler(
        entry_points = [RegexHandler('^(Авторизироваться)$', user_email)], #Вход в диалог
        states = {
            '':[]
        },#Состояние
        fallbacks = []#Обработка ошибок
    )

    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(autorization)
    
    mbot.start_polling() # начни ходить на платформу telegram и проверять наличие сообщений
    mbot.idle() #будет выполнять пока принудитлеьноне остановим



if __name__ == '__main__':
    main()

