# SciAstra Telegram Bot — Setup Guide

## Files in this folder
```
bot.py           ← Main bot code (edit this to make changes)
requirements.txt ← Python packages needed
Procfile         ← Tells Railway how to run the bot
schedule.png     ← Your schedule image (ADD THIS YOURSELF)
```

---

## Step 1 — Test locally first

1. Install Python if you don't have it: https://python.org
2. Open terminal/command prompt in this folder
3. Run:
   ```
   pip install python-telegram-bot==20.7
   python bot.py
   ```
4. Open Telegram, find your bot, type /start
5. If it replies → working! Press Ctrl+C to stop

---

## Step 2 — Add your schedule image

- Rename your schedule image to: `schedule.png`
- Place it in the SAME folder as `bot.py`
- That's it! The bot will send this image when students type /schedule

### To update the schedule later:
- Just replace `schedule.png` with the new image (keep the same filename)
- Re-deploy on Railway (just push to GitHub again)

---

## Step 3 — Deploy on Railway (runs 24/7, FREE)

### 3a. Upload to GitHub
1. Create a free account at https://github.com
2. Create a new repository (name it `sciastra-bot`)
3. Upload all 4 files: `bot.py`, `requirements.txt`, `Procfile`, `schedule.png`

### 3b. Deploy on Railway
1. Go to https://railway.app
2. Sign up with your GitHub account
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your `sciastra-bot` repository
5. Railway will auto-detect Python and deploy it
6. Wait ~2 minutes → your bot is now online 24/7! ✅

### 3c. Verify it's running
- Open Telegram → type /start to your bot
- It should reply even with VS Code closed

---

## How to make changes later

### Update the schedule image:
1. Replace `schedule.png` in your GitHub repo
2. Railway auto-redeploys in ~1 minute

### Add a new command (example: /notes):
1. Open `bot.py`
2. Add this function (copy from existing ones):
   ```python
   async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
       await update.message.reply_text("📝 Notes will be shared soon!")
   ```
3. Register it near the bottom:
   ```python
   application.add_handler(CommandHandler("notes", notes))
   ```
4. Save → push to GitHub → Railway auto-updates

### Add more bad words:
1. Open `bot.py`
2. Find the `BAD_WORDS = [...]` list
3. Add your word in quotes with a comma: `"newword",`
4. Save and push to GitHub

---

## Bot Commands Summary

| Command    | What it does                          |
|------------|---------------------------------------|
| /start     | Welcome message + command list        |
| /schedule  | Sends the weekly timetable image      |
| /guide     | Tags @Sahil_sciastra for help         |
| /rules     | Shows group rules                     |
| /about     | About SciAstra group                  |

---

## Make the bot an admin in your group!
For auto-delete to work, you MUST:
1. Add the bot to your Telegram group
2. Go to group settings → Admins → Add Admin → select your bot
3. Enable: **Delete messages** permission

That's it — the bot will now delete bad messages automatically.
