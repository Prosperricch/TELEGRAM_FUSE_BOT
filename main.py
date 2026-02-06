import telebot
from telebot.types import BotCommand
import google.generativeai as genai
import os
import time

# ==================== CONFIG ====================
TOKEN = os.environ.get("TELEGRAM_TOKEN") or "8336577956:AAHtWI2tsC1o0Ghyd0KdgUyJzp66dNF_tpo"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or "AIzaSyBThIX_Pzh_4vVNguiv2kAyxUboCruUrLY"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

bot = telebot.TeleBot(TOKEN)

# Set visible commands
bot.set_my_commands([
    BotCommand('start',   'Welcome message'),
    BotCommand('drinks',  'Drink recommendations'),
    BotCommand('food',    'Food suggestions'),
    BotCommand('ai',      'Ask AI anything (e.g. /ai What is the capital of Nigeria?)')
])

# ==================== COMMAND HANDLERS ====================
@bot.message_handler(commands=['start', 'drinks', 'food'])
def handle_commands(message):
    command = message.text.lower().lstrip('/').split()[0]
    name = message.from_user.first_name or 'There'

    if command == 'start':
        bot.reply_to(message, f"Hi {name}! Welcome 😊 Try /drinks, /food or /ai")
    elif command == 'drinks':
        bot.reply_to(message, f"Hi {name}, have you tried Zobo? 🍹")
    elif command == 'food':
        bot.reply_to(message, f"Hi {name}, have you tried rice? 🍚")

# ==================== NEW: AI COMMAND ====================
@bot.message_handler(commands=['ai'])
def ai_command(message):
    # Get everything after /ai
    question = message.text.replace('/ai', '', 1).strip()

    if not question:
        bot.reply_to(message, "Please ask something after /ai\nExample: `/ai What is the capital of Nigeria?`")
        return

    name = message.from_user.first_name or "there"
    bot.reply_to(message, f"Thinking... 🤖")   # nice feedback

    try:
        response = model.generate_content(
            f"You are a friendly and helpful university student assistant. "
            f"Answer in a casual, fun way. Keep replies short and clear.\n\n"
            f"User: {question}"
        )
        answer = response.text.strip()
    except Exception as e:
        answer = "Sorry, Gemini is busy right now 😅 Try again in a moment."

    bot.reply_to(message, f"@{name} 👇\n\n{answer}")

# ==================== GROUP REACTIONS & GREETINGS ====================
@bot.message_handler(content_types=['new_chat_members'])
def greet_new_member(message):
    for member in message.new_chat_members:
        name = member.first_name or "new friend"
        bot.reply_to(message, f"Welcome {name}! 🎉 Glad you're here!")

@bot.message_handler(content_types=['text'])
def group_text_handler(message):
    text = message.text.lower()
    if text.startswith('/'): return   # ignore commands

    name = message.from_user.first_name or "there"

    if 'hello' in text or 'hi' in text:
        bot.reply_to(message, f"Hey {name}! 👋 How's it going?")
    elif 'zobo' in text:
        bot.reply_to(message, f"Zobo gang! 🍹 {name}, you drinking today?")
    elif 'hungry' in text:
        bot.reply_to(message, f"Hungry {name}? Type /food for ideas 🍚")

print("Bot started with Gemini AI...")

while True:
    try:
        bot.infinity_polling(timeout=30, long_polling_timeout=20)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
