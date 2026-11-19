import os
import threading
from flask import Flask
import telebot

TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TELEGRAM_TOKEN") or "حط_التوكن_هنا"

bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "اهلا بيك في بوت ليبيا AI 🇱🇾\nابعتلي رسالة او صورة ونجاوبك")

@bot.message_handler(content_types=['photo'])
def photo(message):
    bot.reply_to(message, "وصلتني الصورة ✅ توا بنشوفها ونرد عليك")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, f"وصلتني رسالتك: {message.text}")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

if __name__ == "__main__":
    print("Bot started...")
    bot.infinity_polling()
