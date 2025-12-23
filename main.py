import telebot
from telebot import types
import database  # Aapki database.py file

TOKEN = 'YAHAN_APNA_BOT_TOKEN_DAALEIN'
bot = telebot.TeleBot(TOKEN)

# Bot start hote hi database setup karega
database.init_db()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("🎮 Play Game")
    btn2 = types.KeyboardButton("💰 My Balance")
    markup.add(btn1, btn2)
    bot.reply_to(message, "Welcome! Game khelo aur earning karo.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "💰 My Balance")
def balance(message):
    user_id = message.from_user.id
    coins = database.get_balance(user_id)
    bot.send_message(message.chat.id, f"Aapka balance: {coins} coins")

@bot.message_handler(func=lambda message: message.text == "🎮 Play Game")
def play(message):
    # Ek simple game: Direct 10 coins milenge demo ke liye
    user_id = message.from_user.id
    database.add_coins(user_id, 10)
    bot.send_message(message.chat.id, "Mubarak ho! Aapne game khela aur 10 coins kamaye!")

bot.polling()


