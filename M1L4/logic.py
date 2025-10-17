from random import randint, uniform
import requests


class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = randint(1, 1000)  # Первое поколение
        self.data = self.get_data()

        # Основные свойства
        self.name = self.data["name"].capitalize()
        self.img = self.data["sprites"]["front_default"]
        self.id = self.data["id"]
        self.height = self.data["height"]
        self.weight = self.data["weight"]
        self.types = [t["type"]["name"] for t in self.data["types"]]
        self.abilities = [a["ability"]["name"] for a in self.data["abilities"]]
        self.base_experience = self.data["base_experience"]

        # Дополнительные игровые свойства
        self.level = 1
        self.exp = 0

        # Статы (HP, Attack, Defense и т.п.)
        self.stats = {s["stat"]["name"]: s["base_stat"] for s in self.data["stats"]}

        # ✅ Новый код: случайная суперспособность (Wizard / Fighter / None)
        abilities_list = ["Wizard", "Fighter", None]
        self.super_ability = abilities_list[randint(0, 2)]

        Pokemon.pokemons[pokemon_trainer] = self

    # --- Работа с API ---
    def get_data(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "name": "Pikachu",
                "sprites": {"front_default": "N/A"},
                "id": 25,
                "height": 4,
                "weight": 60,
                "types": [{"type": {"name": "electric"}}],
                "abilities": [{"ability": {"name": "static"}}],
                "base_experience": 112,
                "stats": [{"stat": {"name": "hp"}, "base_stat": 35}],
            }

    # --- Методы для работы с данными ---
    def info(self):
        types = ", ".join(self.types)
        abilities = ", ".join(self.abilities)
        extra = f"\nСуперспособность: {self.super_ability}" if self.super_ability else ""
        return (
            f"Имя: {self.name}\n"
            f"Тип: {types}\n"
            f"Рост: {self.height}\n"
            f"Вес: {self.weight}\n"
            f"Уровень: {self.level}\n"
            f"Опыт: {self.exp}/{self.base_experience}\n"
            f"Способности: {abilities}{extra}"
        )

    def show_img(self):
        return self.img

    def show_stats(self):
        stats_text = "\n".join([f"{k.capitalize()}: {v}" for k, v in self.stats.items()])
        return f"Характеристики покемона {self.name}:\n{stats_text}"

    # --- Методы для изменения свойств ---
    def level_up(self):
        self.level += 1
        self.exp = 0

        for stat_name in self.stats:
            old_value = self.stats[stat_name]
            self.stats[stat_name] = int(old_value * 1.1)  # округляем до целого числа

        return f"{self.name} повысил уровень! Теперь уровень: {self.level}\nВсе характеристики увеличены на 10%!"

    def attack(self, enemy):
        # Этот метод можно оставить как вспомогательный, не удаляю
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer} осталось {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "

    def add_ability(self, ability):
        self.abilities.append(ability)
        return f"Покемону {self.name} добавлена новая способность: {ability}"

    def rename(self, new_name):
        old_name = self.name
        self.name = new_name
        return f"Покемон {old_name} теперь называется {new_name}!"

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.base_experience:
            return self.level_up()
        return f"{self.name} получил {amount} опыта. Всего: {self.exp}/{self.base_experience}"


# ✅ Новый код: функция для сражений
def battle(pokemon1, pokemon2, attacker_name, defender_name):
    """Проводит бой между двумя покемонами"""
    # Берём базовые показатели атаки и защиты
    atk_power = pokemon1.stats.get("attack", 50)
    def_power = pokemon2.stats.get("defense", 50)

    # Бонус за суперспособности
    bonus1 = 1.2 if pokemon1.super_ability == "Fighter" else 1.0
    bonus2 = 1.2 if pokemon2.super_ability == "Wizard" else 1.0

    # Рассчитываем итоговую силу с элементом случайности
    attack_score = (atk_power * pokemon1.level * bonus1) * uniform(0.8, 1.2)
    defend_score = (def_power * pokemon2.level * bonus2) * uniform(0.8, 1.2)

    if attack_score > defend_score:
        winner = attacker_name
        loser = defender_name
        pokemon1.gain_exp(50)
        result = (
            f"🔥 Победитель: @{winner} и его {pokemon1.name}!\n"
            f"💀 Проиграл @{loser} ({pokemon2.name}).\n"
            f"⚔️ Сила атаки: {int(attack_score)} vs {int(defend_score)}"
        )
    elif attack_score < defend_score:
        winner = defender_name
        loser = attacker_name
        pokemon2.gain_exp(50)
        result = (
            f"🏆 Победитель: @{winner} и его {pokemon2.name}!\n"
            f"😢 Проиграл @{loser} ({pokemon1.name}).\n"
            f"⚔️ Сила атаки: {int(attack_score)} vs {int(defend_score)}"
        )
    else:
        result = (
            f"⚖️ Ничья между @{attacker_name} и @{defender_name}! "
            f"Их покемоны оказались равны по силе."
        )

    return result




