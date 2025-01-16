import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv
from inventory import Weapon, Armor, Inventory

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBAPP_HOST = "0.0.0.0"  # Хост для запуска
WEBAPP_PORT = int(os.getenv("PORT", 10000))  # Порт для запуска

# Проверка наличия обязательных переменных
if not BOT_TOKEN or not WEBHOOK_URL:
    print("Токен бота или URL вебхука не указаны. Проверьте .env файл.")
    exit(1)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Пример оружия и брони
weapons = [
    Weapon(name="Пистолет", damage=20, cost=100, weapon_type="Пистолет"),
    Weapon(name="Автомат", damage=50, cost=300, weapon_type="Автомат"),
    Weapon(name="Нож", damage=10, cost=50, weapon_type="Нож")
]

armors = [
    Armor(name="Легкий бронежилет", defense=15, cost=200, armor_type="Бронежилет"),
    Armor(name="Тяжелый бронежилет", defense=30, cost=500, armor_type="Бронежилет"),
    Armor(name="Каска", defense=5, cost=100, armor_type="Каска")
]

# Создание инвентаря
inventory = Inventory()

# Хэндлер для команды /start
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.reply("Привет! Готов к PvP-сражениям!")

# Хэндлер для команды /inventory
@dp.message_handler(commands=["inventory"])
async def inventory_handler(message: types.Message):
    items = inventory.show_inventory()
    if items:
        await message.reply("Ваш инвентарь: " + ", ".join(items))
    else:
        await message.reply("Ваш инвентарь пуст!")

# Хэндлер для команды /add_item
@dp.message_handler(commands=["add_item"])
async def add_item_handler(message: types.Message):
    # В данном примере добавляем автомат и бронежилет
    inventory.add_item(weapons[1])
    inventory.add_item(armors[0])
    await message.reply("Предметы добавлены в инвентарь.")

# Хэндлер для команды /remove_item
@dp.message_handler(commands=["remove_item"])
async def remove_item_handler(message: types.Message):
    # Удаляем предмет (в данном примере автомат)
    inventory.remove_item(weapons[1])
    await message.reply("Предмет удален из инвентаря.")

# Хэндлер для команды /battle
@dp.message_handler(commands=["battle"])
async def battle_handler(message: types.Message):
    await message.reply("PvP-сражение пока в разработке!")

# Настройка webhook
async def on_startup(dispatcher):
    print("Установка вебхука...")
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dispatcher):
    print("Удаление вебхука...")
    await bot.delete_webhook()

# Обработчик обновлений с вебхука
async def handle_webhook(request):
    # Получаем тело запроса как JSON
    json_data = await request.json()
    update = types.Update(**json_data)  # Преобразуем в объект Update
    await dp.process_update(update)  # Обрабатываем обновление через Dispatcher
    return web.Response(status=200)

# Настройка веб-приложения
app = web.Application()
app.router.add_post('/webhook', handle_webhook)

if __name__ == "__main__":
    # Настроим вебхук
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # Запускаем приложение
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)

