import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv

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
if not BOT_TOKEN:
    logger.error("Токен бота не указан. Проверьте .env файл.")
    exit(1)
if not WEBHOOK_URL:
    logger.error("URL вебхука не указан. Проверьте .env файл.")
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

# Настройка webhook
async def on_startup(dispatcher):
    logger.info("Установка вебхука...")
    try:
        await bot.set_webhook(WEBHOOK_URL)
        logger.info("Вебхук успешно установлен!")
    except Exception as e:
        logger.error(f"Ошибка установки вебхука: {e}")
        exit(1)

async def on_shutdown(dispatcher):
    logger.info("Удаление вебхука...")
    try:
        await bot.delete_webhook()
        await bot.session.close()
        logger.info("Вебхук успешно удалён.")
    except Exception as e:
        logger.error(f"Ошибка удаления вебхука: {e}")

if __name__ == "__main__":
    # Проверяем, что WEBHOOK_URL заканчивается на "/webhook"
    if not WEBHOOK_URL.endswith("/webhook"):
        logger.error("WEBHOOK_URL должен содержать путь '/webhook'. Проверьте .env файл.")
        exit(1)

    # Запуск вебхука
    start_webhook(
        dispatcher=dp,
        webhook_path="/webhook",  # Совпадает с указанным в WEBHOOK_URL
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )


