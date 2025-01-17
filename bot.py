import os
import logging
from aiogram import Bot, Dispatcher, types
from aiohttp import web
import asyncio

# Устанавливаем логирование
logging.basicConfig(level=logging.INFO)

# Задаем токен бота через переменную окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    logging.error("BOT_TOKEN не найден! Убедитесь, что переменная BOT_TOKEN настроена правильно.")
    exit(1)  # Если BOT_TOKEN не найден, завершаем работу

# Настроим бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Простой обработчик команд
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Я бот, и я готов работать!")

# Веб-хендлер для основной страницы (проверка состояния бота)
async def on_start(request):
    return web.Response(text="Bot is running!")

# Веб-хендлер для webhook, который будет принимать обновления от Telegram
async def on_webhook(request):
    json_str = await request.json()
    update = types.Update.parse_obj(json_str)
    await dp.process_update(update)  # Передаем обновление в диспетчер
    return web.Response()  # Подтверждаем получение обновления

# Запуск веб-сервера с aiohttp
async def start_webhook():
    app = web.Application()
    app.router.add_get('/', on_start)  # Обработчик главной страницы
    app.router.add_post('/webhook', on_webhook)  # Обработчик для вебхуков

    # Получаем порт из переменной окружения (Render передает PORT, если работает в облаке)
    port = int(os.getenv('PORT', 5000))  # Используем переменную окружения PORT, если она есть

    # Запуск aiohttp приложения
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

    logging.info(f"Web server running on http://0.0.0.0:{port}")

# Основная асинхронная функция для запуска бота и вебхуков
async def main():
    try:
        # Устанавливаем webhook URL из переменной окружения
        webhook_url = os.getenv('WEBHOOK_URL')

        if not webhook_url:
            logging.error("WEBHOOK_URL не найден! Убедитесь, что переменная WEBHOOK_URL настроена правильно.")
            return  # Возвращаем управление без завершения программы
        
        # Устанавливаем webhook для бота (Telegram будет отправлять обновления на этот URL)
        await bot.set_webhook(webhook_url)
        logging.info(f"Webhook установлен: {webhook_url}")

        # Запуск веб-сервера с webhook
        await start_webhook()

        # Бот будет работать до завершения работы приложения
        logging.info("Bot is up and running...")

    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")

if __name__ == '__main__':
    # Запускаем асинхронную функцию main
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Фатальная ошибка: {e}")


















