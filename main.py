import config
import telebot
import requests
from config import token
from telebot import types


def telegram_bot():
    bot = telebot.TeleBot(token)
    response = requests.get(config.url).json()

    # При введенні команди '/start' привітаємося з користувачем.
    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Привіт ✋\nЩоб ознайомитись з моїми функціями напиши: \n/help")

    # При введенні команди '/help' появляється список команд.
    @bot.message_handler(commands=["help"])
    def help_message(message):
        bot.send_message(message.chat.id, "Сommand list: ⚙\n/quote- цитати відомих людей 💡"
                                          "\n/joke - випадковий жарт 😂"""
                                          "\n/exchange - курс валют 💰")

    # При введенні команди '/quotes' появляється випадкова читата.
    @bot.message_handler(commands=["quote"])
    def quotes_message(message):
        url = "https://quotes15.p.rapidapi.com/quotes/random/"

        headers = {
            'x-rapidapi-key': "30ac74a7a3msh5ce4d557e7296c7p13cdf0jsn89552fa140f3",
            'x-rapidapi-host': "quotes15.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers)
        rq = response.json()
        out_quotes = rq["content"]
        out_quotess = rq["originator"]["name"]
        bot.send_message(
            message.chat.id,
            f"❕{out_quotes},\n"
            f"👨🏻‍💼{out_quotess}"
        )

    # При введенні команди '/joke' появляється випадковй жарт.
    @bot.message_handler(commands=["joke"])
    def jokes_message(message):
        rq = requests.get("https://official-joke-api.appspot.com/random_joke")
        response = rq.json()
        setup_que = response["setup"]
        setup_ans = response["punchline"]
        bot.send_message(
            message.chat.id,
            f" -{setup_que},\n-{setup_ans}😂😂😂")

    # При введенні команди '/exchange' появляється курс валют, таких як usd/eur/rur/btc.

    @bot.message_handler(commands=['exchange'])
    def send_exch(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('USD')
        itembtn2 = types.KeyboardButton('EUR')
        itembtn3 = types.KeyboardButton('RUB')
        itembtn4 = types.KeyboardButton('BTC')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        msg = bot.send_message(message.chat.id,
                               "Дізнатись курс ПриватБанку у відділенні", reply_markup=markup)
        bot.register_next_step_handler(msg, process_coin_step)

    def process_coin_step(message):
        try:
            markup = types.ReplyKeyboardRemove(selective=False)

            for coin in response:
                if (message.text == coin['ccy']):
                    bot.send_message(message.chat.id, printCoin(coin['buy'], coin['sale']),
                                     reply_markup=markup, parse_mode="Markdown")

        except Exception as e:
            bot.reply_to(message, 'ooops!')

    def printCoin(buy, sale):
        '''Вивід курсу користувачу'''
        return "💰 *Курс купівлі:* " + str(buy) + "\n💰 *Курс продажу:* " + str(sale)

    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()

    bot.polling()

if __name__ == '__main__':
    telegram_bot()
