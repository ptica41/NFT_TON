import datetime
import time
import asyncio
import json
import requests

from bs4 import BeautifulSoup
from aiogram import types, Dispatcher, Bot, executor
from aiogram.dispatcher.filters import Text
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


from config import TOKEN

URL1 = 'https://fragment.com/numbers?sort=price_asc&filter=sale'
URL2 = 'https://getgems.io/collection/EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N?filter=%7B%22saleType%22%3A%22fix_price%22%7D'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
run1 = False
run2 = False
bid = 0

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


@dp.message_handler(commands=['start_fragment'])
async def start(message: types.Message):
    global run1, bid, URL1
    if not run1:
        run1 = True
        await bot.send_message(message.chat.id, 'Парсинг площадки №1 запущен')

        while run1:
            content1 = requests.get(URL1)
            soup = BeautifulSoup(content1.text, 'lxml')

            try:
                if float(soup.find('div', class_='table-cell-value tm-value icon-before icon-ton').text.replace(',', '.')) <= bid:
                    await bot.send_message(message.chat.id, f'Время: {datetime.datetime.now().replace(microsecond=0)}')
                    await bot.send_message(message.chat.id,
                                           'https://fragment.com' + soup.find('a', class_='table-cell').attrs['href'])
            except:
                continue

            await asyncio.sleep(10)

    else:
        await bot.send_message(message.chat.id, 'Парсинг площадки №1 уже запущен')


@dp.message_handler(commands=['stop_fragment'])
async def stop(message: types.Message):
    global run1
    run1 = False
    await bot.send_message(message.chat.id, 'Парсинг площадки №1 остановлен')


@dp.message_handler(commands=['start_getgems'])
async def start(message: types.Message):
    global run2, bid, URL2, options
    if not run2:
        run2 = True
        await bot.send_message(message.chat.id, 'Парсинг площадки №2 запущен')

        while run2:
            try:
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                driver.get(URL2)
                driver.implicitly_wait(5)
                content2 = driver.find_element(By.CLASS_NAME, 'NftItemContainer').find_element(By.TAG_NAME, 'a')
                if float(content2.find_element(By.CLASS_NAME, 'CryptoPrice__amount').text.replace(',', '.')) <= bid:
                    await bot.send_message(message.chat.id, f'Время: {datetime.datetime.now().replace(microsecond=0)}')
                    await bot.send_message(message.chat.id, content2.get_attribute('href'))
            except Exception as e:
                print(e)
                continue

            driver.quit()
            await asyncio.sleep(20)
    else:
        await bot.send_message(message.chat.id, 'Парсинг площадки №2 уже запущен')


@dp.message_handler(commands=['stop_getgems'])
async def stop(message: types.Message):
    global run2
    run2 = False
    await bot.send_message(message.chat.id, 'Парсинг площадки №2 остановлен')


@dp.message_handler(commands=['info'])
async def count(message: types.Message):
    global bid, run1, run2
    await bot.send_message(message.chat.id, f'Максимальная стоимость 👉🏼 {bid} TON')
    if run1:
        await bot.send_message(message.chat.id, f'Площадка №1 запущена')
    else:
        await bot.send_message(message.chat.id, f'Площадка №1 остановлена')
    if run2:
        await bot.send_message(message.chat.id, f'Площадка №2 запущена')
    else:
        await bot.send_message(message.chat.id, f'Площадка №2 остановлена')


@dp.message_handler(Text)
async def set_count(message: types.Message):
    global bid
    try:
        bid = int(message.text)
    except:
        bid = 0
    if bid:
        await bot.send_message(message.chat.id, f'Установлена максимальная стоимость 👉🏼 {bid} TON')
    else:
        await bot.send_message(message.chat.id, f'Это не число, попробуй еще раз')


executor.start_polling(dp, skip_updates=True)
