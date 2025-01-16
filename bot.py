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

# Хэндлер для команды /help
@dp.message_handler(commands=["help"])
async def help_handler(message: types.Message):
    help_text = (
        "/start - Начать игру или взаимодействие с ботом\n"
        "/rules - Правила игры\n"
        "/about - О боте\n"
        "/battle - Вызвать игрока на PvP\n"
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
    rules_text = "Правила игры:\n1. Каждый игрок должен вызвать другого на PvP.\n2. Ожидайте атаки и защищайтесь.\n3. Побеждает тот, кто выживет."
    await message.reply(rules_text)

# Хэндлер для команды /about
@dp.message_handler(commands=["about"])
async def about_handler(message: types.Message):
    about_text = "Этот бот предназначен для PvP-сражений в стиле PUBG Mobile. Присоединяйтесь к битвам!"
    await message.reply(about_text)

# Хэндлер для команды /battle
@dp.message_handler(commands=["battle"])
async def battle_handler(message: types.Message):
    await message.reply("PvP-сражение пока в разработке!")

# Хэндлер для команды /accept
@dp.message_handler(commands=["accept"])
async def accept_handler(message: types.Message):
    await message.reply("Вы приняли вызов на PvP-сражение!")

# Хэндлер для команды /attack
@dp.message_handler(commands=["attack"])
async def attack_handler(message: types.Message):
    await message.reply("Вы атаковали соперника!")

# Хэндлер для команды /defend
@dp.message_handler(commands=["defend"])
async def defend_handler(message: types.Message):
    await message.reply("Вы защитились от атаки!")

# Хэндлер для команды /exit
@dp.message_handler(commands=["exit"])
async def exit_handler(message: types.Message):
    await message.reply("Вы вышли из игры.")

# Хэндлер для команды /profile
@dp.message_handler(commands=["profile"])
async def profile_handler(message: types.Message):
    await message.reply("Ваш профиль: Уровень 1, Здоровье 100, Баланс 50 монет.")

# Хэндлер для команды /stats
@dp.message_handler(commands=["stats"])
async def stats_handler(message: types.Message):
    await message.reply("Статистика игрока: Побед 10, Поражений 2.")

# Хэндлер для команды /leaderboard
@dp.message_handler(commands=["leaderboard"])
async def leaderboard_handler(message: types.Message):
    await message.reply("Таблица лидеров: 1. Игрок1 100 очков, 2. Игрок2 90 очков.")

# Хэндлер для команды /health
@dp.message_handler(commands=["health"])
async def health_handler(message: types.Message):
    await message.reply("Ваше текущее здоровье: 100.")

# Хэндлер для команды /shop
@dp.message_handler(commands=["shop"])
async def shop_handler(message: types.Message):
    await message.reply("Магазин открыт: 1. Лечебный набор - 20 монет, 2. Оружие - 50 монет.")

# Хэндлер для команды /buy
@dp.message_handler(commands=["buy"])
async def buy_handler(message: types.Message):
    await message.reply("Вы купили предмет!")

# Хэндлер для команды /sell
@dp.message_handler(commands=["sell"])
async def sell_handler(message: types.Message):
    await message.reply("Вы продали предмет!")

# Хэндлер для команды /inventory
@dp.message_handler(commands=["inventory"])
async def inventory_handler(message: types.Message):
    await message.reply("Ваш инвентарь: Лечебный набор, Пистолет.")

# Хэндлер для команды /equip
@dp.message_handler(commands=["equip"])
async def equip_handler(message: types.Message):
    await message.reply("Вы экипировали пистолет.")

# Хэндлер для команды /unequip
@dp.message_handler(commands=["unequip"])
async def unequip_handler(message: types.Message):
    await message.reply("Вы сняли пистолет.")

# Хэндлер для команды /balance
@dp.message_handler(commands=["balance"])
async def balance_handler(message: types.Message):
    await message.reply("Ваш баланс: 50 монет.")

# Хэндлер для команды /daily
@dp.message_handler(commands=["daily"])
async def daily_handler(message: types.Message):
    await message.reply("Вы получили ежедневный бонус: 10 монет.")

# Хэндлер для команды /upgrade
@dp.message_handler(commands=["upgrade"])
async def upgrade_handler(message: types.Message):
    await message.reply("Вы улучшили оружие!")

# Хэндлер для команды /addcoins
@dp.message_handler(commands=["addcoins"])
async def addcoins_handler(message: types.Message):
    # Только для администраторов
    if message.from_user.id == 123456789:  # Здесь должен быть ID администратора
        await message.reply("Вы добавили монеты!")
    else:
        await message.reply("У вас нет прав для этой команды.")

# Хэндлер для команды /resetstats
@dp.message_handler(commands=["resetstats"])
async def resetstats_handler(message: types.Message):
    # Только для администраторов
    if message.from_user.id == 123456789:  # Здесь должен быть ID администратора
        await message.reply("Статистика игрока сброшена!")
    else:
        await message.reply("У вас нет прав для этой команды.")

# Настройка webhook
async def on_startup(dispatcher):
    logger.info("Установка вебхука...")
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dispatcher):
    logger.info("Удаление вебхука...")
    await bot.delete_webhook()
    await bot.session.close()

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path="/webhook",  # Путь для вебхука
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )







