import logging
import os
import random
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from inventory import Inventory
from models import weapons, armors, items  # Импортируем модели предметов

# Загрузка переменных окружения
load_dotenv()

# Инициализация бота и диспетчера
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Инвентарь игрока
inventory = Inventory()

# Логирование
logging.basicConfig(level=logging.INFO)

# Установка обработчиков команд
@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    await message.reply("Привет! Это игра. Выберите команду.")

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply("Список команд:\n/start - начать игру\n/help - список команд")

@dp.message_handler(commands=['inventory'])
async def show_inventory(message: types.Message):
    items = inventory.show_inventory()
    if items:
        await message.reply(f"Ваш инвентарь: {', '.join(items)}")
    else:
        await message.reply("Ваш инвентарь пуст.")

# Пример периодической задачи - ежедневный бонус
async def daily_bonus():
    print("Выдача ежедневного бонуса!")
    # Логика бонусов (например, добавление монет)

# Основной цикл событий
loop = asyncio.get_event_loop()

# Планировщик задач для выполнения ежедневно
scheduler = AsyncIOScheduler(event_loop=loop)
scheduler.add_job(daily_bonus, IntervalTrigger(hours=24))
scheduler.start()

if __name__ == '__main__':
    from aiogram import executor

    # Убедитесь, что event loop существует
    try:
        loop.run_until_complete(asyncio.sleep(0))
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    # Запуск бота
    executor.start_polling(dp, skip_updates=True)





















