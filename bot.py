import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 10000))

# Проверка переменных окружения
if not BOT_TOKEN or not WEBHOOK_URL:
    logger.error("BOT_TOKEN или WEBHOOK_URL не настроены. Проверьте файл .env.")
    exit(1)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Клавиатура для удобства
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("/start"),
    KeyboardButton("/help"),
    KeyboardButton("/rules"),
    KeyboardButton("/battle"),
    KeyboardButton("/profile"),
)

# Команды бота
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.reply("Добро пожаловать в игру! Выберите команду для начала.", reply_markup=main_keyboard)

@dp.message_handler(commands=["help"])
async def help_handler(message: types.Message):
    await message.reply(
        "Список всех доступных команд:\n"
        "/start - Начать игру или взаимодействие с ботом\n"
        "/help - Список всех команд\n"
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

@dp.message_handler(commands=["rules"])
async def rules_handler(message: types.Message):
    await message.reply("Правила игры:\n1. Сражайтесь с другими игроками.\n2. Улучшайте своё снаряжение.\n3. Достигайте вершины рейтинга!\nУдачи!")

@dp.message_handler(commands=["about"])
async def about_handler(message: types.Message):
    await message.reply("Этот бот создан для PvP-сражений. Прокачивайте себя, покупайте предметы и побеждайте соперников!")

@dp.message_handler(commands=["battle"])
async def battle_handler(message: types.Message):
    await message.reply("Выберите игрока для вызова на PvP. (В разработке)")

@dp.message_handler(commands=["accept"])
async def accept_handler(message: types.Message):
    await message.reply("Вы приняли вызов! (В разработке)")

@dp.message_handler(commands=["attack"])
async def attack_handler(message: types.Message):
    await message.reply("Вы атаковали соперника! (В разработке)")

@dp.message_handler(commands=["defend"])
async def defend_handler(message: types.Message):
    await message.reply("Вы защитились от атаки! (В разработке)")

@dp.message_handler(commands=["exit"])
async def exit_handler(message: types.Message):
    await message.reply("Вы вышли из текущей игры.")

@dp.message_handler(commands=["profile"])
async def profile_handler(message: types.Message):
    await message.reply(f"Ваш профиль:\nИмя: {message.from_user.username}\nID: {message.from_user.id}")

@dp.message_handler(commands=["stats"])
async def stats_handler(message: types.Message):
    await message.reply("Ваша статистика: Победы - 0, Поражения - 0.")

@dp.message_handler(commands=["leaderboard"])
async def leaderboard_handler(message: types.Message):
    await message.reply("Таблица лидеров: (В разработке)")

@dp.message_handler(commands=["health"])
async def health_handler(message: types.Message):
    await message.reply("Ваше текущее здоровье: 100/100.")

@dp.message_handler(commands=["shop"])
async def shop_handler(message: types.Message):
    await message.reply("Добро пожаловать в магазин! Используйте /buy <номер> для покупки.")

@dp.message_handler(commands=["buy"])
async def buy_handler(message: types.Message):
    await message.reply("Вы купили предмет. (В разработке)")

@dp.message_handler(commands=["sell"])
async def sell_handler(message: types.Message):
    await message.reply("Вы продали предмет. (В разработке)")

@dp.message_handler(commands=["inventory"])
async def inventory_handler(message: types.Message):
    await message.reply("Ваш инвентарь: (В разработке)")

@dp.message_handler(commands=["equip"])
async def equip_handler(message: types.Message):
    await message.reply("Вы экипировали предмет. (В разработке)")

@dp.message_handler(commands=["unequip"])
async def unequip_handler(message: types.Message):
    await message.reply("Вы сняли предмет. (В разработке)")

@dp.message_handler(commands=["balance"])
async def balance_handler(message: types.Message):
    await message.reply("Ваш баланс: 100 монет.")

@dp.message_handler(commands=["daily"])
async def daily_handler(message: types.Message):
    await message.reply("Вы получили ежедневный бонус: 50 монет!")

@dp.message_handler(commands=["upgrade"])
async def upgrade_handler(message: types.Message):
    await message.reply("Вы улучшили своё снаряжение. (В разработке)")

@dp.message_handler(commands=["addcoins"])
async def addcoins_handler(message: types.Message):
    await message.reply("Монеты добавлены. (Только для админов)")

@dp.message_handler(commands=["resetstats"])
async def resetstats_handler(message: types.Message):
    await message.reply("Ваша статистика сброшена.")

# Настройка вебхуков
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
        webhook_path="/webhook",
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )






