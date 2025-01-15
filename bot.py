import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiohttp import web
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка токена из .env файла
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    logger.error("Токен бота не найден. Убедитесь, что он указан в .env файле.")
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
    try:
        # Предполагается, что функция start_battle принимает player_id и возвращает результат
        from battle import start_battle
        result = start_battle(player_id=message.from_user.id)
        await message.reply(result)
    except Exception as e:
        logger.error(f"Ошибка в обработке команды /battle: {e}")
        await message.reply("Произошла ошибка во время PvP-сражения.")

# Функция для настройки вебхуков
async def on_startup(dp):
    webhook_url = "https://yourdomain.com/webhook"  # Замените на ваш домен и путь
    await bot.set_webhook(webhook_url)

# Создание веб-сервера для обработки обновлений через вебхуки
app = web.Application()
app.router.add_post('/webhook', dp._process_update)

# Запуск бота через вебхуки
if __name__ == '__main__':
    logger.info("Бот запускается...")
    web.run_app(app, host='0.0.0.0', port=8080)





