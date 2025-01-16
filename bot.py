import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.filters import Command

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Ваш токен API
API_TOKEN = 'YOUR_BOT_TOKEN'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработчик для команды "/start"
@dp.message_handler(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hello! I'm your bot.")

# Обработчик для других сообщений
@dp.message_handler()
async def echo(message: Message):
    await message.answer(f"Echo: {message.text}")

# Запуск бота
if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)








































