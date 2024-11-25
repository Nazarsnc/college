# game_logic.py
import random
from game_entities import FireDragon, IceDragon, PoisonDragon, Chest

def random_encounter():
    """Функція для визначення випадкової події після вибору шляху"""
    encounters = [None, FireDragon(), IceDragon(), PoisonDragon(), Chest()]  # Випадкові варіанти
    return random.choice(encounters)  # Повертаємо випадковий елемент

def remove_buttons(chat_id, message_id):
    """
    Видаляє кнопки зі старого повідомлення, роблячи їх неактивними.
    """
    try:
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)
    except Exception as e:
        logging.warning(f"Не вдалося видалити кнопки в повідомленні {message_id}: {str(e)}")