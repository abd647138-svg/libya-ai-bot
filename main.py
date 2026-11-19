import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلا بيك! أنا LibyaAI Bot 🇱🇾 اسألني أي شي")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        prompt = update.message.text
        response = model.generate_content(f"أنت مساعد ذكي ليبي، رد باللهجة الليبية البسيطة والمفهومة: {prompt}")
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("صار خطأ شوية، عاود المحاولة")
        print(e)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()
