import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_LINK = os.getenv("GROUP_LINK")
CODES_FILE = "codes.json"

# Load codes from file
def load_codes():
    try:
        with open(CODES_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save codes to file
def save_codes(codes):
    with open(CODES_FILE, "w") as f:
        json.dump(codes, f, indent=2)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"/start triggered by: {update.effective_user.username}")
    await update.message.reply_text(
        "Hi! To join The Snug, please enter your access code like this:\n\n/verify YOURCODE"
    )

# Command: /verify <code>
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"/verify triggered by: {update.effective_user.username}")
    codes = load_codes()
    user = update.effective_user
    args = context.args

    if not args:
        await update.message.reply_text("❗ Please enter your code like this:\n/verify YOURCODE")
        return

    code = args[0].strip().upper()

    if code not in codes:
        await update.message.reply_text("❌ That code isn’t valid. Please check and try again.")
        return

    if codes[code]:
        await update.message.reply_text("⚠️ That code has already been used.")
        return

    # Mark code as used
    codes[code] = True
    save_codes(codes)

    await update.message.reply_text(
        f"✅ Welcome to The Snug, {user.first_name}! 🦥\n\n"
        f"Here’s your private invite link:\n{GROUP_LINK}\n\n"
        f"Please do not share this link — it's just for you!"
    )

# Log non-command messages to confirm activity
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Received message in group: {update.message.text}")

# App setup
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).parse_mode("HTML").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verify", verify))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()
