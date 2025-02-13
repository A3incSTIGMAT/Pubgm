from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

# Создаем роутер
router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    """Обработчик команды /start"""
    await msg.answer("Привет! Я помогу тебе узнать твой ID, просто отправь мне любое сообщение")

@router.message()
async def message_handler(msg: Message):
    """Обработчик всех сообщений"""
    await msg.answer(f"Твой ID: {msg.from_user.id}")
