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

# Функция для обработки обновлений через вебхук
async def on_startup(dp):
    webhook_url = "https://yourdomain.com/webhook"  # Замените на ваш домен и путь
    await bot.set_webhook(webhook_url)

# Обработка POST-запроса на вебхук
async def webhook_handler(request):
    json_str = await request.json()
    update = types.Update(**json_str)
    await dp.process_update(update)
    return web.Response()

# Создание веб-сервера для обработки обновлений через вебхуки
app = web.Application()
app.router.add_post('/webhook', webhook_handler)

# Запуск бота через вебхуки
async def on_start():
    logger.info("Бот запускается...")
    await on_startup(dp)
    await web.run_app(app, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    # Убедитесь, что используете правильные аргументы и синхронизируйте запуск
    executor.start_polling(dp, skip_updates=True)







