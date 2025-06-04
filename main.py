import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
# Trigger redeploy

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROUP_LINK = os.environ.get("GROUP_LINK")

valid_codes = {
    "7RH4DCGL",
    "QWUNAWK8",
    "QV1Y2UXZ"
}
used_codes = set()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to The Snug 🦥\nPlease enter your access code:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip().upper()

    if code in used_codes:
        await update.message.reply_text("❌ This code has already been used.")
    elif code in valid_codes:
        used_codes.add(code)
        await update.message.reply_text(f"✅ Access granted! Join here:\n{GROUP_LINK}")
    else:
        await update.message.reply_text("❌ Invalid code. Try again.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🤖 Bot is running...")
app.run_polling()
