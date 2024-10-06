import telebot

bot = telebot.TeleBot('7733352163:AAG6r0WvTJO5tBSTAr8i6kWuUyWRTYozlws')

@bot.message_handler(content_types=['text'])
def send_echo(message):
    bot.send_message(message.chat.id, message.text)

bot.polling()

# http://t.me/Exo_snc_bot