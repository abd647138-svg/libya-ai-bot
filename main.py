import os
import threading
import telebot
from flask import Flask
import google.generativeai as genai
from PIL import Image

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live"

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "اهلا بيك، انا بوت ليبيا AI، ابعتلي اي سؤال او صورة")

@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        bot.send_chat_action(message.chat.id, "typing")
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print("Text Error:", e)
        bot.reply_to(message, "صار خطأ")

@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    try:
        bot.send_chat_action(message.chat.id, "typing")
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)
        with open("temp.jpg", "wb") as f:
            f.write(downloaded)
        img = Image.open("temp.jpg")
        response = model.generate_content(["اشرح هده الصورة بالتفصيل بالعربية", img])
        bot.reply_to(message, response.text)
    except Exception as e:
        print("Photo Error:", e)
        bot.reply_to(message, "صار خطأ في الصورة")

def run_bot():
    print("Bot started polling...")
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
