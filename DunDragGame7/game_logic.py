# game_logic.py
import telebot
from telebot import types
import random
from game_entities import FireDragon, IceDragon, PoisonDragon, Chest
import logging
def random_encounter():
    """Функція для визначення випадкової події після вибору шляху"""
    encounters = [None, FireDragon(), IceDragon(), PoisonDragon(), Chest()]  # Випадкові варіанти
    return random.choice(encounters)  # Повертаємо випадковий елемент

def random_encounter():
    encounters = [FireDragon(), IceDragon(), PoisonDragon(), Chest()]
    return random.choice(encounters)


