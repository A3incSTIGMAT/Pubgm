import random

def start_battle(player_id):
    # Простая логика для сражений
    outcomes = ["Ты победил!", "Ты проиграл!", "Ничья!"]
    result = random.choice(outcomes)
    return f"Результат битвы: {result}"
