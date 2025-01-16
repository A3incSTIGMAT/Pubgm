from aiogram import types
from aiogram.dispatcher import Dispatcher

# Хэндлер для команды /start
async def start_handler(message: types.Message):
    await message.reply("Добро пожаловать! Для начала взаимодействия с ботом, напишите /help.")

# Хэндлер для команды /help
async def help_handler(message: types.Message):
    help_text = (
        "/start - Начать игру или взаимодействие с ботом\n"
        "/help - Список всех команд\n"
        "/rules - Правила игры\n"
        "/about - О боте\n"
        "/battle - Вызвать игрока на PvP\n"
        "/accept - Принять вызов\n"
        "/attack - Атаковать соперника\n"
        "/defend - Защититься от атаки\n"
        "/exit - Выйти из текущей игры\n"
        "/profile - Ваш профиль\n"
        "/stats - Статистика игрока\n"
        "/leaderboard - Таблица лидеров\n"
        "/health - Узнать текущее здоровье\n"
        "/shop - Открыть магазин\n"
        "/buy - Купить предмет\n"
        "/sell - Продать предмет\n"
        "/inventory - Ваш инвентарь\n"
        "/equip - Экипировать предмет\n"
        "/unequip - Снять предмет\n"
        "/balance - Проверить баланс\n"
        "/daily - Получить ежедневный бонус\n"
        "/upgrade - Улучшить оружие или броню\n"
        "/addcoins - Добавить монеты (только для админов)\n"
        "/resetstats - Сбросить статистику игрока"
    )
    await message.reply(help_text)

# Хэндлер для команды /rules
async def rules_handler(message: types.Message):
    rules_text = (
        "Правила игры:\n"
        "1. Взаимодействуйте с ботом, используя команды.\n"
        "2. Используйте /battle для вызова другого игрока на PvP.\n"
        "3. Улучшайте свои предметы через /upgrade и используйте /shop для покупок.\n"
        "4. Получайте ежедневные бонусы через /daily и проверяйте свой профиль с помощью /profile."
    )
    await message.reply(rules_text)

# Хэндлер для команды /about
async def about_handler(message: types.Message):
    about_text = (
        "Этот бот предназначен для организации PvP-сражений, торговли и улучшений предметов.\n"
        "Используйте команды для взаимодействия и улучшения своего персонажа."
    )
    await message.reply(about_text)

# Хэндлер для команды /battle
async def battle_handler(message: types.Message):
    await message.reply("Вы вызвали игрока на PvP-сражение! Ожидайте ответа.")

# Хэндлер для команды /accept
async def accept_handler(message: types.Message):
    await message.reply("Вы приняли вызов на PvP-сражение!")

# Хэндлер для команды /attack
async def attack_handler(message: types.Message):
    await message.reply("Вы атаковали соперника!")

# Хэндлер для команды /defend
async def defend_handler(message: types.Message):
    await message.reply("Вы защищаетесь от атаки!")

# Хэндлер для команды /exit
async def exit_handler(message: types.Message):
    await message.reply("Вы вышли из текущей игры.")

# Хэндлер для команды /profile
async def profile_handler(message: types.Message):
    await message.reply("Это ваш профиль.")

# Хэндлер для команды /stats
async def stats_handler(message: types.Message):
    await message.reply("Статистика вашего персонажа.")

# Хэндлер для команды /leaderboard
async def leaderboard_handler(message: types.Message):
    await message.reply("Таблица лидеров.")

# Хэндлер для команды /health
async def health_handler(message: types.Message):
    await message.reply("Текущее здоровье вашего персонажа.")

# Хэндлер для команды /shop
async def shop_handler(message: types.Message):
    await message.reply("Добро пожаловать в магазин! Вы можете купить предметы.")

# Хэндлер для команды /buy
async def buy_handler(message: types.Message):
    await message.reply("Вы купили предмет!")

# Хэндлер для команды /sell
async def sell_handler(message: types.Message):
    await message.reply("Вы продали предмет!")

# Хэндлер для команды /inventory
async def inventory_handler(message: types.Message):
    await message.reply("Ваш инвентарь.")

# Хэндлер для команды /equip
async def equip_handler(message: types.Message):
    await message.reply("Вы экипировали предмет.")

# Хэндлер для команды /unequip
async def unequip_handler(message: types.Message):
    await message.reply("Вы сняли предмет.")

# Хэндлер для команды /balance
async def balance_handler(message: types.Message):
    await message.reply("Ваш текущий баланс.")

# Хэндлер для команды /daily
async def daily_handler(message: types.Message):
    await message.reply("Вы получили ежедневный бонус!")

# Хэндлер для команды /upgrade
async def upgrade_handler(message: types.Message):
    await message.reply("Вы улучшили свое оружие или броню!")

# Хэндлер для команды /addcoins (только для админов)
async def addcoins_handler(message: types.Message):
    # Проверяем, является ли пользователь администратором
    if message.from_user.id == 123456789:  # Здесь укажите ID администратора
        await message.reply("Вы добавили монеты!")
    else:
        await message.reply("У вас нет прав для выполнения этой команды.")

# Хэндлер для команды /resetstats
async def resetstats_handler(message: types.Message):
    await message.reply("Статистика вашего персонажа была сброшена.")

# Регистрируем все хэндлеры
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(help_handler, commands=["help"])
    dp.register_message_handler(rules_handler, commands=["rules"])
    dp.register_message_handler(about_handler, commands=["about"])
    dp.register_message_handler(battle_handler, commands=["battle"])
    dp.register_message_handler(accept_handler, commands=["accept"])
    dp.register_message_handler(attack_handler, commands=["attack"])
    dp.register_message_handler(defend_handler, commands=["defend"])
    dp.register_message_handler(exit_handler, commands=["exit"])
    dp.register_message_handler(profile_handler, commands=["profile"])
    dp.register_message_handler(stats_handler, commands=["stats"])
    dp.register_message_handler(leaderboard_handler, commands=["leaderboard"])
    dp.register_message_handler(health_handler, commands=["health"])
    dp.register_message_handler(shop_handler, commands=["shop"])
    dp.register_message_handler(buy_handler, commands=["buy"])
    dp.register_message_handler(sell_handler, commands=["sell"])
    dp.register_message_handler(inventory_handler, commands=["inventory"])
    dp.register_message_handler(equip_handler, commands=["equip"])
    dp.register_message_handler(unequip_handler, commands=["unequip"])
    dp.register_message_handler(balance_handler, commands=["balance"])
    dp.register_message_handler(daily_handler, commands=["daily"])
    dp.register_message_handler(upgrade_handler, commands=["upgrade"])
    dp.register_message_handler(addcoins_handler, commands=["addcoins"])
    dp.register_message_handler(resetstats_handler, commands=["resetstats"])
