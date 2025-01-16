import logging
import os
from aiogram import Bot, Dispatcher, types
from flask import Flask, request
from dotenv import load_dotenv
import asyncio
from threading import Thread

# Загрузка переменных из .env
load_dotenv()

# Проверка загрузки токена и вебхука
API_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Вывод отладочной информации
print(f"API_TOKEN: {API_TOKEN}")
print(f"WEBHOOK_URL: {WEBHOOK_URL}")

# Проверка, что переменные загружены корректно
if not API_TOKEN:
    raise ValueError("Ошибка: BOT_TOKEN не найден в переменных окружения.")
else:
    print("Токен загружен успешно!")

if not WEBHOOK_URL:
    raise ValueError("Ошибка: WEBHOOK_URL не найден в переменных окружения.")
else:
    print("WEBHOOK_URL загружен успешно!")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

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
async def webhook():
    json_str = await request.get_data()
    update = types.Update.parse_raw(json_str)
    await dp.process_update(update)
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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    # Создаем event loop
    loop = asyncio.get_event_loop()

    # Устанавливаем webhook
    loop.create_task(on_start())  

    # Запуск Flask в отдельном потоке
    thread = Thread(target=run_flask)
    thread.start()

    # Запуск aiogram бота с использованием новой версии
    dp.start_polling()
































