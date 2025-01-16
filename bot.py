import os
from dotenv import load_dotenv

# Загрузка .env для локальной разработки (на Render не требуется)
load_dotenv()

# Загрузка переменных окружения
API_TOKEN = os.getenv("API_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Проверка переменных окружения
if not API_TOKEN:
    print("API_TOKEN не найден!")
    raise ValueError("API_TOKEN не найден! Убедитесь, что переменная API_TOKEN настроена правильно.")
else:
    print(f"Loaded API_TOKEN: {API_TOKEN}")

if not WEBHOOK_URL:
    print("WEBHOOK_URL не найден!")
    raise ValueError("WEBHOOK_URL не найден! Убедитесь, что переменная WEBHOOK_URL настроена правильно.")
else:
    print(f"Loaded WEBHOOK_URL: {WEBHOOK_URL}")












































