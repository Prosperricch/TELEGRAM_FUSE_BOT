import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

TOKEN = "8336577956:AAHtWI2tsC1o0Ghyd0KdgUyJzp66dNF_tpo"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    # Create buttons RIGHT HERE when user does /start
    markup = InlineKeyboardMarkup()
    show_prices = InlineKeyboardButton('Shoe Prices', callback_data='shoe_details')
    markup.add(show_prices)

    bot.send_message(
        message.chat.id,
        "Hi there! Click the button below to see shoe prices.",
        reply_markup=markup
    )

# Only ONE callback handler — combine logic if needed
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call: CallbackQuery):
    bot.answer_callback_query(call.id)  # remove loading spinner

    if call.data == 'shoe_details':
        chat_id = call.message.chat.id

        prices_text = (
            "Here are the shoe prices:\n\n"
            "SHOE ID: 1\n"
            "NAME: Adidas\n"
            "PRICE: $100\n\n"
            "SHOE ID: 2\n"
            "NAME: Nike\n"
            "PRICE: $120"
        )

        bot.send_message(chat_id, prices_text)

    else:
        bot.send_message(call.message.chat.id, "Unknown button pressed.")

print("Bot started.... Press Ctrl+C to stop")
bot.infinity_polling()
