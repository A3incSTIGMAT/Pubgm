import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.exceptions import TelegramAPIError
from aiohttp import web
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка токена и URL вебхука из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = "/webhook"
PORT = int(os.getenv("PORT", 10000))

if not BOT_TOKEN:
    logger.error("Токен бота не найден. Убедитесь, что он указан в .env файле.")
    exit(1)

if not WEBHOOK_URL:
    logger.error("URL вебхука не указан. Убедитесь, что он указан в .env файле.")
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
        # Импорт функции сражения (имитация для примера)
        from battle import start_battle
        result = start_battle(player_id=message.from_user.id)  # Здесь вызов вашей логики
        await message.reply(result)
    except Exception as e:
        logger.error(f"Ошибка в обработке команды /battle: {e}")
        await message.reply("Произошла ошибка во время PvP-сражения.")

# Установка вебхука при запуске
async def on_startup(app):
    try:
        await bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)
        logger.info(f"Webhook успешно установлен: {WEBHOOK_URL + WEBHOOK_PATH}")
    except TelegramAPIError as e:
        logger.error(f"Ошибка при установке вебхука: {e}")
        exit(1)

# Удаление вебхука при завершении
async def on_shutdown(app):
    await bot.delete_webhook()
    logger.info("Webhook удалён.")

# Обработка POST-запросов на вебхук
async def webhook_handler(request):
    try:
        json_data = await request.json()
        update = types.Update(**json_data)
        await dp.process_update(update)
        return web.Response(status=200)
    except Exception as e:
        logger.error(f"Ошибка при обработке вебхука: {e}")
        return web.Response(status=500)

# Обработка запроса на корневой маршрут (необязательно)
async def index_handler(request):
    return web.Response(text="Бот работает! Используйте Telegram для взаимодействия.")

# Настройка маршрутов приложения
app = web.Application()
app.router.add_post(WEBHOOK_PATH, webhook_handler)
app.router.add_get("/", index_handler)

# Подключение хуков старта и завершения
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

# Запуск приложения
if __name__ == "__main__":
    logger.info(f"Запуск веб-сервера на порту {PORT}...")
    web.run_app(app, host="0.0.0.0", port=PORT)
