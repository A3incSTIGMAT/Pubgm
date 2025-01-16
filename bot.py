import logging
import os
from aiogram import Bot, Dispatcher, types
from flask import Flask, request
from dotenv import load_dotenv
from aiogram.utils import executor
import asyncio
from threading import Thread

# Загрузка переменных из .env
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Установим логирование
logging.basicConfig(level=logging.INFO)

# Хэндлеры команд
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Это бот для PvP-сражений!", parse_mode="HTML")

@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    await message.answer("Вот список команд:\n/start - Старт\n/help - Справка", parse_mode="HTML")

@dp.message_handler(commands=["battle"])
async def cmd_battle(message: types.Message):
    await message.answer("Вы вызвали игрока на PvP-сражение!", parse_mode="HTML")

# Настройка Flask сервера
app = Flask(__name__)

# Вебхук для приема обновлений от Telegram
@app.route('/webhook', methods=["POST"])
def webhook():
    json_str = request.get_data(as_text=True)
    update = types.Update.parse_raw(json_str)
    asyncio.run(dp.process_update(update))  # Обработка обновлений в асинхронном режиме
    return "OK"

# Установка вебхука
async def set_webhook():
    webhook_url = f"{WEBHOOK_URL}/webhook"
    await bot.set_webhook(webhook_url)

# Ожидание получения обновлений с Telegram
async def on_start():
    await set_webhook()
    print("Webhook установлен")

# Запуск Flask в отдельном потоке
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(on_start())  # Устанавливаем webhook
    # Запуск Flask в отдельном потоке
    thread = Thread(target=run_flask)
    thread.start()

    # Запуск aiogram бота с использованием executor для асинхронной работы
    executor.start_polling(dp, skip_updates=True)





























