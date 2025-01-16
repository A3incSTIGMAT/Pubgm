import os
import logging
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from dotenv import load_dotenv
from commands import  # Импортируем команды из файла commands.py

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
    """
    Главная страница Flask-приложения.
    """
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
    Устанавливает Webhook для Telegram.
    """
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook установлен: {WEBHOOK_URL}")


async def on_startup():
    """
    Действия при запуске.
    """
    logging.info("Запуск бота и установка Webhook...")
    await set_webhook()


async def on_shutdown():
    """
    Действия при остановке бота.
    """
    await bot.delete_webhook()
    await bot.session.close()
    logging.info("Webhook удален, бот остановлен.")


# Обработчик всех команд из commands.py
@dp.message_handler(commands=list(COMMANDS.keys()))
async def handle_commands(message: types.Message):
    """
    Обрабатывает команды, указанные в файле commands.py.
    """
    command = message.get_command(pure=True)
    response = COMMANDS.get(command, "Команда не найдена.")
    await message.reply(response)


# Пример команды /start
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    """
    Стартовая команда.
    """
    await message.reply("Привет! Добро пожаловать в игру. Используй /help для списка команд.")


if __name__ == "__main__":
    try:
        # Указание порта для Flask
        port = int(os.getenv("PORT", 8080))  # Порт из переменных окружения
        app.run(host="0.0.0.0", port=port)
    except Exception as e:
        logging.error(f"Ошибка при запуске: {e}")























