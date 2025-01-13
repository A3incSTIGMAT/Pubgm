import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка токена из .env файла
load_dotenv()
BOT_TOKEN = os.getenv("7707583089:AAHOL7IZ96PThIVjQByjW1J7I6cBK2ewNr0")

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

# Запуск бота
if __name__ == "__main__":
    logger.info("Бот запускается...")
    executor.start_polling(dp, skip_updates=True)


