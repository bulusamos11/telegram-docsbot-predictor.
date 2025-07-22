import os, logging, openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load tokens from environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! Send /virtualtips to get instant virtual football tips."
    )

async def virtualtips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = (
        "You are a football prediction expert. "
        "Provide 5 short virtual football match predictions in the format:\n"
        "<TeamA> vs <TeamB> – <Market> (<Odds>)\n"
        "Use popular markets: 1X2, Over 2.5, Under 2.5, BTTS. "
        "Keep odds realistic (1.50–2.20)."
    )

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        text = resp.choices[0].message.content.strip()
        await update.message.reply_text("📊 AI Virtual Football Tips:\n\n" + text)
    except Exception as e:
        await update.message.reply_text(f"❌ Error getting tips: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("virtualtips", virtualtips))
    logging.info("Bot started...")
    app.run_polling()
