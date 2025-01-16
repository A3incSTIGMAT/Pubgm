import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Update
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from flask import Flask, request
from dotenv import load_dotenv
from aiohttp import web

# Загрузка переменных окружения из .env
load_dotenv()

# Токен и URL из окружения
API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например, https://your-app.onrender.com/webhook

# Настройка Flask
app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Хэндлер команды /start
@dp.message_handler(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Hello! I'm your bot.")

# Хэндлер для всех остальных сообщений
@dp.message_handler()
async def echo_handler(message: types.Message):
    await message.answer(f"Echo: {message.text}")

# Вебхук обработчик для Flask
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = Update.parse_raw(json_str)
    try:
        # Обработка обновления через aiogram
        dp.feed_update(bot, update)
    except Exception as e:
        logger.error(f"Error processing update: {e}")
    return 'OK'

# Функция запуска вебхука
async def on_startup():
    try:
        await bot.set_webhook(WEBHOOK_URL)
        logger.info(f"Webhook set: {WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        raise

# Функция остановки вебхука
async def on_shutdown():
    try:
        await bot.delete_webhook()
        logger.info("Webhook deleted.")
    except Exception as e:
        logger.error(f"Error deleting webhook: {e}")

# Основной блок запуска
if __name__ == '__main__':
    # Настройка перед запуском Flask
    import asyncio
    asyncio.run(on_startup())
    
    try:
        app.run(host="0.0.0.0", port=5000, debug=False)
    finally:
        asyncio.run(on_shutdown())










































