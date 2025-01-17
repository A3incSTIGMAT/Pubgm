import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils.executor import start_webhook
from flask import Flask, request

# Получаем данные из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN', '7707583089:AAHOL7IZ96PThIVjQByjW1J7I6cBK2ewNr0')  # Токен бота
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://pubgm-it8l.onrender.com/webhook')  # URL для webhook
PORT = int(os.getenv('PORT', 5000))  # Порт для Flask

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Flask сервер для обработки webhook запросов
app = Flask(__name__)

# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def cmd_start(msg: types.Message):
    await msg.answer("Hello! I'm your bot!")

# Функция для запуска вебхука
async def on_start(msg: types.Message):
    await msg.answer("Webhook has been set up!")

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data(as_text=True)
    update = types.Update.parse_raw(json_str)
    dp.process_update(update)  # Отправляем обновление в aiogram
    return 'OK'

# Устанавливаем webhook
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)  # Устанавливаем вебхук

# Остановка бота
async def on_shutdown(dp):
    await bot.close()

# Основная функция для запуска бота и вебхуков
if __name__ == '__main__':
    from aiogram.utils import executor
    app.run(host="0.0.0.0", port=PORT)  # Запуск Flask сервера
    executor.start_polling(dp, on_shutdown=on_shutdown)













