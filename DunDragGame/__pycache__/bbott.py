import telebot
from telebot import types
import random
from game_entities import Hero, FireDragon, IceDragon, PoisonDragon, Chest, Monster

# Введіть ваш токен бота
API_TOKEN = '7733352163:AAG6r0WvTJO5tBSTAr8i6kWuUyWRTYozlws'
bot = telebot.TeleBot(API_TOKEN)

# Стан бота
USER_DATA = {}
USER_MESSAGES = {}  # Зберігатимемо ID повідомлень для кожного користувача


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Створити героя", callback_data='create_hero')
    keyboard.add(button)

    bot.send_message(message.chat.id, 'Вітаю у грі Підземелля та Дракони! Натисніть кнопку нижче, щоб створити героя.',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'create_hero')
def create_hero(call):
    # Деактивуємо кнопку "Створити героя"
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

    msg = bot.send_message(call.message.chat.id, "Введіть ім'я вашого героя:")
    USER_MESSAGES[call.message.chat.id] = [msg.message_id]  # Зберігаємо ID повідомлення
    bot.register_next_step_handler(msg, receive_name)


def receive_name(message):
    user_name = message.text
    USER_DATA[message.chat.id] = {'hero': Hero(user_name)}  # Зберігаємо героя у словнику

    # Створюємо кнопку для початку гри
    keyboard = types.InlineKeyboardMarkup()
    start_game_button = types.InlineKeyboardButton("Почати гру", callback_data='start_game')
    keyboard.add(start_game_button)

    # Відправляємо повідомлення з кнопкою
    msg = bot.send_message(message.chat.id, f"Ваш герой створений! Ім'я: {user_name}, Здоров'я: 100HP",
                           reply_markup=keyboard)
    USER_MESSAGES[message.chat.id].append(msg.message_id)  # Зберігаємо ID нового повідомлення


@bot.callback_query_handler(func=lambda call: call.data == 'start_game')
def start_game(call):
    # Деактивуємо кнопку "Почати гру"
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

    # Коротка історія
    story_text = (
        "Ви ввійшли у підземелля. Темрява охоплює все навколо, "
        "ледь пробиваючись крізь світло вашого факела. Ви стоїте на роздоріжжі:\n\n"
        "Ліворуч ви чуєте дивне завивання вітру з темного тунелю.\n"
        "Праворуч ледь видно слабке мерехтіння світла, ніби там щось чекає на вас."
    )

    # Створюємо кнопки "Піти наліво" і "Піти направо"
    keyboard = types.InlineKeyboardMarkup()
    left_button = types.InlineKeyboardButton("Піти наліво", callback_data='go_left')
    right_button = types.InlineKeyboardButton("Піти направо", callback_data='go_right')
    keyboard.add(left_button, right_button)

    # Відправляємо історію з вибором
    bot.send_message(call.message.chat.id, story_text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['go_left', 'go_right'])
def choose_path(call):
    encounter = random_encounter()  # Викликаємо функцію, щоб отримати випадкову подію

    # Деактивуємо кнопки "Піти наліво" і "Піти направо"
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

    # Обробляємо вибір гравця та результат події
    if encounter is None:
        response_text = "Ви не зустріли нікого. Темрява навколо і тиша вас супроводжує..."
    elif isinstance(encounter, Monster):
        response_text = f"Ви зустріли {encounter.name} з {encounter.hp} HP та атакою {encounter.attack}!"
    elif isinstance(encounter, Chest):
        response_text = "Ви знайшли скриню з наступними предметами: " + ", ".join(encounter.items)
        encounter.open_chest(USER_DATA[call.message.chat.id]['hero'])  # Взаємодія зі скринею

    bot.send_message(call.message.chat.id, response_text)


def random_encounter():
    """Функція для визначення випадкової події після вибору шляху"""
    encounters = [None, FireDragon(), IceDragon(), PoisonDragon(), Chest()]  # Випадкові варіанти
    return random.choice(encounters)  # Повертаємо випадковий елемент


@bot.message_handler(commands=['status'])
def status(message):
    hero = USER_DATA.get(message.chat.id, {}).get('hero')
    if hero:
        msg = bot.send_message(message.chat.id, f"Ім'я героя: {hero.name}\nЗдоров'я: {hero.hp}HP\nСила: {hero.strength}")
        USER_MESSAGES[message.chat.id].append(msg.message_id)  # Зберігаємо ID нового повідомлення
    else:
        msg = bot.send_message(message.chat.id, "Ви ще не створили героя. Використайте команду /start.")
        USER_MESSAGES[message.chat.id] = [msg.message_id]  # Зберігаємо ID нового повідомлення


@bot.message_handler(commands=['clear'])
def clear_data(message):
    if message.chat.id in USER_DATA:
        del USER_DATA[message.chat.id]
        # Очищуємо повідомлення
        for msg_id in USER_MESSAGES.get(message.chat.id, []):
            try:
                bot.delete_message(message.chat.id, msg_id)
            except Exception as e:
                print(f"Не вдалося видалити повідомлення з ID {msg_id}: {e}")

        del USER_MESSAGES[message.chat.id]  # Очищаємо ID повідомлень
        bot.send_message(message.chat.id, "Ваші дані та повідомлення успішно очищено. Ви можете створити нового героя.")
    else:
        bot.send_message(message.chat.id, "У вас немає даних для очищення.")


@bot.message_handler(commands=['cancel'])
def cancel(message):
    bot.send_message(message.chat.id, 'Гру скасовано. Дякуємо за гру!')


# Запускаємо бота
if __name__ == '__main__':
    print("Бот запущений...")
    bot.polling(none_stop=True)
