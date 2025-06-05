import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime

# Get environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_LINK = os.getenv("GROUP_LINK")
MOD_GROUP_ID = os.getenv("MOD_GROUP_ID")
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
    await update.message.reply_text(
        "Hi! To join The Snug, please enter your access code like this:\n\n/verify YOURCODE"
    )

# Command: /verify <code>
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    # Send public confirmation message (no link)
    await update.message.reply_text(
        f"✅ Thanks {user.first_name}, your code is valid!\n\n"
        f"📩 Please check your private messages from <b>@TheSnugBot</b> — it contains your one-time invite to The Snug Lounge.\n\n"
        f"⚠️ If you don’t see a DM, first message the bot directly to open the chat: @TheSnugBot",
        parse_mode="HTML"
    )

    # Send invite link privately
    try:
        await context.bot.send_message(
            chat_id=user.id,
            text=(
                f"✅ Welcome to The Snug, {user.first_name}! 🦥\n\n"
                f"Here’s your private invite link:\n{GROUP_LINK}\n\n"
                f"Please do not share this link — it's just for you!"
            )
        )
    except Exception as e:
        await update.message.reply_text("❗ I couldn’t DM you! Please message @TheSnugBot first to unlock your chat.")

    # Send log to mod group
    try:
        await context.bot.send_message(
            chat_id=int(MOD_GROUP_ID),
            text=(
                f"👤 <b>{user.full_name}</b> just verified with code <code>{code}</code>\n"
                f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"🔗 <a href='tg://user?id={user.id}'>View Profile</a>"
            ),
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Error sending log to mod group: {e}")

# Main app setup
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("verify", verify))
    app.run_polling()
