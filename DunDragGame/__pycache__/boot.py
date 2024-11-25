import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# Встановлюємо рівень логування game_entities.py
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

CHOOSING, TYPING_NAME = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[InlineKeyboardButton("Створити героя", callback_data='create_hero')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Створюємо клавіатуру
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Додаємо кнопки з інформацією про героя
    hero_info_button = types.KeyboardButton(f"Інфо про героя:")
    keyboard.add(hero_info_button)

    await update.message.reply_text('Вітаю у грі Підземелля та Дракони! Натисніть кнопку нижче, щоб створити героя.', reply_markup=reply_markup)
    return CHOOSING

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'create_hero':
        await query.edit_message_text(text="Введіть ім'я вашого героя:")
        return TYPING_NAME

async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_name = update.message.text
    context.user_data['hero_name'] = user_name
    await update.message.reply_text(f"Ваш герой створений! Ім'я: {user_name}, Здоров'я: 100HP")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Гру скасовано. Дякуємо за гру!')
    return ConversationHandler.END

async def main() -> None:
    logging.info("Запуск бота...")
    application = ApplicationBuilder().token("7733352163:AAG6r0WvTJO5tBSTAr8i6kWuUyWRTYozlws").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [CallbackQueryHandler(button)],
            TYPING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
