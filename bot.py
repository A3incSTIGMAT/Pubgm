import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from battle import start_battle

# Загрузка токена бота из переменных окружения
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("7707583089:AAHOL7IZ96PThIVjQByjW1J7I6cBK2ewNr0")

bot = Bot(token=7707583089:AAHOL7IZ96PThIVjQByjW1J7I6cBK2ewNr0)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.reply("Привет! Готов к PvP-сражениям? Напиши /battle, чтобы начать!")

@dp.message_handler(commands=["battle"])
async def battle_handler(message: types.Message):
    # Логика PvP-сражения
    result = start_battle(player_id=message.from_user.id)
    await message.reply(result)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
