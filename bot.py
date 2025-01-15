import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения из .env файла
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Проверка токена
if not BOT_TOKEN:
    logger.error("Токен бота не найден. Убедитесь, что он указан в .env файле.")
    exit(1)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Хэндлер для команды /start
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} вызвал команду /start")
    await message.reply("Привет! Бот работает. Готов к PvP-сражениям?")

# Хэндлер для команды /battle
@dp.message_handler(commands=["battle"])
async def battle_handler(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} вызвал команду /battle")
    try:
        # Предполагается, что функция start_battle принимает player_id и возвращает результат
        from battle import start_battle  # Убедитесь, что файл battle.py существует
        result = start_battle(player_id=message.from_user.id)
        await message.reply(result)
    except ImportError:
        logger.error("Модуль battle не найден. Убедитесь, что файл battle.py существует.")
        await message.reply("Ошибка: PvP-функция временно недоступна.")
    except Exception as e:
        logger.error(f"Ошибка в обработке команды /battle: {e}")
        await message.reply("Произошла ошибка во время PvP-сражения.")

# Хэндлер для тестовой команды /test
@dp.message_handler(commands=["test"])
async def test_handler(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} вызвал команду /test")
    await message.reply("Тестовая команда выполнена успешно!")

# Основной запуск бота
if __name__ == "__main__":
    logger.info("Бот запускается...")
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске бота: {e}")
        exit(1)



