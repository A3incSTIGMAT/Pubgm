import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv
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
    logger.error(f"WEBHOOK_URL должен содержать путь '/webhook'. Текущее значение: {WEBHOOK_URL}")
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

# Хэндлер для обработки вебхуков
async def webhook_handler(request):
    # Получаем данные, отправленные Telegram через вебхук
    json_data = await request.json()
    logger.info(f"Получены данные от Telegram: {json_data}")

    # Получаем обновление от Telegram и передаем его в aiogram
    update = types.Update(**json_data)
    await dp.process_update(update)
    
    # Ответ на вебхук
    return web.Response(status=200)

# Настройка webhook
async def on_startup(dispatcher):
    logger.info("Установка вебхука...")
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dispatcher):
    logger.info("Удаление вебхука...")
    await bot.delete_webhook()
    await bot.session.close()

# Запуск веб-сервера
if __name__ == "__main__":
    # Создание приложения aiohttp
    app = web.Application()
    app.router.add_post("/webhook", webhook_handler)

    # Настройка и запуск вебхука
    start_webhook(
        dispatcher=dp,
        webhook_path="/webhook",  # Путь для вебхука
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

    # Запуск aiohttp сервера на том же порту
    logger.info(f"Запуск веб-сервера на {WEBAPP_HOST}:{WEBAPP_PORT}")
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)




