import logging
import sqlite3
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURATION (Edit These) ---
BOT_TOKEN = "APNA_BOT_TOKEN_YAHAN_DALO" 
ADMIN_ID = 123456789 
CHANNEL_LINK = "https://t.me/YourChannel" # Aapka Channel Link
SHORTLINK_URL = "https://gplinks.in/api?api=YOUR_API&url=https://google.com" # Example

# --- DATABASE SETUP ---
conn = sqlite3.connect('play4coin.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                  (user_id INTEGER PRIMARY KEY, balance INTEGER DEFAULT 100, referred_by INTEGER)''')
conn.commit()

# --- MAIN MENU KEYBOARD ---
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎮 Play Tic-Tac-Toe", callback_query_data='play_menu')],
        [InlineKeyboardButton("💰 Earn Coins", callback_query_data='earn'), InlineKeyboardButton("👥 Invite Friends", callback_query_data='invite')],
        [InlineKeyboardButton("🏦 Wallet / Redeem", callback_query_data='wallet')],
        [InlineKeyboardButton("📊 My Stats", callback_query_data='stats'), InlineKeyboardButton("📢 Updates", url=CHANNEL_LINK)]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- COMMANDS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # Referral Logic
    if context.args and context.args[0].isdigit():
        ref_by = int(context.args[0])
        cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
        if not cursor.fetchone() and ref_by != user_id:
            cursor.execute("INSERT INTO users (user_id, referred_by) VALUES (?, ?)", (user_id, ref_by))
            cursor.execute("UPDATE users SET balance = balance + 500 WHERE user_id=?", (ref_by,))
            conn.commit()
    
    # Ensure user exists
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

    welcome_text = (
        "🔥 **Welcome to Play4Coin Bot!**\n\n"
        "Yahan aap Tic-Tac-Toe khel kar aur doston ko invite karke real rewards jeet sakte hain.\n\n"
        "🎮 **Game Khele:** Har jeet par coins milege.\n"
        "👥 **Invite Kare:** Har referral par 500 coins."
    )
    await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Difficulty Select Karein:", 
                                   reply_markup=InlineKeyboardMarkup([[
                                       InlineKeyboardButton("Easy", callback_query_data='game_easy'),
                                       InlineKeyboardButton("Medium", callback_query_data='game_med'),
                                       InlineKeyboardButton("Hard (Pro)", callback_query_data='game_hard')
                                   ]]), parse_mode="Markdown")

# --- CALLBACK HANDLER (Buttons) ---
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == 'invite':
        ref_link = f"https://t.me/Play4CoinBot?start={user_id}"
        msg = f"🚀 **Aapka Referral Link:**\n`{ref_link}`\n\nIs link ko doston ke saath share karein. Jab wo join karenge, aapko **500 Coins** milenge!"
        await query.edit_message_text(msg, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

    elif query.data == 'wallet':
        cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
        bal = cursor.fetchone()[0]
        msg = f"🏦 **Aapka Wallet**\n\n💰 Balance: `{bal}` Coins\n\n⚠️ Withdraw karne ke liye minimum 5,000 coins chahiye."
        await query.edit_message_text(msg, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

# --- MAIN FUNCTION ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play_command))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    
    print("Bot is Live... Go to Telegram and search @Play4CoinBot")
    app.run_polling()

if __name__ == '__main__':
    main()
      
