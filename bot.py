from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.filters import Command
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging
import os

API_TOKEN = os.getenv('API_TOKEN')  # Убедитесь, что переменная окружения API_TOKEN настроена правильно

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Использование фильтра Command
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот.")

# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)











