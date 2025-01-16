import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv
import aiohttp
from aiohttp import web

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBAPP_HOST = "0.0.0.0"  # Хост для запуска
WEBAPP_PORT = int(os.getenv("PORT", 10000))  # Порт для запуска

# Проверяем наличие обязательных переменных
if not BOT_TOKEN or not WEBHOOK_URL:
    logger.error("Токен бота или URL вебхука не указаны. Проверьте .env файл.")
    exit(1)

# Проверка правильности URL вебхука
if not WEBHOOK_URL.endswith("/webhook"):
    logger.error(f"WEBHOOK_URL должен заканчиваться на '/webhook'. Текущее значение: {WEBHOOK_URL}")
    exit(1)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Хэндлер для команды /start
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.reply("Привет! Готов к PvP-сражениям!")

# Хэндлер для команды /battle
@dp.message_handler(commands=["battle"])
async def battle_handler(message: types.Message):
    await message.reply("PvP-сражение пока в разработке!")

# Добавляем обработчик для корневого пути "/"
async def handle_root(request):
    return web.Response(text="OK")

# Настройка webhook
async def on_startup(dispatcher):
    logger.info("Установка вебхука...")
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dispatcher):
    logger.info("Удаление вебхука...")
    await bot.delete_webhook()

# Добавляем маршрут для проверки
app = web.Application()
app.router.add_get('/', handle_root)

# Основная настройка вебхука
async def init_webhook():
    # Устанавливаем вебхук
    webhook_path = "/webhook"
    app.router.add_post(webhook_path, dp.process_update)  # Обработка обновлений через dp.process_update

    return app

if __name__ == "__main__":
    app = web.Application()

    # Добавляем обработку /webhook
    app.router.add_post('/webhook', dp.process_update)  # Обработка обновлений

    # Добавляем обработчик для корня (для проверки)
    app.router.add_get('/', handle_root)

    # Настроим вебхук
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # Запускаем приложение
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)















