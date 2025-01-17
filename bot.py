from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiohttp import web
import logging
import os

# Получаем токен и URL вебхука из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
PORT = os.getenv('PORT', 5000)

# Настроим логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем объект бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Я твой бот.")

# Обработчик текстовых сообщений
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text, parse_mode=ParseMode.MARKDOWN)

# Функция для настройки вебхука
async def on_start(request):
    try:
        await bot.set_webhook(WEBHOOK_URL)
        return web.Response(text="Webhook setup successfully!")
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return web.Response(text="Error setting webhook", status=500)

# Запуск вебхука
async def on_webhook(request):
    json_str = await request.json()
    update = types.Update.parse_obj(json_str)
    await dp.process_update(update)
    return web.Response()

# Настройка маршрутов для вебхука
app = web.Application()
app.router.add_get('/', on_start)
app.router.add_post('/webhook', on_webhook)

# Запуск веб-сервера на указанном порту
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=PORT)














