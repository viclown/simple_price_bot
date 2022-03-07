import telebot
from binance.spot import Spot
from typing import Tuple


client = Spot()
bot = telebot.TeleBot('secret_token')


def get_price(currency: str) -> Tuple[float]:
    info = client.klines(currency+"USDT", "1m", limit=1)
    sell_price = float(info[0][2])
    buy_price = float(info[0][3])
    return sell_price, buy_price

@bot.message_handler(commands=["start"])
def start(m, res=False) -> None:
    bot.send_message(m.chat.id, 'Введите, пожалуйста, тикер')

@bot.message_handler(content_types=["text"])
def handle_text(message: str) -> None:
    try:
        prices = get_price(message.text.upper())
        bot.send_message(message.chat.id,
                         'Лучшая цена для продажи: 1 {0} = {1} USDT \nЛучшая цена для покупки: 1 {0} = {2} USDT'.format(message.text.upper(), prices[0], prices[1]))
    except:
        bot.send_message(message.chat.id, 'Пожалуйста, проверьте корректность введенного вами тикера!')

bot.polling(none_stop=True, interval=0)
