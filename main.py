import json

import telebot
from config import get_tg_bot_key
import time
from api import marketapi


bot = telebot.TeleBot(get_tg_bot_key())

@bot.message_handler(commands=['start'])
def hello(message):
    msg = " Hi. This bot can help check current floor and floor Price Ratio\n"
    msg += """
    You can get data when set _collection ID_ from url
    
    Example: if you need check stats on collection 
    */collections/scroll-bubble-girls-x*
    You need sent *scroll-bubble-girls-x*
    """
    bot.send_message(message.chat.id, f'{msg}', parse_mode="Markdown")
    bot.register_next_step_handler(message, send_collection_data)


def send_collection_data(message):
    collection_data = marketapi.get_collection_data(message.text)
    if collection_data.status_code == 200:
        result = json.loads(collection_data.text)
        floor_price = result['data']['floorPrice']
        usd_floor_price = round(result['data']['usdFloorPrice'], 2)
        stats_1d_floor_price_ratio = round(result['data']['stats1D']['floorPriceRatio'], 4)
        stats_7d_floor_price_ratio = round(result['data']['stats7D']['floorPriceRatio'], 4)

        msg = f'Floor price: *{floor_price}* ETH\n'
        msg += f'USD floor price: *{usd_floor_price}* USD\n'
        msg += f'1 day floor price ratio: {stats_1d_floor_price_ratio}\n'
        msg += f'7 day floor price ratio: {stats_7d_floor_price_ratio}\n'
    else:
        msg = f'Error: \n{collection_data.text}'
    bot.send_message(message.chat.id, f'{msg}', parse_mode="Markdown")
    bot.register_next_step_handler(message, send_collection_data)


while True:
    try:
        bot.polling()
    except Exception as e:
        print(e)
        time.sleep(5)
