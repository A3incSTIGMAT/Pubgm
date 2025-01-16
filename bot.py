import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Update
from aiohttp import web
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Переменные окружения
API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например, https://your-app.onrender.com/webhook

# Проверка переменных окружения
if not API_TOKEN:
    raise ValueError("API_TOKEN не найден! Убедитесь, что переменная API_TOKEN настроена правильно.")
if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL не найден! Убедитесь, что переменная WEBHOOK_URL настроена правильно.")

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message_handler(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Я ваш бот! Напиши что-нибудь, и я отвечу.")

# Команда /help
@dp.message_handler(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("Доступные команды:\n/start - Запуск бота\n/help - Справка")

# Эхо-ответ для всех остальных сообщений
@dp.message_handler()
async def echo_handler(message: types.Message):
    await message.answer(f"Echo: {message.text}")

# Обработчик вебхуков
async def handle_webhook(request):
    try:
        data = await request.json()
        update = Update.parse_raw(data)
        await dp.feed_update(bot, update)
    except Exception as e:
        logger.error(f"Ошибка обработки вебхука: {e}")
        return web.Response(text=f"Ошибка: {e}", status=500)
    return web.Response(text="OK", status=200)

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

# Запуск aiohttp-сервера
app = web.Application()
app.router.add_post('/webhook', handle_webhook)

if __name__ == '__main__':
    from aiohttp import web

    # Запуск сервера с обработкой вебхуков
    web.run_app(
        app,
        host="0.0.0.0",  # Слушать все адреса
        port=5000,       # Порт, на котором работает сервер
    )













































