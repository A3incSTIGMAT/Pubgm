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

# Хэндлер для команды /help
@dp.message_handler(commands=["help"])
async def help_handler(message: types.Message):
    help_text = (
        "/start - Начать игру или взаимодействие с ботом\n"
        "/battle - Вызвать игрока на PvP\n"
        "/help - Список всех команд\n"
        "/rules - Правила игры\n"
        "/about - О боте\n"
        "/accept - Принять вызов\n"
        "/attack - Атаковать соперника\n"
        "/defend - Защититься от атаки\n"
        "/exit - Выйти из текущей игры\n"
        "/profile - Ваш профиль\n"
        "/stats - Статистика игрока\n"
        "/leaderboard - Таблица лидеров\n"
        "/health - Узнать текущее здоровье\n"
        "/shop - Открыть магазин\n"
        "/buy - Купить предмет\n"
        "/sell - Продать предмет\n"
        "/inventory - Ваш инвентарь\n"
        "/equip - Экипировать предмет\n"
        "/unequip - Снять предмет\n"
        "/balance - Проверить баланс\n"
        "/daily - Получить ежедневный бонус\n"
        "/upgrade - Улучшить оружие или броню\n"
        "/addcoins - Добавить монеты (только для админов)\n"
        "/resetstats - Сбросить статистику игрока"
    )
    await message.reply(help_text)

# Хэндлер для команды /rules
@dp.message_handler(commands=["rules"])
async def rules_handler(message: types.Message):
    await message.reply("Правила игры: Взаимодействуйте с ботом, сражайтесь с другими игроками и улучшайте свои характеристики!")

# Хэндлер для команды /about
@dp.message_handler(commands=["about"])
async def about_handler(message: types.Message):
    await message.reply("Бот для PvP-сражений в стиле PUBG Mobile!")

# Настройка webhook
async def on_startup(dispatcher):
    logger.info("Установка вебхука...")
    try:
        # Настройка вебхука
        await bot.set_webhook(WEBHOOK_URL)
    except Exception as e:
        logger.error(f"Ошибка при установке вебхука: {e}")
        exit(1)

async def on_shutdown(dispatcher):
    logger.info("Удаление вебхука...")
    await bot.delete_webhook()
    # Получаем сессию и закрываем её корректно
    session = await bot.get_session()
    await session.close()

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path="/webhook",  # Путь для вебхука
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )









