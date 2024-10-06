import asyncio
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
from config import TOKEN, OPENWEATHER_API_KEY
from gtts import gTTS
from googletrans import Translator
import os
import random


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('audio'))
async def audio(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_audio')
    audio = FSInputFile('Суздальская Ночь.mp3')
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command('history'))
async def history(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_voice')
    history_list = [
        "Чем уникален Суздаль? В городе сохранились многочисленные памятники архитектуры, которые позволяют ощутить дух средневековой Руси. Здесь можно посетить Суздальский кремль, Спасо-Евфимиев монастырь, Покровский монастырь, а также храмы и объекты культурного наследия, каждый из которых имеет свою уникальную историю.",
        "Почему город Суздаль так назвали? Так, впервые город упоминается как Суждаль в Лаврентьевской летописи 1024 года, что могло обозначать (основатель судил быть тут городу). Если предположить греческое происхождение, то (Суз дулус) в переводу с греческого означает (раб твой).",
        "Когда и кем был основан город Суздаль? Первое упоминание Суздаля в летописях происходит в 1024 году из-за восстания волхвов. Согласно (Повести временных лет), крестьяне взбунтовались из-за неурожайного года, вызванного засухой. Чуть позже Суздаль становится вотчиной Владимира Мономаха, который уделяет колоссальное внимание усилению и укреплению города."
    ]
    rand_his = random.choice(history_list)
    await message.answer(f'Это история города Суздаль: {rand_his}')

    tts = gTTS(text=rand_his, lang='ru')
    tts.save("history.ogg")
    audio = FSInputFile('history.ogg')
    await bot.send_voice(message.chat.id, audio)
    os.remove("history.ogg")


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

@dp.message(F.photo)
async def react_photo(message: Message):
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')



@dp.message(F.text == "Что такое бот?")
async def bottext(message: Message):
    await message.answer('Бот - это программа, выполняющая автоматические заранее настроенные повторяющиеся задачи')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Список комманд: \n /start \n /help \n /photo \n /weather \n /audio \n /history")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет {message.from_user.first_name}! я бот про красивый город Суздаль")


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


translator = Translator()
# Обработка обычных текстовых сообщений, не являющихся командами
@dp.message()
async def translate(message: Message):
    # Проверяем, если это не команда (не начинается с '/')
    if not message.text.startswith('/'):
        translated = translator.translate(message.text, src='ru', dest='en')  # Переводим с русского на английский
        await message.answer(translated.text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
