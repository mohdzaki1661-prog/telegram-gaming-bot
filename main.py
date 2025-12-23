import telebot
from telebot import types
import database
import games

TOKEN = '8481908531:AAE0aHzORrGuX02wwoAkQqeG7M63OBcfBeE'
bot = telebot.TeleBot(TOKEN)

database.init_db()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("🎲 Dice Game")
    btn2 = types.KeyboardButton("💰 Balance")
    markup.add(btn1, btn2)
    bot.reply_to(message, "Welcome! Game khelo aur coins kamao.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🎲 Dice Game")
def play_dice(message):
    user_roll = games.dice_roll()
    bot.send_message(message.chat.id, f"Aapne dice phenka aur aaya: {user_roll} 🎲")
    
    # Logic: Agar 4 se bada number aaya toh hi jeetoge
    if user_roll > 3:
        database.add_coins(message.from_user.id, 10)
        bot.send_message(message.chat.id, "Mubarak ho! Aap 10 coins jeet gaye! 🎉")
    else:
        bot.send_message(message.chat.id, "Oh ho! Aap haar gaye. Dubara koshish karein. ❌")

@bot.message_handler(func=lambda message: message.text == "💰 Balance")
def check_balance(message):
    bal = database.get_balance(message.from_user.id)
    bot.send_message(message.chat.id, f"Aapka total balance: {bal} coins")

bot.infinity_polling()
