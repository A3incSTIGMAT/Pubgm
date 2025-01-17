import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram import Router
from aiohttp import web
import asyncio
from config import BOT_TOKEN, WEBHOOK_URL
from handlers import router

# Настроим логирование
logging.basicConfig(level=logging.INFO)

# Создаем объект бота с токеном
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# Подключаем обработчики
dp.include_router(router)

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

    # Получаем порт из переменной окружения
    port = int(os.getenv('PORT', 5000))  # Render передает PORT, если работает в облаке

    # Запуск aiohttp приложения
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

    logging.info(f"Web server running on http://0.0.0.0:{port}")

# Основная асинхронная функция для запуска бота и вебхуков
async def main():
    try:
        # Устанавливаем вебхук URL
        webhook_url = WEBHOOK_URL

        # Устанавливаем webhook для бота
        await bot.set_webhook(webhook_url)
        logging.info(f"Webhook установлен: {webhook_url}")

        # Запуск веб-сервера с webhook
        await start_webhook()

        # Бот будет работать до завершения работы приложения
        logging.info("Bot is up and running...")

    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
        raise

if __name__ == '__main__':
    # Запускаем асинхронную функцию main
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Фатальная ошибка: {e}")



