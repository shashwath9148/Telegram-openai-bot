import os
import logging
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Logging
logging.basicConfig(level=logging.INFO)

# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Flask app for Render health check
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

# Telegram Bot Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Send me a prompt and I’ll generate an image with OpenAI.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await update.message.reply_text("🎨 Generating image... please wait...")

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="512x512"
    )

    image_url = result.data[0].url
    await update.message.reply_photo(photo=image_url, caption="✅ Here’s your AI-generated image!")

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    appbuilder = ApplicationBuilder().token(BOT_TOKEN).build()
    appbuilder.add_handler(CommandHandler("start", start))
    appbuilder.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    import threading
    threading.Thread(target=run).start()
    appbuilder.run_polling()
