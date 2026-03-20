"""
SciAstra Coaching Group Bot
============================
Admin: @Sahil_sciastra

HOW TO UPDATE SCHEDULE:
  - Replace the image file path in SCHEDULE_IMAGE variable below
  - Or update the SCHEDULE_TEXT string for text fallback

HOW TO ADD NEW COMMANDS:
  - Copy any existing async def handler, rename it, change the text
  - Register it at the bottom with: application.add_handler(CommandHandler('yourcommand', your_function))

HOW TO ADD MORE BAD WORDS:
  - Add words to the BAD_WORDS list below
"""

import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# ─────────────────────────────────────────────
# ✏️  EASY EDIT ZONE — change these anytime
# ─────────────────────────────────────────────

BOT_TOKEN = "8683877270:AAE92_iTUBdNst5TVPCGaKseajql4buOURo"

# Your Telegram username (without @)
ADMIN_USERNAME = "Sahil_sciastra"

# Path to your schedule image (place the image in the same folder as bot.py)
SCHEDULE_IMAGE = "schedule.png"

# Fallback text if image is not found
SCHEDULE_TEXT = """
📅 *Week 2 — IAT/NEST Crash Course 2026*
🗓 16th March – 21st March
🕐 Mon–Sat | 10:00 AM – 3:00 PM

| Day       | 10:00–11:30 | 11:45–1:15 | 1:30–3:00 |
|-----------|------------|-----------|----------|
| Monday    | Biology    | Chemistry | Physics  |
| Tuesday   | Maths      | Chemistry | Biology  |
| Wednesday | Physics    | Chemistry | Maths    |
| Thursday  | Biology    | Chemistry | Physics  |
| Friday    | Chemistry  | Biology   | Maths    |
| Saturday  | Maths      | Biology   | Physics  |

Total: Bio×5 | Chem×5 | Phy×4 | Maths×4 = *18 classes*
"""

# ✏️  Add/remove bad words here (lowercase)
BAD_WORDS = [
    "fuck", "shit", "bastard", "bitch", "asshole", "dick", "pussy",
    "nude", "naked", "porn", "sex", "xxx", "bsdk", "BSDK", "adult", "nsfw", "Chod", "Madar", "lodu",
    "chutiya", "madarchod", "bhenchod", "gandu", "randi", "harami",
    "bhosdike", "lund", "gaand", "chut", "saala", "mc", "bc", "land", "Land", "jhatu", 
    "Jhatu", "Suck", "suck", "chodu", "gandu", "Gandu", "Lodi", "lodi", "betichod", "maa ki chuut"
    "maa ki chut", "nangi"
]

# ✏️  Welcome message shown when someone types /start
WELCOME_MESSAGE = """
👋 *Welcome to SciAstra Coaching Bot!*

Here's what I can do:

📅 /schedule — See this week's class timetable
❓ /guide — Get help from admin
📢 /rules — Group rules
ℹ️ /about — About this group

_Type any command to get started!_
"""

# ✏️  Rules message
RULES_MESSAGE = """
📋 *Group Rules*

1️⃣ Be respectful to everyone
2️⃣ No adult or inappropriate content
3️⃣ Stay on topic — academics only
4️⃣ No spamming or self-promotion
5️⃣ Ask doubts politely

_Breaking rules = warning → ban_ ⚠️
"""

# ✏️  About message
ABOUT_MESSAGE = """
ℹ️ About SciAstra

This is the official study group for IAT/NEST Crash Course 2026.

🌐 Website: sciAstra.com
Admin: @Sahil_sciastra

Study hard, score high! 🚀
"""

# ─────────────────────────────────────────────
# Bot setup (don't need to edit below)
# ─────────────────────────────────────────────

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode="Markdown")


# /schedule — sends image if found, else text
async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists(SCHEDULE_IMAGE):
        with open(SCHEDULE_IMAGE, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption="📅 *This week's schedule* — SciAstra IAT/NEST Crash Course 2026",
                parse_mode="Markdown"
            )
    else:
        await update.message.reply_text(SCHEDULE_TEXT, parse_mode="Markdown")


# /guide — tags admin
async def guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(
        f"🙋 {user.first_name} needs help!\n\n"
        f"@{ADMIN_USERNAME} — a student is requesting guidance. 👆"
    )


# /rules
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(RULES_MESSAGE, parse_mode="Markdown")


# /about
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ABOUT_MESSAGE)


# Auto-delete bad words from text messages
async def filter_bad_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()
    found = [word for word in BAD_WORDS if word in text]

    if found:
        user = update.message.from_user
        try:
            await update.message.delete()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    f"⚠️ @{user.username or user.first_name}, your message was removed "
                    f"for violating group rules.\n\n"
                    f"Please keep the group clean and respectful. 🙏\n"
                    f"_Repeated violations may result in a ban._"
                ),
                parse_mode="Markdown"
            )
            logger.info(f"Deleted message from {user.username} — contained: {found}")
        except Exception as e:
            logger.error(f"Could not delete message: {e}")


# Auto-delete adult images/videos (stickers, GIFs, videos flagged by caption)
async def filter_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    caption = (update.message.caption or "").lower()
    has_bad_caption = any(word in caption for word in BAD_WORDS)

    # Check if message has flagged caption on media
    if has_bad_caption and (update.message.photo or update.message.video or update.message.document):
        user = update.message.from_user
        try:
            await update.message.delete()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    f"⚠️ @{user.username or user.first_name}, your media was removed "
                    f"for inappropriate content.\n\n"
                    f"_This group is for academic purposes only._ 📚"
                ),
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Could not delete media: {e}")


# ─────────────────────────────────────────────
# Register all handlers & run
# ─────────────────────────────────────────────

application = ApplicationBuilder().token(BOT_TOKEN).build()

# Commands — filters.ALL makes /cmd@BotName work in groups too
application.add_handler(CommandHandler("start",    start,    filters=filters.ALL))
application.add_handler(CommandHandler("schedule", schedule, filters=filters.ALL))
application.add_handler(CommandHandler("guide",    guide,    filters=filters.ALL))
application.add_handler(CommandHandler("rules",    rules,    filters=filters.ALL))
application.add_handler(CommandHandler("about",    about,    filters=filters.ALL))

# ✏️  TO ADD A NEW COMMAND — copy the two lines below, change the name:
# application.add_handler(CommandHandler("mycommand", my_function, filters=filters.ALL))

# Auto-filters
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_bad_words))
application.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.Document.ALL, filter_media))

print("✅ Bot is running...")
application.run_polling()
