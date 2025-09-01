import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.getenv("8253801582:AAHDkzPjXtQ80oqGkV4O-s7ExEF4f-lzJPs")
OPENAI_API_KEY = os.getenv("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")

async def generate_image(prompt: str):
    url = "https://api.openai.com/v1/images/generations"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    data = {"model": "gpt-image-1", "prompt": prompt, "size": "512x512"}
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["data"][0]["url"]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text
    await update.message.reply_text("🎨 Generating image... please wait...")
    try:
        image_url = await generate_image(user_prompt)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()