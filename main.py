import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, BotCommand
import time
import os

TOKEN = os.environ.get("TELEGRAM_TOKEN") or "8336577956:AAHtWI2tsC1o0Ghyd0KdgUyJzp66dNF_tpo"
bot = telebot.TeleBot(TOKEN)

# Commands menu (run once or leave here)
bot.set_my_commands([
    BotCommand('start',   'Welcome & help'),
    BotCommand('drinks',  'Drink recommendations'),
    BotCommand('food',    'Food suggestions')
])

@bot.message_handler(commands=['start', 'drinks', 'food'])
def handle_commands(message):
    command = message.text.lower().lstrip('/').split()[0]
    name = message.from_user.first_name or 'There'

    if command == 'start':
        bot.reply_to(message, f"Hi {name}, welcome! 😊 Try /drinks or /food")
    elif command == 'drinks':
        bot.reply_to(message, f"Hi {name}, have you tried Zobo? 🍹")
    elif command == 'food':
        bot.reply_to(message, f"Hi {name}, have you tried rice? 🍚")

# Greet new members
@bot.message_handler(content_types=['new_chat_members'])
def greet_new_member(message):
    for member in message.new_chat_members:
        name = member.first_name or "new friend"
        bot.reply_to(message, f"Welcome {name}! 🎉 Glad you're here!")

# Read & reply to normal messages in group
@bot.message_handler(content_types=['text'])
def group_text_handler(message):
    text = message.text.lower()

    # Skip commands (already handled)
    if text.startswith('/'):
        return

    name = message.from_user.first_name or "there"

    if 'hello' in text or 'hi' in text:
        bot.reply_to(message, f"Hey {name}! 👋 What's up?")
    elif 'zobo' in text:
        bot.reply_to(message, f"Zobo lover detected! 🍹 {name}, you drinking today?")
    elif 'hungry' in text:
        bot.reply_to(message, f"Hungry {name}? Type /food for ideas 🍚")

print("Bot started.... Press Ctrl+C to stop")

while True:
    try:
        bot.infinity_polling(timeout=30, long_polling_timeout=20, interval=0)
    except Exception as e:
        print(f"Polling error: {e}")
        time.sleep(10)
