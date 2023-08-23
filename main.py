import datetime
import time
import asyncio
import json

from bs4 import BeautifulSoup
import requests
from aiogram import types, Dispatcher, Bot, executor
from aiogram.dispatcher.filters import Text
from config import TOKEN

url1 = 'https://fragment.com/numbers?sort=price_asc&filter=sale'
url2 = 'https://getgems.io/collection/EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N?filter=%7B"saleType"%3A"fix_price"%7D'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
pause = True
num = 300


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global pause, num, url1, url2
    pause = True
    await bot.send_message(message.chat.id, 'Парсинг запущен')

    while True:
        content1 = requests.get(url1)
        soup1 = BeautifulSoup(content1.text, 'lxml')

        try:
            if int(soup1.find('div', class_='table-cell-value tm-value icon-before icon-ton').text) <= num:
                await bot.send_message(message.chat.id, f'Время: {datetime.datetime.now().replace(microsecond=0)}')
                await bot.send_message(message.chat.id,
                                       'https://fragment.com' + soup1.find('a', class_='table-cell').attrs['href'])
        except:
            continue

        await asyncio.sleep(10)
        if not pause:
            break


@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    global pause
    pause = False
    await bot.send_message(message.chat.id, 'Парсинг остановлен')


@dp.message_handler(commands=['count'])
async def count(message: types.Message):
    await bot.send_message(message.chat.id, 'Введи максимальную стоимость для парсинга 👇🏼')


@dp.message_handler(Text)
async def set_count(message: types.Message):
    global num
    try:
        num = int(message.text)
    except:
        num = 0
    if num:
        await bot.send_message(message.chat.id, f'Установлена максимальная стоимость < {num}')
    else:
        await bot.send_message(message.chat.id, f'Это не число, попробуй еще раз')


executor.start_polling(dp, skip_updates=True)
