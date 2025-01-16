from flask import Flask
from threading import Thread
import subprocess
import time
import os

# Загрузка переменных окружения
from dotenv import load_dotenv
load_dotenv()

# Инициализация Flask для поддержания работы
app = Flask("")

@app.route('/')
def home():
    return "Бот работает!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Убедитесь, что процесс автоперезапуска работает корректно
def auto_restart():
    while True:
        time.sleep(3600)  # Проверка и перезапуск раз в час
        print("Перезапуск бота...")
        subprocess.run(["python3", "bot.py"])

if __name__ == '__main__':
    keep_alive()
    auto_restart()


