import os

# Указываем токен бота и вебхук URL
# Если вы хотите использовать их напрямую, замените os.getenv(...) на строковые значения
BOT_TOKEN = os.getenv('BOT_TOKEN', 'ваш_токен_бота')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://pubgm-it8l.onrender.com/webhook')

# Проверяем, что токен и вебхук URL заданы
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден! Убедитесь, что переменная BOT_TOKEN настроена правильно.")

if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL не найден! Убедитесь, что переменная WEBHOOK_URL настроена правильно.")

# Вывод для проверки
print(f"BOT_TOKEN: {BOT_TOKEN[:5]}*** (токен скрыт)")
print(f"WEBHOOK_URL: {WEBHOOK_URL}")
