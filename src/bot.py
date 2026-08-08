# ============================================
# THARKI MULTIBOT JSON (Fixed & Optimized)
# ============================================

import asyncio
import json
import os
import random
import time
import logging
import sys
from typing import Dict, Set, List
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import error as telegram_error
from gtts import gTTS
import io

# ============================================
# WINDOWS ASYNCIO FIX (Required for Windows RDP)
# ============================================
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )
    logging.info("⚙️ Windows event loop policy set (Selector)")

# ---------------------------
# CONFIG (UPDATED WITH YOUR TOKENS & OWNER)
# ---------------------------
TOKENS = [
    "8415930377:AAG7ikfjbzV9JdanDrsSnMfBFP6j-JfSBJU",
    "8628809540:AAFx9ZpQ1UGWrcgI82LFLKQb1L_YnrFufMk",
    "8928720021:AAFUQXUfLmGdCJEOaDOjtB6RWZoD6LNGcp4",
    "8839699728:AAEFwYbwp62f0f1uSkTfa-3A4mfOX4HXJVg",
    "8941290905:AAEm3M0-gohVKcqxi7nLU3AmJtTvCpyOx7A"
]

# Owner ID & Bot Name Configuration
OWNER_ID = 5769074791
SUDO_FILE = "sudo_users.json"
BOT_NAME_STYLE = "-*𝐓ʜᴀʀᴋɪ𝒃𝒂𝒛𝒛 - 𓂃 . ‹𝅮."

# ---------------------------
# RAID TEXT FORMATTING LISTS
# ---------------------------
EMOJI_LIST = [
    "Tᴇʀɪ Mᴀᴀ Cʜᴜᴅɪ ⎯‌⎯⃝𓆩⚚𓆪⎯‌⎯⃝⚰️",
    "Sᴀʟᴀᴍ Tʜᴏᴋ ⎯‌⎯⃝𓆩⚚𓆪⎯‌⎯⃝⚰️",
    "Cʜɪɴᴀᴀʀ ⎯‌⎯⃝𓆩⚚𓆪⎯‌⎯⃝⚰️",
    "Mᴀᴢᴅᴏᴏʀ ⎯‌⎯⃝𓆩⚚𓆪⎯‌⎯⃝⚰️",
    "Hᴀᴡᴀʙᴀᴢᴢ ⎯‌⎯⃝𓆩⚚𓆪⎯‌⎯⃝⚰️",
    "𝑻𝒉𝒂𝒓𝒌𝒊𝒃𝒂𝒛𝒛 ʙᴏʟ⎯‌⎯⃝𓆩⚚𓆪⎯‌⎯⃝⚰️",
    "Tᴍᴋʟ ⎯‌⎯⃝𓆩⚚𓆪⎯‌⎯⃝⚰️",
    "ᴋᴀᴍᴢᴏʀ Kᴜᴛɪʏᴀ ⎯‌⎯⃝𓆩⚚𓆪⎯‌⎯⃝⚰️",
    "Bʜᴇᴇᴋ Mᴀɴɢ ⎯‌⎯⃝𓆩⚚𓆪⎯‌⎯⃝⚰️",
    "RɴᴅɪMᴏɴ ⎯‌⎯⃝𓆩⚚𓆪⎯‌⎯⃝⚰️",
    "Cʜᴜᴅᴀɪ Kɪᴅᴅᴇ ⎯‌⎯⃝𓆩⚚𓆪⎯‌⎯⃝⚰️",
    "Gʜᴀᴛɪʏᴀ Bᴇᴛᴀ ⎯‌⎯⃝𓆩⚚𓆪⎯‌⎯⃝⚰️",
    "Tᴇʀᴀ Bᴀᴀᴘ 𝑻𝒉𝒂𝒓𝒌𝒊𝒃𝒂𝒛𝒛 ⎯‌⎯⃝𓆩⚚𓆪⎯‌⎯⃝⚰️",
    "GAɴᴅ Mᴀʀᴀ ᴍᴜʟʟᴇ ⎯‌⎯⃝𓆩⚚𓆪⎯‌⎯⃝⚰️",
    "Cʜᴜᴅᴇɢɪ TᴇʀɪMA ⎯‌⎯⃝𓆩⚚𓆪⎯‌⎯⃝⚰️",
]

RAID_TEXTS = [  
    "RND🕷️","BC🕷️","BKL🕷️","TBKL🕷️","MKL🕷️","CUD🕷️","TMKC🕷️","RO🕷️","CVR KR🕷️","HACLE🕷️",
    "🩷𝑻𝑴𝑲𝑪🩷","💕𝑩𝑯𝑬𝑵कालौड़ा💕","💚लंद𝑪𝑯𝑼𝑺💚","🤍𝑹𝑨𝑵डी़🤍","🩶बिहारी🩶","💙𝑮𝑼 𝑲𝑯𝑨𝑨💙","🖤मो𝑻𝑨𝑨🖤",
    "MADARCHOD 🎀","BHECHOD🎀","TERI MA RND 🎀","RNDY🎀","SUAR🎀","GU KHAA 🎀","LUN CHUS 🎀",
]

NCEMO_EMOJIS = [
    "𝐊ʏᴀ 𝐑ᴇ 𝐑ᴀɴᴅɪᴋᴇ 𝐂ᴏ𝐨ʟ 𝐁ᴀɴᴇɢᴀ 𝐓ᴜ 𝐂ʜᴀʟ 𝐀ʙ 𝐂ʜᴜᴅ 𝐀ᴘɴᴇ 𝐁ᴀᴀᴘ THARKIBAZZ 𝐒ᴇ - 🦢💘",
    "𝐊ɪ 𝐌ᴀᴀ 𝐌ᴀʀʀ 𝐆ᴀʏɪ 𝐘ᴀᴀʀ - 𝐉ᴀɪ THARKIBAZZ ! 🌙",
    "acha beta 😂🔥👊🏻 ? coi na me toh HATER codunga 😹💔🔥😆👊🏻💥",
    "chudke bhaga kaise 😂💥🤣🤘🏻",
]

SPAM_PATTERNS = ["[ any text ] 1-//--🩷🥀"]

voice_cache: Dict[tuple, bytes] = {}
pin_on_spam: Dict[int, bool] = {}
oneword_tasks: Dict[int, asyncio.Task] = {}
raid_tasks: Dict[int, asyncio.Task] = {}

shutdown_event: asyncio.Event | None = None

# Load or initialize SUDO users
if os.path.exists(SUDO_FILE):
    try:
        with open(SUDO_FILE, "r", encoding="utf-8") as f:
            _loaded = json.load(f)
            SUDO_USERS = set(int(x) for x in _loaded)
    except Exception:
        SUDO_USERS = {OWNER_ID}
else:
    SUDO_USERS = {OWNER_ID}

def save_sudo():
    with open(SUDO_FILE, "w", encoding="utf-8") as f:
        json.dump(list(SUDO_USERS), f)

group_tasks: Dict[int, Dict[str, asyncio.Task]] = {}
nc_tasks: Dict[int, List[asyncio.Task]] = {}
nc_counters: Dict[int, int] = {}
nc_modes: Dict[int, str] = {}
spam_tasks: Dict[int, asyncio.Task] = {}
voice_tasks: Dict[int, asyncio.Task] = {}
apps, bots = [], []
delay = 0.3
MIN_DELAY = 0.05
MAX_DELAY = 60.0

logging.basicConfig(level=logging.INFO)

def only_sudo(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user:
            return
        uid = update.effective_user.id
        if uid not in SUDO_USERS and uid != OWNER_ID:
            return await update.message.reply_text("🌙 OYY GRIB KE BACHE TERI MAA KA LODAA🩷")
        return await func(update, context)
    return wrapper

def only_owner(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.effective_user:
            return
        uid = update.effective_user.id
        if uid != OWNER_ID:
            return await update.message.reply_text("🤍 BOOLLLLL THARKIBAZZ PAPAAA TAB MILEGA SUDO ")
        return await func(update, context)
    return wrapper

# Worker Functions (Count based & Target Tagging)
async def oneword_loop_count(update: Update, target: str, count: int):
    try:
        sent = 0
        while not shutdown_event.is_set() and sent < count:
            for word in RAID_TEXTS:
                if shutdown_event.is_set() or sent >= count:
                    break
                msg_text = f"{target} {word}"
                await update.message.reply_text(msg_text)
                sent += 1
                await asyncio.sleep(max(MIN_DELAY, min(delay, MAX_DELAY)))
    except asyncio.CancelledError:
        pass

async def raid_loop_count(update: Update, target: str, count: int):
    try:
        sent = 0
        while not shutdown_event.is_set() and sent < count:
            for emoji in EMOJI_LIST:
                for raid in RAID_TEXTS:
                    if shutdown_event.is_set() or sent >= count:
                        break
                    full_text = f"{emoji} {target} {raid}"
                    await update.message.reply_text(full_text)
                    sent += 1
                    await asyncio.sleep(max(MIN_DELAY, min(delay, MAX_DELAY)))
    except asyncio.CancelledError:
        pass

async def _staggered_nc_worker(bot, chat_id: int, base_text: str, mode: str, counter_dict: Dict, bot_index: int):
    startup_delay = bot_index * 0.1
    if startup_delay > 0:
        try:
            await asyncio.sleep(startup_delay)
        except:
            return
    await nc_worker(bot, chat_id, base_text, mode, counter_dict)

async def nc_worker(bot, chat_id: int, base_text: str, mode: str, counter_dict: Dict):
    global shutdown_event
    emoji_len = len(EMOJI_LIST)
    ncemo_len = len(NCEMO_EMOJIS)
    try:

     # Fix update

        while not shutdown_event.is_set():
            try:
                styled_base = f"{base_text} {BOT_NAME_STYLE}"
                if mode == "emoji":
                    text = f"{styled_base} {NCEMO_EMOJIS[random.randint(0, ncemo_len - 1)]}"
                else:
                    text = f"{EMOJI_LIST[random.randint(0, emoji_len - 1)]} {styled_base}"
                await bot.set_chat_title(chat_id, text)
                counter_dict[chat_id] = counter_dict.get(chat_id, 0) + 1
            except telegram_error.Forbidden:
                return
            except asyncio.CancelledError:
                break
            except:
                pass
    except:
        pass

async def spam_loop(update, context, text):
    global shutdown_event, pin_on_spam
    chat_id = update.message.chat_id
    i = 0
    bot = context.bot
    try:
        while not shutdown_event.is_set():
            try:
                spam_pattern = SPAM_PATTERNS[i % len(SPAM_PATTERNS)]
                spam_text = spam_pattern.replace("[ any text ]", text)
                msg = await update.message.reply_text(spam_text)
                if pin_on_spam.get(chat_id, False) and msg:
                    try:
                        await bot.pin_chat_message(chat_id=chat_id, message_id=msg.message_id, disable_notification=True)
                    except:
                        pass
                i += 1
                await asyncio.sleep(max(MIN_DELAY, min(delay, MAX_DELAY)))
            except asyncio.CancelledError:
                break
            except:
                await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        pass

async def voice_loop(bot, chat_id: int, text: str):
    global shutdown_event, voice_cache
    cache_key = (chat_id, text)
    try:
        if cache_key not in voice_cache:
            try:
                tts = gTTS(text=text, lang='en')
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                voice_cache[cache_key] = audio_bytes.getvalue()
            except:
                return
        cached_voice = voice_cache[cache_key]
        while not shutdown_event.is_set():
            try:
                voice_io = io.BytesIO(cached_voice)
                await bot.send_voice(chat_id=chat_id, voice=voice_io)
                await asyncio.sleep(max(MIN_DELAY, min(delay, MAX_DELAY)))
            except asyncio.CancelledError:
                break
            except:
                await asyncio.sleep(0.1)
    except:
        pass

# Commands
@only_owner
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"✨ {BOT_NAME_STYLE} BOT STARTED! Type /help for commands.")

@only_sudo
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    HELP_TEXT = (
f"🔥 {BOT_NAME_STYLE} 🔥\n"
f"👑 Owner: @ix_aura\n\n"
"[ 🤍 SYSTEM 🤍 ]\n"
"● ~ping, ~myid, ~delay <sec>\n\n"
"[ 🩷 NAME CHAOS & RAID 🩷 ]\n"
"● ~ncloop <text>\n"
"● ~oneword <target> <count> ⚡\n"
"● ~raid <target> <count> 💥\n"
"● ~stopgcnc, ~stoponeword, ~stopraid, ~stopall\n\n"
"[ 🖤 SPAM & VOICE 🖤 ]\n"
"● ~spamloop <text>\n"
"● ~voice <text>, ~stopvoice, ~stopspam\n"
"━━━━━━━━━━━━━━━━━━\n"
f"⚡ @ix_aura ⚡"
    )
    await update.message.reply_text(HELP_TEXT)

@only_sudo
async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    msg = await update.message.reply_text("🏓 Pinging...")
    latency = int((time.time() - start_time) * 1000)
    await msg.edit_text(f"🏓 Pong! ✅ {latency} ms")

@only_sudo
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Your ID: {update.effective_user.id} | Username: @ix_aura")

@only_sudo
async def oneword_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    target = ""
    count = 5 # Default count if not given

    if update.message.reply_to_message:
        target = f"@{update.message.reply_to_message.from_user.username}" if update.message.reply_to_message.from_user.username else update.message.reply_to_message.from_user.first_name
        if args and args[0].isdigit():
            count = int(args[0])
    elif len(args) >= 2:
        target = args[0]
        if args[1].isdigit():
            count = int(args[1])
    elif len(args) == 1:
        if args[0].isdigit():
            count = int(args[0])
            target = f"@{update.effective_user.username}" if update.effective_user.username else update.effective_user.first_name
        else:
            target = args[0]
    else:
        return await update.message.reply_text("⚠️ Usage: ~oneword <target/username> <count> (or reply to user)")

    chat_id = update.message.chat_id
    if chat_id in oneword_tasks:
        oneword_tasks[chat_id].cancel()
    oneword_tasks[chat_id] = asyncio.create_task(oneword_loop_count(update, target, count))
    await update.message.reply_text(f"⚡ OneWord spam started on {target} ({count} times)")

@only_sudo
async def stop_oneword_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in oneword_tasks:
        oneword_tasks[chat_id].cancel()
        oneword_tasks.pop(chat_id)
        await update.message.reply_text("🛑 OneWord spam stopped.")
    else:
        await update.message.reply_text("❌ No OneWord spam running.")

@only_sudo
async def raid_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    target = ""
    count = 5 # Default count if not given

    if update.message.reply_to_message:
        target = f"@{update.message.reply_to_message.from_user.username}" if update.message.reply_to_message.from_user.username else update.message.reply_to_message.from_user.first_name
        if args and args[0].isdigit():
            count = int(args[0])
    elif len(args) >= 2:
        target = args[0]
        if args[1].isdigit():
            count = int(args[1])
    elif len(args) == 1:
        if args[0].isdigit():
            count = int(args[0])
            target = f"@{update.effective_user.username}" if update.effective_user.username else update.effective_user.first_name
        else:
            target = args[0]
    else:
        return await update.message.reply_text("⚠️ Usage: ~raid <target/username> <count> (or reply to user)")

    chat_id = update.message.chat_id
    if chat_id in raid_tasks:
        raid_tasks[chat_id].cancel()
    raid_tasks[chat_id] = asyncio.create_task(raid_loop_count(update, target, count))
    await update.message.reply_text(f"💥 Heavy Raid started on {target} ({count} times)")

@only_sudo
async def stop_raid_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in raid_tasks:
        raid_tasks[chat_id].cancel()
        raid_tasks.pop(chat_id)
        await update.message.reply_text("🛑 Heavy Raid stopped.")
    else:
        await update.message.reply_text("❌ No Heavy Raid running.")

@only_owner
async def voice_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: ~voice <text>")
    text = " ".join(context.args)
    chat_id = update.message.chat_id
    if chat_id in voice_tasks:
        try:
            voice_tasks[chat_id].cancel()
        except:
            pass
    if not bots:
        return await update.message.reply_text("❌ No bots available")
    voice_tasks[chat_id] = asyncio.create_task(voice_loop(bots[0], chat_id, text))
    await update.message.reply_text(f"🎤 Voice loop started: '{text}'")

@only_sudo
async def stopvoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in voice_tasks:
        voice_tasks[chat_id].cancel()
        del voice_tasks[chat_id]
        await update.message.reply_text("🛑 Voice loop stopped.")
    else:
        await update.message.reply_text("❌ No voice loop running.")

@only_sudo
async def gcnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: ~ncloop <text>")
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    user_id = update.effective_user.id
    if not bots:
        return await update.message.reply_text("❌ No bots available")
    if chat_id not in nc_tasks:
        nc_counters[chat_id] = 0
        nc_modes[chat_id] = "raid"
        group_tasks.setdefault(chat_id, {})
        nc_tasks[chat_id] = []
        for idx, bot in enumerate(bots):
            key = getattr(bot, "token", str(id(bot)))
            if key not in group_tasks[chat_id]:
                task = asyncio.create_task(_staggered_nc_worker(bot, chat_id, base, "raid", nc_counters, idx))
                nc_tasks[chat_id].append(task)
                group_tasks[chat_id][key] = task
    await update.message.reply_text("✅ NC GROUP LOOP STARTED")

@only_sudo
async def stopgcnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        for task in group_tasks[chat_id].values():
            task.cancel()
        group_tasks[chat_id] = {}
        nc_tasks.pop(chat_id, None)
        await update.message.reply_text("🛑 NC Loop Stopped.")
    else:
        await update.message.reply_text("❌ No NC loop running.")

@only_sudo
async def stopall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for chat_id in list(group_tasks.keys()):
        for task in group_tasks[chat_id].values():
            task.cancel()
        group_tasks[chat_id] = {}
    oneword_tasks.clear()
    raid_tasks.clear()
    spam_tasks.clear()
    voice_tasks.clear()
    await update.message.reply_text("⏹ All loops & raids stopped.")

@only_sudo
async def delay_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global delay
    if not context.args:
        return await update.message.reply_text(f"⏱ Current delay: {delay}s")
    try:
        delay = max(MIN_DELAY, min(float(context.args[0]), MAX_DELAY))
        await update.message.reply_text(f"✅ Delay set to {delay}s")
    except:
        await update.message.reply_text("⚠️ Invalid number.")

@only_owner
async def addsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
    elif context.args:
        try:
            uid = int(context.args[0])
        except ValueError:
            return await update.message.reply_text("⚠️ Invalid User ID format.")
    else:
        return await update.message.reply_text("⚠️ Usage: Reply to a user or provide user ID to add sudo.")
    
    SUDO_USERS.add(uid)
    save_sudo()
    await update.message.reply_text(f"✅ {uid} added as SUDO.")

@only_owner
async def delsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
    elif context.args:
        try:
            uid = int(context.args[0])
        except ValueError:
            return await update.message.reply_text("⚠️ Invalid User ID format.")
    else:
        return await update.message.reply_text("⚠️ Usage: Reply to a user or provide user ID to remove sudo.")
    
    if uid in SUDO_USERS:
        SUDO_USERS.remove(uid)
        save_sudo()
        await update.message.reply_text(f"🗑 {uid} removed from SUDO.")
    else:
        await update.message.reply_text("❌ User is not in SUDO list.")

@only_sudo
async def spamloop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: ~spamloop <text>")
    text = " ".join(context.args)
    chat_id = update.message.chat_id
    if chat_id in spam_tasks:
        spam_tasks[chat_id].cancel()
    spam_tasks[chat_id] = asyncio.create_task(spam_loop(update, context, text))
    await update.message.reply_text("🔄 Spam loop started.")

@only_sudo
async def stopspam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in spam_tasks:
        spam_tasks[chat_id].cancel()
        spam_tasks.pop(chat_id)
        await update.message.reply_text("🛑 Spam stopped.")
    else:
        await update.message.reply_text("❌ No spam running.")

# Universal Handler Router
async def universal_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        if not text.startswith("~"):
            return
        parts = text[1:].split(None, 1)
        if not parts:
            return
        command = parts[0].lower()
        args_str = parts[1] if len(parts) > 1 else ""
        context.args = args_str.split() if args_str else []
        
        handlers = {
            "start": start_cmd,
            "help": help_cmd,
            "ping": ping_cmd,
            "myid": myid,
            "voice": voice_cmd,
            "stopvoice": stopvoice,
            "ncloop": gcnc,
            "stopgcnc": stopgcnc,
            "oneword": oneword_cmd,
            "stoponeword": stop_oneword_cmd,
            "raid": raid_cmd,
            "stopraid": stop_raid_cmd,
            "stopall": stopall,
            "delay": delay_cmd,
            "addsudo": addsudo,
            "delsudo": delsudo,
            "spamloop": spamloop,
            "stopspam": stopspam,
        }
        
        if command in handlers:
               await handlers[command] (update, context) 
                       
    except Exception as e:
        logging.error(f"Error: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update caused error: {context.error}")

def build_app(token):
    app = Application.builder().token(token).build()
    app.add_error_handler(error_handler)
    app.add_handler(MessageHandler(filters.Regex(r"^~\w"), universal_command_handler))
    return app

async def run_all_bots():
    global shutdown_event, apps, bots
    shutdown_event = asyncio.Event()
    
    seen = set()
    for t in TOKENS:
        if t and t not in seen:
            seen.add(t)
            try:
                app = build_app(t)
                apps.append(app)
                bots.append(app.bot)
            except Exception as e:
                logging.error(f"Failed building app: {e}")

    for idx, app in enumerate(apps):
        try:
            await app.initialize()
            await app.start()
            await app.updater.start_polling()
            logging.info(f"✅ Bot {idx + 1} started (@ix_aura)")
            await asyncio.sleep(0.3)
        except Exception as e:
            logging.error(f"Failed starting bot {idx + 1}: {e}")

    await shutdown_event.save() if hasattr(shutdown_event, 'save') else await shutdown_event.wait()

def main():
    try:
        asyncio.run(run_all_bots())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import threading

    class SimpleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is alive and running!")

    def run_server():
        port = int(os.environ.get("PORT", 10000))
        server = HTTPServer(("0.0.0.0", port), SimpleHandler)
        server.serve_forever()

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    main()
