# ------------------------------------------------------------------------------
# OpenClaw: The Mobile AI Agent Gateway (Grok Intelligence Integrated)
# ------------------------------------------------------------------------------
import os
import sys
import logging
import asyncio
import subprocess
import re
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from datetime import datetime
from openai import OpenAI

# CONFIGURATION
TOKEN = "8571904781:AAEhaViQiEihWOHShd0a0ywJ0BMufSh13p8"
PORTFOLIO_DIR = "/home/nishan/portfolio"
ADMIN_FILE = os.path.join(PORTFOLIO_DIR, "admin_id.txt")
CONFIG_FILE = os.path.join(PORTFOLIO_DIR, "claw_config.json")

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("OpenClaw")

# Debug log for server startup
DEBUG_LOG = os.path.join(PORTFOLIO_DIR, "bot_health.log")
with open(DEBUG_LOG, 'a') as f: f.write(f"\n[{datetime.now()}] Bot Script Started\n")


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f: return json.load(f)
        except Exception as e:
            logger.error(f"Config load error: {e}")
    return {"grok_key": None}

def get_admin():
    if os.path.exists(ADMIN_FILE):
        try:
            with open(ADMIN_FILE, 'r') as f: return int(f.read().strip())
        except: return None
    return None

def get_grok_client():
    config = load_config()
    key = config.get("grok_key")
    if key:
        return OpenAI(api_key=key, base_url="https://api.x.ai/v1")
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    admin = get_admin()
    
    if not admin:
        with open(ADMIN_FILE, 'w') as f: f.write(str(user_id))
        admin = user_id
    
    if user_id != admin:
        await update.message.reply_text("⛔ Security Lock Active.")
        return

    kb = [["📊 Status", "🧼 Clean"], ["🎯 Sync Challenge", "📖 Help"]]
    markup = ReplyKeyboardMarkup(kb, resize_keyboard=True)
    await update.message.reply_text(
        "🚀 **OpenClaw Multi-Agent Command Center Online.**\n\n"
        "I am your dedicated **Mobile Agent/Analytical Assistant**. Grok Intelligence is now active.\n\n"
        "⚡ **Capabilities:**\n"
        "- **Chat**: Just type! (Powered by Grok)\n"
        "- **Shell**: `$ [cmd]` (e.g. `$ ls -la`)\n"
        "- **Python**: ```python [code] ```\n"
        "- **Image**: Send photos for surgical cleaning and sync.",
        reply_markup=markup, parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    admin = get_admin()
    
    if not admin:
        with open(ADMIN_FILE, 'w') as f: f.write(str(user_id))
        admin = user_id

    if user_id != admin: return
    
    text = update.message.text
    if not text: return
    logger.info(f"Received: {text}")

    # 1. Shell Command Handler ($)
    if text.startswith("$"):
        cmd = text[1:].strip()
        await update.message.reply_text(f"🐚 **Running Shell...**\n`{cmd}`", parse_mode='Markdown')
        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            output = (res.stdout + res.stderr).strip() or "[No Output]"
            await update.message.reply_text(f"🏁 **Output:**\n```\n{output[:3500]}\n```", parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
        return

    # 2. Python Code Execution
    if "```" in text:
        code = re.sub(r'```python|```', '', text).strip()
        await update.message.reply_text("🐍 **Executing Python...**", parse_mode='Markdown')
        try:
            tmp_file = f"/tmp/claw_exec_{datetime.now().strftime('%H%M%S')}.py"
            with open(tmp_file, 'w') as f: f.write(code)
            res = subprocess.run([sys.executable, tmp_file], capture_output=True, text=True, timeout=15)
            output = (res.stdout + res.stderr).strip() or "[No Output]"
            await update.message.reply_text(f"📝 **Result:**\n```\n{output[:3500]}\n```", parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
        return

    # 3. Quick Actions
    if text.lower() in ["status", "📊 status"]:
        res = subprocess.check_output("uptime && free -h", shell=True).decode()
        await update.message.reply_text(f"🖥️ **Server Vitals:**\n\n```\n{res}\n```", parse_mode='Markdown')
        return

    if text.lower() in ["clean", "🧼 clean"]:
        await update.message.reply_text("🧼 **Starting Deep Surgical Cleanup...**")
        subprocess.Popen([sys.executable, f"{PORTFOLIO_DIR}/image_processor.py"])
        return

    # 4. Grok Intelligence (Natural Language)
    client = get_grok_client()
    if not client:
        await update.message.reply_text("⚠️ **Grok Intelligence is not configured.**\nUse /set_grok [key] to activate the brain.")
        return

    status_msg = await update.message.reply_text("🤔 **Grok is thinking...**")
    try:
        response = client.chat.completions.create(
            model="grok-2",
            messages=[
                {"role": "system", "content": "You are the OpenClaw AI Hub, a professional and analytical assistant. You assist the user with server management, coding, and general intelligence. Keep responses concise and focused on the technical goal."},
                {"role": "user", "content": text}
            ]
        )
        ai_reply = response.choices[0].message.content
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=status_msg.message_id, text=ai_reply)
    except Exception as e:
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=status_msg.message_id, text=f"❌ Grok Error: {e}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    admin = get_admin()
    if user_id != admin: return
    
    msg_id = update.message.message_id
    logger.info(f"📸 Received photo update (MSG: {msg_id})")
    await update.message.reply_text(f"📸 **Image {msg_id} Detected.** Queuing for processing...")
    
    try:
        from ocr_helper import extract_challenge_info
        from image_processor import clean_image
        
        # Get highest resolution
        photo = update.message.photo[-1]
        f = await context.bot.get_file(photo.file_id)
        
        # Unique paths per message
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_filename = f"sync_{ts}_{msg_id}.jpg"
        temp_path = os.path.join(PORTFOLIO_DIR, "static", "images", temp_filename)
        
        logger.info(f"Downloading photo {msg_id} to {temp_path}")
        await f.download_to_drive(temp_path)
        
        # Offload blocking operations to executor
        loop = asyncio.get_event_loop()
        
        logger.info(f"Starting OCR/Clean for {msg_id}")
        date_id, title = await loop.run_in_executor(None, extract_challenge_info, temp_path)
        await loop.run_in_executor(None, clean_image, temp_path)
        
        target_date = date_id or datetime.now().strftime("%Y-%m-%d")
        logger.info(f"Photo {msg_id} processed. Date: {target_date}, Title: {title}")
        
        # Rename to target format
        final_filename = f"{target_date.replace('-', '')}_{msg_id}_sync.jpg"
        final_path = os.path.join(PORTFOLIO_DIR, "static", "images", final_filename)
        os.rename(temp_path, final_path)
        
        # DB Sync via Subprocess (keeping it simple for now)
        db_script = f"""
import sys
sys.path.append('{PORTFOLIO_DIR}')
from app import app, db, Challenge
with app.app_context():
    challenge = Challenge.query.filter_by(date_id='{target_date}').first()
    if not challenge: challenge = Challenge(date_id='{target_date}', title='{title or "Daily Challenge"}')
    challenge.image_path = '{final_filename}'
    db.session.add(challenge)
    db.session.commit()
"""
        await loop.run_in_executor(None, lambda: subprocess.run([sys.executable, "-c", db_script]))
        
        await update.message.reply_text(f"✅ **Challenge Synced!** (ID: {msg_id})\nDate: `{target_date}`\nWebsite updated. 🚀")
        logger.info(f"✅ Photo {msg_id} sync complete.")
        
    except Exception as e:
        logger.error(f"❌ Pipeline Error for {msg_id}: {e}", exc_info=True)
        await update.message.reply_text(f"❌ **Pipeline Error ({msg_id}):** {e}")

async def set_grok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != get_admin(): return
    if not context.args: return
    key = context.args[0]
    with open(CONFIG_FILE, 'w') as f: json.dump({"grok_key": key}, f)
    await update.message.reply_text("✅ **Grok Intelligence Key Set.** Brain activated! 🦾")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("set_grok", set_grok))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    logger.info("OpenClaw Agent Hub Online.")
    with open(DEBUG_LOG, 'a') as f: f.write(f"[{datetime.now()}] Entering app.run_polling()\n")
    app.run_polling()
