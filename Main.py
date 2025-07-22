import os
import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load tokens securely from secrets
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Use /virtualtips to get today's smart AI football predictions.")

async def virtualtips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = (
        "You are a football prediction expert. "
        "Provide 5 smart virtual football match predictions in this format:\n"
        "Team A vs Team B – Market (Odds)\n"
        "Markets: 1X2, Over 2.5, Under 2.5, BTTS\n"
        "Use odds between 1.50 and 2.20 only."
    )
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        reply = response.choices[0].message.content
        await update.message.reply_text("📊 Predictions:\n\n" + reply)
    except Exception as e:
        await update.message.reply_text("❌ Error: " + str(e))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("virtualtips", virtualtips))
    logging.info("Bot running...")
    app.run_polling()
