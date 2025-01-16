import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiohttp import web
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Это бот для PvP-сражений!")

# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.reply("Вот список команд:\n/start - Старт\n/help - Справка")

# Настройка вебхука
async def on_start(request):
    return web.Response(text="Bot is running!")

async def on_webhook(request):
    json_str = await request.json()
    update = types.Update.parse_obj(json_str)
    await dp.process_update(update)
    return web.Response(status=200)

# Настройка веб-сервера
app = web.Application()
app.router.add_get('/', on_start)
app.router.add_post('/webhook', on_webhook)

# Установка вебхука
async def on_start_webhook(dp):
    await bot.set_webhook(WEBHOOK_URL)

# Запуск бота и веб-сервера
async def on_start_polling(dp):
    await dp.start_polling()

async def main():
    await on_start_webhook(dp)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()

if __name__ == '__main__':
    from asyncio import run
    run(main())






































