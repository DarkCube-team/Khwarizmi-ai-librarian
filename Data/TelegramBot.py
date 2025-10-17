import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI


client = OpenAI(api_key=OPENAI_API_KEY)

# --- Logging ---
logging.basicConfig(level=logging.INFO)

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your AI bot 🤖. Ask me anything!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-4o"
        messages=[{"role": "user", "content": user_message}],
    )

    bot_reply = response.choices[0].message.content
    await update.message.reply_text(bot_reply)

# --- Main ---
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
