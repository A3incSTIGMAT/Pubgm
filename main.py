from flask import Flask
from threading import Thread
import os
import subprocess
import time
import requests
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Проверка, загружается ли токен
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    print("Ошибка: Токен не найден! Проверьте переменную окружения в .env файле.")
    exit(1)
else:
    print(f"Токен успешно загружен: {TOKEN[:5]}...")  # Показывает первые 5 символов токена

# Flask-приложение для поддержания активности
app = Flask('')

@app.route('/')
def home():
    return "Бот работает!"

def run():
    app.run(host='0.0.0.0', port=8080)  # Убрано debug=True для минимизации логов

def keep_alive():
    t = Thread(target=run)
    t.start()

# Ссылка на ваш репозиторий GitHub
GITHUB_REPO_URL = "https://github.com/A3incSTIGMAT/Pubgm"  # Замените на ваш реальный репозиторий
BOT_DIRECTORY = "bot_code"

def clone_or_pull_repo():
    """
    Клонирует репозиторий, если папка не существует,
    либо обновляет его при наличии.
    """
    try:
        if not os.path.exists(BOT_DIRECTORY):
            print("Клонирование репозитория...")
            subprocess.run(["git", "clone", GITHUB_REPO_URL, BOT_DIRECTORY], check=True)
        else:
            print("Обновление репозитория...")
            subprocess.run(["git", "-C", BOT_DIRECTORY, "pull"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при работе с Git: {e}")
        exit(1)

def install_dependencies():
    """
    Устанавливает зависимости из requirements.txt.
    """
    try:
        print("Установка зависимостей...")
        requirements_path = os.path.join(BOT_DIRECTORY, "requirements.txt")
        if os.path.exists(requirements_path):
            subprocess.run(["pip", "install", "-r", requirements_path], check=True)
        else:
            print("Файл requirements.txt не найден, пропускаем установку зависимостей.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при установке зависимостей: {e}")
        exit(1)

def run_bot():
    """
    Запускает основное приложение бота.
    """
    try:
        print("Запуск бота...")
        bot_script_path = os.path.join(BOT_DIRECTORY, "bot.py")
        if os.path.exists(bot_script_path):
            subprocess.run(["python", bot_script_path], check=True)
        else:
            print("Файл bot.py не найден, убедитесь, что репозиторий настроен правильно.")
            exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при запуске бота: {e}")
        exit(1)

if __name__ == "__main__":
    try:
        # Поддержание активности через Flask
        keep_alive()

        # Клонирование репозитория и установка зависимостей
        clone_or_pull_repo()
        install_dependencies()

        # Запуск бота
        run_bot()

    except Exception as e:
        print(f"Общая ошибка: {e}")
        exit(1)

    # Проверка работы Telegram API с вашим токеном
    if TOKEN:
        url = f"https://api.telegram.org/bot{TOKEN}/getMe"
        try:
            response = requests.get(url)
            print(f"Ответ от Telegram API: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при обращении к Telegram API: {e}")

