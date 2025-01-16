import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils import executor
from dotenv import load_dotenv
from flask import Flask, request

# Загружаем переменные из .env файла
load_dotenv()

# Токен и URL из переменных окружения
API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Инициализация Flask и бота
app = Flask(__name__)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Команда /start
@dp.message_handler(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hello! I'm your bot.")

# Обработчик для всех других сообщений
@dp.message_handler()
async def echo(message: Message):
    await message.answer(f"Echo: {message.text}")

# Вебхук для Flask
@app.route('/webhook', methods=['POST'])
async def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, bot)
    await dp.process_update(update)
    return 'OK'

# Запуск бота с вебхуками
async def on_start():
    try:
        # Настройка webhook
        await bot.set_webhook(WEBHOOK_URL)
        logger.info(f"Webhook set to: {WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        raise

# Основной блок
if __name__ == '__main__':
    from aiogram import executor
    loop = executor.start_polling(dp, skip_updates=True)

    # Для Flask запускаем сервер отдельно
    app.run(host="0.0.0.0", port=5000, debug=False)









































