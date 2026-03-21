"""
SciAstra Coaching Group Bot
============================
Admin: @Sahil_sciastra

HOW TO UPDATE SCHEDULE:
  - Replace schedule.png in your folder with the new image (keep same filename)

HOW TO EDIT ANY MESSAGE:
  - Find the message variable (e.g. TIPS_PLANNING) in the EASY EDIT ZONE below
  - Change the text, save, re-upload to GitHub

HOW TO ADD A NEW COMMAND:
  - Add a new message variable in the EASY EDIT ZONE
  - Copy any async def handler below, rename it, point it to your new message
  - Register it at the bottom with: application.add_handler(CommandHandler("name", function, filters=filters.ALL))

HOW TO ADD MORE BAD WORDS:
  - Add words (lowercase) to the BAD_WORDS list below

HOW TO ALLOW A NEW LINK:
  - Add the domain to ALLOWED_DOMAINS list below
"""

import logging
import os
import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# ─────────────────────────────────────────────
# EASY EDIT ZONE — change these anytime
# ─────────────────────────────────────────────

BOT_TOKEN = "8683877270:AAE92_iTUBdNst5TVPCGaKseajql4buOURo"

# ✏️  ADMINS LIST — add or remove admins anytime (without @)
# First person in the list is the main admin tagged by /guide
# To add a new admin: add their username in quotes with a comma
# Example: ADMINS = ["Sahil_sciastra", "newadmin123"]
ADMINS = [
    "Sahil_sciastra",    # Main admin — tagged by /guide
    "Evyavansachan",
    "jester_here",
]

# Main admin is always the first one in the list
MAIN_ADMIN = ADMINS[0]

# Builds a tag string for all admins e.g. "@Sahil_sciastra @other_admin"
def tag_all_admins():
    return " ".join(f"@{a}" for a in ADMINS)

# Path to schedule image (must be in same folder as bot.py)
SCHEDULE_IMAGE = "schedule.png"

# Fallback text if image not found
SCHEDULE_TEXT = """
Week 2 - IAT/NEST Crash Course 2026
16th March - 21st March | Mon-Sat | 10:00 AM - 3:00 PM

Day        | 10:00-11:30 | 11:45-1:15 | 1:30-3:00
Monday     | Biology     | Chemistry  | Physics
Tuesday    | Maths       | Chemistry  | Biology
Wednesday  | Physics     | Chemistry  | Maths
Thursday   | Biology     | Chemistry  | Physics
Friday     | Chemistry   | Biology    | Maths
Saturday   | Maths       | Biology    | Physics

Total: Bio x5 | Chem x5 | Phy x4 | Maths x4 = 18 classes
"""

# Bad words list (add more anytime, keep lowercase)
BAD_WORDS = [
    "fuck", "shit", "bastard", "bitch", "asshole", "dick", "pussy",
    "nude", "naked", "porn", "sex", "xxx", "adult", "nsfw",
    "chutiya", "madarchod", "bhenchod", "gandu", "randi", "harami",
    "bhosdike", "lund", "gaand", "chut", "saala", "mc", "bc"
]

# Allowed domains — links from these sites will NOT be deleted
ALLOWED_DOMAINS = [
    "sciastra.com",
    "youtube.com",
    "youtu.be",
    "iiseradmission.in",
    "nestexam.in",
    "ncert.nic.in",
    "drive.google.com",
    "docs.google.com",
]

# Suspicious patterns — messages containing these are auto-deleted
SUSPICIOUS_PATTERNS = [
    "t.me/+",               # Telegram group invite links
    "t.me/joinchat",        # Old Telegram invite format
    "telegram.me/joinchat",
    "bit.ly",               # URL shorteners
    "tinyurl.com",
    "shorturl.at",
    "cutt.ly",
    "rb.gy",
    "is.gd",
    "gg.gg",
    "tiny.cc",
    "ow.ly",
    "buff.ly",
    "adf.ly",               # Ad-based shorteners
    "linktr.ee",            # Self-promotion pages
    "taplink.cc",
    "solo.to",
    "onlyfans.com",         # Adult platforms
    "xvideos.com",
    "pornhub.com",
    "xnxx.com",
    "xhamster.com",
]

# Welcome message
WELCOME_MESSAGE = """
Welcome to SciAstra Telegram Bot! 👋

Here's what I can help you with:

/start       - See everything the bot can do
/schedule    - This week's class timetable
/planning    - How to plan your study schedule
/strategy    - Exam strategy and time management
/motivation  - Feeling low? Read this
/resources   - Books and revision tips
/cutoff      - Cutoffs and college info
/rules       - Group rules
/about       - About this group
/guide       - Ask the mentor directly
"""

# Rules message
RULES_MESSAGE = """
Group Rules

1. Be respectful to everyone
2. No adult or inappropriate content
3. Stay on topic - academics only
4. No spamming or self-promotion
5. Ask doubts politely
6. Do not share personal contact info publicly

Breaking rules = warning then ban ⚠️
"""

# About message
ABOUT_MESSAGE = """
About SciAstra

Official study group for IAT/NEST Crash Course 2026.

Website: sciAstra.com
Mentor: @Sahil_sciastra
"""

# Planning tips
TIPS_PLANNING = """
Study Schedule and Planning Tips

How many hours should you study daily?
Aim for 6-8 focused hours. Quality beats quantity - 5 hours of real focus is better than 10 hours of distraction.

How to balance school and crash course?
- Attend all crash course classes first (priority)
- Use school free periods for quick revision
- Keep weekends for full mock tests and weak topic revision

Should I attempt both IAT and NEST?
Yes. Both exams have overlapping syllabus. Attempting both gives you more chances. Focus more on whichever exam date comes first.

Weekly plan suggestion:
- Mon-Sat: Attend classes + solve 30 questions daily per subject
- Sunday: Full mock test in the morning, revision in evening
"""

# Exam strategy tips
TIPS_STRATEGY = """
Exam Strategy and Time Management

During the exam:
- First 5 minutes: Read the full paper once, mark easy questions
- Attempt easy questions first - build confidence and save time
- Do not spend more than 2 minutes on any single question
- Come back to tough questions after finishing easy ones
- Leave 10 minutes at the end for review

Accuracy vs attempts:
- IAT: Negative marking applies - only attempt if 70%+ confident
- NEST: Attempt more - negative marking is lower
- Target 80%+ accuracy over high attempts

For mock tests:
- Simulate real exam conditions - no phone, no breaks
- Analyse every wrong answer after the test
- Focus on why you got it wrong, not just the correct answer
"""

# Motivation message
TIPS_MOTIVATION = """
Feeling Low? Read This

It is completely normal to feel this way. Every topper has been here.

When mock scores are low:
- One bad mock does not define your result
- Treat every mock as practice, not judgment
- Analyse mistakes calmly - each wrong answer is a lesson

When you feel behind others:
- Stop comparing. Everyone has a different starting point.
- Focus on your own progress from last week, not others' scores
- Even 1% improvement daily adds up over time

When you feel like giving up:
- Remember why you started this journey
- Talk to the mentor - that is what we are here for
- Take a short break (30 mins max), then come back stronger

You are not alone in this. The entire batch is going through the same pressure. Keep going! 🔥
"""

# Resources tips
TIPS_RESOURCES = """
Books and Revision Tips

For IAT/NEST - what is enough?
- NCERT is the foundation - read every line, every example
- SciAstra material provided in class is sufficient
- Do not keep buying new books - depth over breadth
- You can prefer SciAstra books too.

Revision strategy (last 2 weeks):
- Week 1: Topic-wise revision + solve past year questions
- Week 2: Full mock tests daily + only revise weak topics
- Last 2 days: Light revision only, no new topics

How to revise effectively:
- Make a 1-page cheat sheet for each chapter (key formulas, reactions, concepts)
- Teach concepts out loud as if explaining to someone - best memory trick
- Solve at least 5 past year questions per topic

Previous year papers:
- IAT: Last 5 years papers are a must
- NEST: Last 3 years papers are enough
- Find them at sciAstra.com or ask in the group
"""

# Cutoff and college info
TIPS_CUTOFF = """
Cutoffs and College Info

IAT (IISER Aptitude Test):
- Generally top 500-800 ranks get good campus and branch options
- IISER Pune, Kolkata, Mohali are most preferred
- BS-MS dual degree: 5 years, excellent research opportunities

NEST (National Entrance Screening Test):
- For admission to NISER Bhubaneswar and CEBS Mumbai
- Cutoff: Top 300-400 ranks for NISER
- Integrated MSc: 5 years, great for research careers

Which is better - IAT or NEST?
Both are excellent for science research careers. IISER network is larger (7 campuses). NISER is highly ranked for biology and physics.

After clearing these exams:
- Direct research exposure from Year 1
- PhD opportunities in top institutes globally
- Strong alumni network in academia and industry

For latest cutoffs always check official websites:
- iiseradmission.in
- nestexam.in
"""

# ─────────────────────────────────────────────
# Bot logic — no need to edit below this line
# ─────────────────────────────────────────────

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)


async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists(SCHEDULE_IMAGE):
        with open(SCHEDULE_IMAGE, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption="This week's class schedule - SciAstra IAT/NEST Crash Course 2026"
            )
    else:
        await update.message.reply_text(SCHEDULE_TEXT)


async def guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    name = user.first_name or "A student"
    await update.message.reply_text(
        f"{name} needs help!\n\n"
        f"{tag_all_admins()} - a student is requesting your guidance."
    )


async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(RULES_MESSAGE)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ABOUT_MESSAGE)


async def planning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TIPS_PLANNING)


async def strategy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TIPS_STRATEGY)


async def motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TIPS_MOTIVATION)


async def resources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TIPS_RESOURCES)


async def cutoff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TIPS_CUTOFF)


def has_suspicious_link(text: str):
    """Returns (True, reason) if suspicious link found, else (False, '')."""
    text_lower = text.lower()

    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in text_lower:
            return True, f"a suspicious link ({pattern})"

    urls = re.findall(r'https?://[^\s]+|www\.[^\s]+', text_lower)
    for url in urls:
        is_allowed = any(domain in url for domain in ALLOWED_DOMAINS)
        if not is_allowed:
            return True, "an unknown or unverified link"

    return False, ""


async def filter_bad_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()
    user = update.message.from_user
    uname = user.username or user.first_name

    # Check bad words — whole word match only so "obc" does not trigger "bc"
    found_words = [word for word in BAD_WORDS if re.search(r'\b' + re.escape(word) + r'\b', text)]
    if found_words:
        try:
            await update.message.delete()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    f"⚠️ @{uname}, your message was removed for violating group rules.\n"
                    f"Please keep the group clean and respectful.\n"
                    f"Repeated violations may result in a ban."
                )
            )
            logger.info(f"Deleted bad-word message from {uname}")
        except Exception as e:
            logger.error(f"Could not delete message: {e}")
        return

    # Check suspicious links
    flagged, reason = has_suspicious_link(update.message.text)
    if flagged:
        try:
            await update.message.delete()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    f"⚠️ @{uname}, your message was removed because it contained {reason}.\n"
                    f"Only verified links are allowed in this group.\n"
                    f"If you want to share something, ask the admin first."
                )
            )
            logger.info(f"Deleted link message from {uname} - reason: {reason}")
        except Exception as e:
            logger.error(f"Could not delete link message: {e}")


async def filter_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    caption = update.message.caption or ""
    caption_lower = caption.lower()
    user = update.message.from_user
    uname = user.username or user.first_name

    has_bad_word = any(word in caption_lower for word in BAD_WORDS)
    link_flagged, link_reason = has_suspicious_link(caption)

    if (has_bad_word or link_flagged) and (
        update.message.photo or update.message.video or update.message.document
    ):
        reason_text = "inappropriate content" if has_bad_word else link_reason
        try:
            await update.message.delete()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=(
                    f"⚠️ @{uname}, your media was removed because it contained {reason_text}.\n"
                    f"This group is for academic purposes only."
                )
            )
            logger.info(f"Deleted media from {uname} - reason: {reason_text}")
        except Exception as e:
            logger.error(f"Could not delete media: {e}")


# ─────────────────────────────────────────────
# Register all handlers and run
# ─────────────────────────────────────────────

application = ApplicationBuilder().token(BOT_TOKEN).build()

# Core commands
application.add_handler(CommandHandler("start",      start,      filters=filters.ALL))
application.add_handler(CommandHandler("schedule",   schedule,   filters=filters.ALL))
application.add_handler(CommandHandler("guide",      guide,      filters=filters.ALL))
application.add_handler(CommandHandler("rules",      rules,      filters=filters.ALL))
application.add_handler(CommandHandler("about",      about,      filters=filters.ALL))

# Mentor tip commands
application.add_handler(CommandHandler("planning",   planning,   filters=filters.ALL))
application.add_handler(CommandHandler("strategy",   strategy,   filters=filters.ALL))
application.add_handler(CommandHandler("motivation", motivation, filters=filters.ALL))
application.add_handler(CommandHandler("resources",  resources,  filters=filters.ALL))
application.add_handler(CommandHandler("cutoff",     cutoff,     filters=filters.ALL))

# TO ADD A NEW COMMAND - copy these 2 lines and change the names:
# application.add_handler(CommandHandler("mycommand", my_function, filters=filters.ALL))

# Auto-filters
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_bad_words))
application.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.Document.ALL, filter_media))

print("Bot is running...")
application.run_polling()
