import asyncio
from flask import Flask, request, render_template
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from config import TOKEN, OPENWEATHER_API_KEY
import random


bot = Bot(token=TOKEN)
dp = Dispatcher()


def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=10)  # Установим тайм-аут в 10 секунд
        response.raise_for_status()  # Проверка на успешность запроса
        data = response.json()
        return f"Погода в {city}: {data['main']['temp']}°C"
    except requests.exceptions.Timeout:
        return "Превышено время ожидания. Попробуйте еще раз."
    except requests.exceptions.RequestException as e:
        return f"Произошла ошибка: {e}"

@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://optim.tildacdn.com/tild3462-3133-4234-a131-376161313063/-/resize/824x/-/format/webp/shutterstock_2059100.jpg',
            'https://cdn.tripster.ru/thumbs2/9b82ce68-6198-11eb-985d-de81d5d267e0.800x600.jpg',
            'https://optim.tildacdn.com/tild3162-6134-4466-a230-353035323762/-/resize/824x/-/format/webp/shutterstock_2145516.jpg']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption="Фото г.Суздаль")

@dp.message(F.text == "Что такое бот?")
async def bottext(message: Message):
    await message.answer('Бот - это программа, выполняющая автоматические заранее настроенные повторяющиеся задачи')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Список комманд:\n/start\n/help\n/photo\n/weather")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет я бот!")


@dp.message(Command('weather'))
async def weather(message: Message):
    # Извлечение аргумента после команды "/weather"
    command_parts = message.text.split(maxsplit=1)

    if len(command_parts) > 1:
        city = command_parts[1]  # Город после команды
        weather_info = get_weather(city)
        await message.answer(weather_info)
    else:
        await message.answer("Пожалуйста, укажите город после команды /weather.\nНапример: /weather Москва")
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
