from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup


load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
joke_url = "https://anekdot.mega8.ru/"


async def get_joke(url):
    answer = requests.get(url)
    bs = BeautifulSoup(answer.text, "lxml")
    joke_raw = bs.find('p')
    joke = str(joke_raw)
    joke = joke.replace("<p>", "")
    joke = joke.replace("</p>", "")
    joke = joke.replace("<br/>", "\n")
    return joke


@dp.message_handler(commands=["start"])
async def greeting(message: types.Message):
    await message.answer("Hello!")


@dp.message_handler(commands=["joke"])
async def send_joke(message: types.Message):
    joke = await get_joke(url=joke_url)
    await message.answer(joke)


if __name__ == "__main__":
    executor.start_polling(dp)
