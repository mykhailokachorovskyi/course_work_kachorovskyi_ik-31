import config
import telebot
import requests
from config import token
from config import random_dog_api


def telegram_bot():
    bot = telebot.TeleBot(token)

    # При введенні команди '/start' привітаємося з користувачем.

    @bot.message_handler(commands=["start"])
    def main(message):
        bot.send_message(message.chat.id, '\nПривіт!' '\nНапиши /help, щоб ознайомитись з моїми функціями'
                                          '\n'
                                          '\n'
                                          'Посміхнись 😊')

    # При введенні команди '/help' виведемо команди для роботи з ботом.
    @bot.message_handler(commands=["help"])
    def command_help(message):
        bot.send_message(message.chat.id, 'Command list:''\n/instagram- інформація про сторінку інстаграм 📷'
                                          '\n/numbers- цікаві факти про цифри 🔢'
                                          '\n/cats- випадкові фото котиків 🐈'
                                          '\n'
                                          '\n''Життя прекрасне 🤠')

    # При введенні команди '/random_dog' виведемо випадкове фото чи відео собаки.
    @bot.message_handler(commands=['random_dog'])
    def random_dog(message):
        try:
            r = requests.get(url=config.random_dog_api)
            response = r.json()
        except:
            bot.send_message(message.chat.id, 'Нажаль не вдалось отримати відповідь 😔')
            return

        # bot.send_message(message.chat.id, f'[Random dog]({response["url"]})', parse_mode='markdown')
        extension = response["url"].split('.')[-1]
        # Якщо відео
        if ('mp4' in extension):
            bot.send_video(message.chat.id, response["url"])
        # gif
        elif ('gif' in extension):
            bot.send_video_note(message.chat.id, response["url"])
        # Фото
        else:
            bot.send_photo(message.chat.id, response["url"])

    bot.polling()


if __name__ == '__main__':
    telegram_bot()
