import telebot
from telebot import types
import random
from game_entities import Hero, FireDragon, IceDragon, PoisonDragon, Chest, Monster
from game_story import get_intro_text, story_text, nothing_encountered_text, get_encounter_monster_text, \
    get_encounter_chest_text
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO)

API_TOKEN = '7733352163:AAG6r0WvTJO5tBSTAr8i6kWuUyWRTYozlws'
bot = telebot.TeleBot(API_TOKEN)

USER_DATA = {}
USER_MESSAGES = {}

def remove_buttons(chat_id, message_id):
    """
    Видаляє кнопки зі старого повідомлення.
    """
    try:
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)
    except Exception as e:
        logging.warning(f"Не вдалося видалити кнопки в повідомленні {message_id}: {str(e)}")


@bot.message_handler(commands=['start'])
def start(message):

    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Створити героя", callback_data='create_hero')
    keyboard.add(button)
    bot.send_message(message.chat.id, get_intro_text(), reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'create_hero')
def create_hero(call):
    remove_buttons(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "Введіть ім'я вашого героя:")
    USER_MESSAGES[call.message.chat.id] = [msg.message_id]
    bot.register_next_step_handler(msg, receive_name)


@bot.message_handler(commands=['stat', 'стат'])
def show_hero_status(message):
    # Отримуємо героя з даних користувача
    hero = USER_DATA.get(message.chat.id, {}).get('hero')

    if hero:
        # Формуємо динамічне повідомлення зі статусом героя
        status_text = (f"Ім'я героя {hero.name}:\n"
                       f"Рівень: {hero.level}\n"
                       f"Здоров'я: {hero.hp}\n"
                       f"Сила: {hero.strength}\n"
                       f"Досвід: {hero.exp} / {hero.get_required_exp()}\n")

        # Виводимо в чат
        bot.send_message(message.chat.id, status_text)
    else:
        # Якщо герой не створений
        bot.send_message(message.chat.id, "Ваш герой не існує. Створіть героя для перегляду статусу.")


def receive_name(message):
    user_name = message.text
    USER_DATA[message.chat.id] = {'hero': Hero(user_name)}

    hero = USER_DATA[message.chat.id]['hero']
    keyboard = types.InlineKeyboardMarkup()
    start_game_button = types.InlineKeyboardButton("Почати гру", callback_data='start_game')
    keyboard.add(start_game_button)

    msg = bot.send_message(
        message.chat.id,
        f"Ваш герой створений! Ім'я: {hero.name}, Рівень: {hero.level}, Здоров'я: {hero.hp}HP, Сила: {hero.strength}",
        reply_markup=keyboard
    )
    USER_MESSAGES[message.chat.id].append(msg.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'start_game')
def start_game(call):
    remove_buttons(call.message.chat.id, call.message.message_id)

    keyboard = types.InlineKeyboardMarkup()
    left_button = types.InlineKeyboardButton("Піти наліво", callback_data='go_left')
    right_button = types.InlineKeyboardButton("Піти направо", callback_data='go_right')
    keyboard.add(left_button, right_button)

    bot.send_message(call.message.chat.id, story_text(), reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['go_left', 'go_right'])
def choose_path(call):
    remove_buttons(call.message.chat.id, call.message.message_id)
    encounter = random_encounter()

    if encounter is None:
        response_text = nothing_encountered_text()
        keyboard = types.InlineKeyboardMarkup()
        continue_button = types.InlineKeyboardButton("Іти далі", callback_data='continue')
        keyboard.add(continue_button)
        bot.send_message(call.message.chat.id, response_text, reply_markup=keyboard)
    elif isinstance(encounter, Monster):
        response_text = get_encounter_monster_text(encounter)
        bot.send_message(call.message.chat.id, response_text)

        keyboard = types.InlineKeyboardMarkup()
        fight_button = types.InlineKeyboardButton("Бій", callback_data=f'fight_{encounter.name}')
        run_button = types.InlineKeyboardButton("Втекти", callback_data=f'run_{encounter.name}')
        keyboard.add(fight_button, run_button)

        USER_DATA[call.message.chat.id]['monster'] = encounter
        bot.send_message(call.message.chat.id, "Що ви хочете зробити?", reply_markup=keyboard)
    elif isinstance(encounter, Chest):
        response_text = "Ви знайшли скриню! Що ви хочете зробити?"
        keyboard = types.InlineKeyboardMarkup()
        open_button = types.InlineKeyboardButton("Відкрити скриню", callback_data='open_chest')
        continue_button = types.InlineKeyboardButton("Іти далі", callback_data='continue')
        keyboard.add(open_button, continue_button)
        bot.send_message(call.message.chat.id, response_text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'open_chest')
def open_chest(call):
    remove_buttons(call.message.chat.id, call.message.message_id)
    hero = USER_DATA[call.message.chat.id]['hero']
    chest = Chest()  # Створюємо новий об'єкт скрині

    # Отримуємо результат відкриття скрині
    open_chest_response = chest.open_chest(hero)

    # Створюємо кнопку "Іти далі"
    keyboard = types.InlineKeyboardMarkup()
    continue_button = types.InlineKeyboardButton("Іти далі", callback_data='continue')
    keyboard.add(continue_button)

    # Відправляємо повідомлення з результатом і кнопкою
    bot.send_message(call.message.chat.id, open_chest_response, reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: call.data.startswith('fight_'))
def fight_monster(call):
    remove_buttons(call.message.chat.id, call.message.message_id)
    try:
        hero = USER_DATA[call.message.chat.id]['hero']
        monster_name = call.data.split('_')[1]

        # Перевірка наявності монстра
        monster = USER_DATA[call.message.chat.id].get('monster', None)
        if monster is None or monster.name != monster_name:
            bot.send_message(call.message.chat.id, "Вибачте, але ви не можете боротися, бо монстра не знайдено.")
            return

        damage_to_monster = hero.strength
        monster.take_damage(damage_to_monster)
        response_text = f"Ви атакували {monster.name} і завдали {damage_to_monster} шкоди!\n"
        response_text += f"У {monster.name} залишилось {monster.hp} HP.\n"

        if monster.is_dead():
            response_text += f"{monster.name} переможений! Ви отримали {monster.exp} EXP."
            hero.gain_exp(monster.exp, call.message.chat.id, bot)
            keyboard = types.InlineKeyboardMarkup()
            continue_button = types.InlineKeyboardButton("Іти далі", callback_data='continue')
            keyboard.add(continue_button)
            del USER_DATA[call.message.chat.id]['monster']
        else:
            damage_to_hero = monster.attack
            hero.take_damage(damage_to_hero)
            response_text += f"{monster.name} завдає вам {damage_to_hero} шкоди! Ваше здоров'я: {hero.hp} HP."
            if hero.hp <= 0:
                response_text += "\nНа жаль, ви загинули. Гра завершена."
                hero.reset_stats()
                keyboard = types.InlineKeyboardMarkup()
                restart_button = types.InlineKeyboardButton("Почати гру спочатку", callback_data='restart_game')
                keyboard.add(restart_button)
            else:
                keyboard = types.InlineKeyboardMarkup()
                fight_button = types.InlineKeyboardButton("Бій", callback_data=f'fight_{monster.name}')
                run_button = types.InlineKeyboardButton("Втекти", callback_data=f'run_{monster.name}')
                keyboard.add(fight_button, run_button)

        bot.send_message(call.message.chat.id, response_text, reply_markup=keyboard)

    except Exception as e:
        logging.error(f"Error occurred in fight_monster: {str(e)}")
        bot.send_message(call.message.chat.id, "Виникла помилка, спробуйте ще раз.")


@bot.callback_query_handler(func=lambda call: call.data.startswith('run_'))
def run_from_monster(call):
    remove_buttons(call.message.chat.id, call.message.message_id)
    try:
        hero = USER_DATA[call.message.chat.id]['hero']
        monster_name = call.data.split('_')[1]

        # Перевірка наявності монстра
        monster = USER_DATA[call.message.chat.id].get('monster', None)
        if monster is None or monster.name != monster_name:
            bot.send_message(call.message.chat.id, "Вибачте, але ви не можете втекти, бо монстра не знайдено.")
            return

        success = random.choice([True, False])

        if success:
            response_text = f"Вам вдалося втекти від {monster.name}!"
            keyboard = types.InlineKeyboardMarkup()
            continue_button = types.InlineKeyboardButton("Іти далі", callback_data='continue')
            keyboard.add(continue_button)
            del USER_DATA[call.message.chat.id]['monster']
        else:
            response_text = f"Втеча не вдалася! {monster.name} завдає вам {monster.attack} шкоди!"
            hero.take_damage(monster.attack)
            if hero.hp <= 0:
                response_text += "\nНа жаль, ви загинули."
                hero.reset_stats()
                keyboard = types.InlineKeyboardMarkup()
                restart_button = types.InlineKeyboardButton("Почати гру спочатку", callback_data='restart_game')
                keyboard.add(restart_button)
            else:
                keyboard = types.InlineKeyboardMarkup()
                fight_button = types.InlineKeyboardButton("Бій", callback_data=f'fight_{monster.name}')
                run_button = types.InlineKeyboardButton("Втекти", callback_data=f'run_{monster.name}')
                keyboard.add(fight_button, run_button)

        bot.send_message(call.message.chat.id, response_text, reply_markup=keyboard)

    except Exception as e:
        logging.error(f"Error occurred in run_from_monster: {str(e)}")
        bot.send_message(call.message.chat.id, "Виникла помилка, спробуйте ще раз.")


@bot.callback_query_handler(func=lambda call: call.data == 'continue')
def continue_adventure(call):
    choose_path(call)


@bot.callback_query_handler(func=lambda call: call.data == 'restart_game')
def restart_game(call):
    remove_buttons(call.message.chat.id, call.message.message_id)
    chat_id = call.message.chat.id

    # Очищення даних гравця
    if chat_id in USER_DATA:
        del USER_DATA[chat_id]

    # Виводимо вітання
    intro_text = get_intro_text()
    bot.send_message(chat_id, intro_text)

    # Додаємо кнопку для створення героя
    start_button = types.InlineKeyboardMarkup()
    create_hero_button = types.InlineKeyboardButton("Створити героя", callback_data='create_hero')
    start_button.add(create_hero_button)

    bot.send_message(chat_id, "Натисніть нижче, щоб створити героя.", reply_markup=start_button)

    # Очищення всіх повідомлень у чаті (не працює для повідомлень користувачів)
    # Можна використовувати timeout, щоб зменшити шанс збоїв при видаленні
    for i in range(1, 200):
        try:
            bot.delete_message(chat_id, call.message.message_id - i)
        except Exception:
            break



# Функція для випадкової зустрічі
def random_encounter():
    encounters = [FireDragon(), IceDragon(), PoisonDragon(), Chest()]
    return random.choice(encounters)

if __name__ == '__main__':
    print("Бот запущений...")
    bot.polling(none_stop=True)

