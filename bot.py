import os
import logging
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from dotenv import load_dotenv
from commands import COMMANDS  # Импортируем команды из файла commands.py

# Загрузка переменных окружения
load_dotenv()

# Конфигурация бота
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_URL")  # URL вашего хостинга
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Flask-приложение
app = Flask(__name__)

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@app.route("/")
def home():
    return "Бот работает!"


@app.route(WEBHOOK_PATH, methods=["POST"])
async def handle_webhook():
    """
    Обработка обновлений, полученных через Webhook.
    """
    update = Update(**request.json)
    await dp.process_update(update)
    return "ok", 200


async def set_webhook():
    """
    Устанавливаем Webhook для Telegram.
    """
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook установлен: {WEBHOOK_URL}")


async def on_startup():
    """
    Действия при запуске.
    """
    await set_webhook()


async def on_shutdown():
    """
    Д






















