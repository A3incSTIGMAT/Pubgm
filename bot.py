from aiogram import Bot, Dispatcher, types
import logging
import os
from aiohttp import web
from aiogram.types import ParseMode

API_TOKEN = os.getenv('API_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Вебхук для обработки сообщений
async def on_message(request):
    payload = await request.json()
    update = types.Update(**payload)
    await dp.process_update(update)
    return web.Response()

# Настройка маршрутов
app = web.Application()
app.router.add_post(f'/{API_TOKEN}', on_message)

# Запуск веб-сервера
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)












