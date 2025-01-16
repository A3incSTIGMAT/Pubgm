import logging
import os
from dotenv import load_dotenv
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Update

# Загрузка переменных окружения из файла .env
load_dotenv()

# Загрузка токена и URL вебхука из переменных окружения
API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например, https://your-app.onrender.com/webhook

# Проверка загрузки токена
if not API_TOKEN:
    raise ValueError("API_TOKEN не найден! Убедитесь, что переменная API_TOKEN настроена правильно.")

if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL не найден! Убедитесь, что переменная WEBHOOK_URL настроена правильно.")

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
    await message.answer("Привет! Я ваш бот!")

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
        logger.error(f"Ошибка обработки обновления: {e}")
    return 'OK'

# Функция запуска вебхука
async def on_startup():
    try:
        await bot.set_webhook(WEBHOOK_URL)
        logger.info(f"Webhook установлен: {WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"Ошибка установки вебхука: {e}")
        raise

# Функция остановки вебхука
async def on_shutdown():
    try:
        await bot.delete_webhook()
        logger.info("Webhook удален.")
    except Exception as e:
        logger.error(f"Ошибка удаления вебхука: {e}")

# Основной блок запуска
if __name__ == '__main__':
    import asyncio

    # Настройка перед запуском Flask
    asyncio.run(on_startup())

    try:
        app.run(host="0.0.0.0", port=5000, debug=False)
    finally:
        asyncio.run(on_shutdown())











































