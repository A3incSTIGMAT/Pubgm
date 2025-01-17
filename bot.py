import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiohttp import web
import asyncio

# Задаем токен бота через переменную окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден! Убедитесь, что переменная BOT_TOKEN настроена правильно.")

# Настроим бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Простой обработчик команд
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Я бот, и я готов работать!")

# Веб-хендлер для основной страницы
async def on_start(request):
    return web.Response(text="Bot is running!")

# Веб-хендлер для webhook
async def on_webhook(request):
    json_str = await request.json()
    update = types.Update.parse_obj(json_str)
    await dp.process_update(update)
    return web.Response()

# Запуск веб-сервера с aiohttp
async def start_webhook():
    app = web.Application()
    app.router.add_get('/', on_start)
    app.router.add_post('/webhook', on_webhook)

    # Запуск aiohttp приложения
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 5000)
    await site.start()

    print("Web server running on http://0.0.0.0:5000")

# Основная асинхронная функция для запуска бота и вебхуков
async def main():
    try:
        # Устанавливаем webhook
        webhook_url = os.getenv('WEBHOOK_URL', 'https://example.com/webhook')  # Замените на реальный URL
        await bot.set_webhook(webhook_url)

        # Запуск веб-сервера с webhook
        await start_webhook()

        # Бот будет работать до завершения работы приложения
        print("Bot is up and running...")

    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
        raise

if __name__ == '__main__':
    # Запускаем асинхронную функцию main
    asyncio.run(main())
















