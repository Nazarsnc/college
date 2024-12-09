import random
import telebot
# Клас Герой
class Hero:
    def __init__(self, name, hp=100, strength=225, level=1, exp=0):
        self.name = name
        self.hp = hp
        self.strength = strength
        self.level = level
        self.exp = exp

    def reset_stats(self):
        """Скидає всі характеристики до початкових значень."""
        self.level = 1
        self.hp = 100
        self.strength = 225
        self.exp = 0

    def heal(self, amount):
        self.hp += amount

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:  # Здоров'я не може бути меншим за 0
            self.hp = 0

    def increase_strength(self, amount):
        self.strength += amount

    def gain_exp(self, amount, chat_id=None, bot=None):
        """
        Збільшує досвід героя. Якщо досвід перевищує необхідний для рівня,
        автоматично підвищує рівень до тих пір, поки вистачає досвіду.
        """
        self.exp += amount

        # Цикл для підвищення рівня, поки досвід перевищує поріг
        while self.exp >= self.get_required_exp():
            if chat_id and bot:  # Якщо є чат і бот для повідомлень
                self.exp -= self.get_required_exp()  # Віднімаємо досвід, необхідний для поточного рівня
                self.level_up(chat_id, bot)
            else:
                raise ValueError("Для підвищення рівня потрібно передати chat_id і bot.")

    def get_required_exp(self):
        """
        Обчислює необхідний досвід для наступного рівня.
        Порог досвіду збільшується з кожним рівнем (прогресивно).
        """
        return 100 * (1.2 ** (self.level - 1))  # Прогресивний поріг

    def level_up(self, chat_id, bot):
        """Підвищує рівень героя. Оновлює здоров'я і силу, відправляє повідомлення."""
        self.level += 1
        self.hp += 20  # Додаткове здоров'я за рівень
        self.strength += 5  # Збільшення сили за рівень

        # Повідомлення про підвищення рівня
        bot.send_message(chat_id, f"🎉 Вітаємо! Ваш герой {self.name} підвищив рівень до {self.level}! 🎉\n"
                                  f"Нові характеристики:\n"
                                  f"Здоров'я: {self.hp} HP\n"
                                  f"Сила: {self.strength} ⚔️")

    def __str__(self):
        return f"Ім'я: {self.name}, Рівень: {self.level}, Здоров'я: {self.hp}, Сила: {self.strength}, Досвід: {self.exp}"

# Клас Монстр
class Monster:
    def __init__(self, name, hp, attack, exp):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.exp = exp  # EXP, яке отримає герой за перемогу

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def is_dead(self):
        return self.hp <= 0

# Три види драконів
class FireDragon(Monster):
    def __init__(self):
        super().__init__("Червоний Дракон", hp=150, attack=30, exp=500)

class IceDragon(Monster):
    def __init__(self):
        super().__init__("Синій Дракон", hp=100, attack=15, exp=30)

class PoisonDragon(Monster):
    def __init__(self):
        super().__init__("Зелений Дракон", hp=110, attack=25, exp=40)

# Клас Сундук
class Chest:
    def __init__(self):
        self.item = self.generate_item()  # Генеруємо лише один предмет

    def generate_item(self):
        """Генерує один випадковий предмет або нічого."""
        possible_items = ['Зілля відновлення', 'Зілля шкоди', 'Меч', 'Нічого']
        return random.choice(possible_items)

    def open_chest(self, hero):
        """Взаємодія з героєм при відкритті скрині."""
        if self.item == 'Зілля відновлення':
            heal_amount = 20
            hero.heal(heal_amount)
            return f"{hero.name} використав {self.item} і відновив {heal_amount} здоров'я."
        elif self.item == 'Зілля шкоди':
            hero.take_damage(10)
            return f"{hero.name} використав {self.item}, отримав 10 шкоди."
        elif self.item == 'Меч':
            hero.increase_strength(15)
            return f"{hero.name} знайшов {self.item} і отримав +15 до сили."
        elif self.item == 'Нічого':
            return "Скриня виявилася порожньою."