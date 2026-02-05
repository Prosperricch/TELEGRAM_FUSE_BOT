import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

TOKEN = "8336577956:AAHtWI2tsC1o0Ghyd0KdgUyJzp66dNF_tpo"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'drinks', 'food'])
def main(message):
    # Command String Verify
    command = message.text.lstrip('/')
    user = message.from_user
    firstName = user.first_name

    # Commands Checking
    if command == 'start':
        bot.reply_to(message,
                     f"hi {firstName or 'There'}, welcome to the group")
    elif command == 'drinks':
        bot.reply_to(message,
                     f"hi {firstName or 'There'}, Have you tried Zobo?")
    elif command == 'food':
        bot.reply_to(message,
                     f"hi {firstName or 'There'}, Have you tried rice?")
        
print("Bot started.... Press Ctrl+C to stop")
bot.infinity_polling()
