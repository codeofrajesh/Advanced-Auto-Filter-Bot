import string
import random
import asyncio
from info import ADMINS
from pyrogram import Client, filters, StopPropagation
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_chats_db import db

# The Native State Machine
BATCH_STATE = {}

def parse_link(link):
    try:
        link = link.split("?")[0]
        if "t.me/c/" in link:
            parts = link.split("/")
            chat_id = int("-100" + parts[-2])
            msg_id = int(parts[-1])
            return chat_id, msg_id
        elif "t.me/" in link:
            parts = link.split("/")
            chat_id = parts[-2]
            msg_id = int(parts[-1])
            return chat_id, msg_id
    except Exception:
        pass
    return None, None

def gen_hash():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=7))

def get_admin_buttons(bot):
    # Generates Telegram's native "Add Bot to Chat" buttons
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add to Channel", url=f"https://t.me/{bot.me.username}?startchannel=true")],
        [InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{bot.me.username}?startgroup=true")]
    ])

async def verify_access(bot, message, chat_id, msg_id):
    try:
        msg = await bot.get_messages(chat_id, msg_id)
        if msg.empty: raise Exception("Empty")
        return True
    except Exception:
        await message.reply("❌ <b>I cannot access that message.</b>\nMake sure I am an admin in that channel/group. Click below to add me:", reply_markup=get_admin_buttons(bot))
        return False
    

# --- Single Link Command ---
@Client.on_message(filters.command("link") & filters.private & filters.user(ADMINS))
async def single_link_generator(bot, message):
    if len(message.command) < 2:
        return await message.reply("⚠️ Usage: <code>/link [message_link]</code>")
    
    chat_id, msg_id = parse_link(message.command[1])
    if not msg_id:
        await message.reply("❌ Invalid Telegram Link.")
        raise StopPropagation

    if not await verify_access(bot, message, chat_id, msg_id):
        raise StopPropagation
        
    try:
        msg = await bot.get_messages(chat_id, msg_id)
        if msg.empty: raise Exception("Empty")
    except Exception:
        return await message.reply("❌ I cannot access that message. Make sure I am an admin in that channel.")

    hash_id = gen_hash()
    await db.save_store_hash(hash_id, [{"chat_id": chat_id, "msg_id": msg_id}])
    
    bot_info = await bot.get_me()
    deep_link = f"https://t.me/{bot_info.username}?start=store_{hash_id}"
    text = f"""<b>╭─[ 🔗 ꜰɪʟᴇ ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ]─⍟
├ 📂 ꜱᴛᴀᴛᴜꜱ : ✅ ꜱᴜᴄᴄᴇꜱꜱ
├ 🔢 ꜰɪʟᴇꜱ : 1 ꜰɪʟᴇ
├ 🪪 ʜᴀꜱʜ ɪᴅ : <code>{hash_id}</code>
╰──────────────────────⍟

<blockquote>📥 ʏᴏᴜʀ ꜱᴇᴄᴜʀᴇ ᴅᴇᴇᴘ ʟɪɴᴋ:
<code>{deep_link}</code></blockquote></b>"""

    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("📤 ꜱʜᴀʀᴇ ʟɪɴᴋ", url=f"https://t.me/share/url?url={deep_link}&text=Here%20is%20your%20secure%20file%20link!")],
        [InlineKeyboardButton("🗑️ ʀᴇᴠᴏᴋᴇ ʟɪɴᴋ", callback_data=f"revokelink_{hash_id}")]
    ])
    
    await message.reply(text, disable_web_page_preview=True, reply_markup=btn)
    raise StopPropagation

# --- 3-Option Batch Command ---
@Client.on_message(filters.command("batch") & filters.private& filters.user(ADMINS))
async def batch_generator(bot, message):
    text = """<b>╭─[ 📦 ʙᴀᴛᴄʜ ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴏʀ ]─⍟
├ 💡 ꜱᴇʟᴇᴄᴛ ᴀ ᴍᴇᴛʜᴏᴅ ᴛᴏ ᴄʟᴜꜱᴛᴇʀ
├ ᴍᴜʟᴛɪᴘʟᴇ ꜰɪʟᴇꜱ ɪɴᴛᴏ ᴀ ꜱɪɴɢʟᴇ
├ ꜱᴇᴄᴜʀᴇ ᴅᴇᴇᴘ ʟɪɴᴋ.
╰──────────────────────⍟</b>"""
    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔢 Message Count", callback_data="batch_count")],
        [InlineKeyboardButton("🔗 Start & End Link", callback_data="batch_range")],
        [InlineKeyboardButton("✍️ Manual Entry", callback_data="batch_manual")]
    ])
    await message.reply(text, reply_markup=btn)
    raise StopPropagation

@Client.on_callback_query(filters.regex(r"^batch_"))
async def batch_callbacks(bot, query):
    action = query.data.split("_")[1]
    user_id = query.from_user.id
    
    if action == "count":
        BATCH_STATE[user_id] = {"mode": "count", "step": 1}
        await query.message.edit_text("🔗 Send the link of the <b>FIRST</b> message:")
    elif action == "range":
        BATCH_STATE[user_id] = {"mode": "range", "step": 1}
        await query.message.edit_text("🔗 Send the link of the <b>FIRST</b> message:")
    elif action == "manual":
        BATCH_STATE[user_id] = {"mode": "manual", "files": []}
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Done", callback_data="manual_done")]])
        prompt = await query.message.edit_text("✍️ Send me message links one by one.\nClick <b>Done</b> when finished.", reply_markup=btn)
        BATCH_STATE[user_id]["prompt_id"] = prompt.id

# --- Native Conversation Listener ---
@Client.on_message(filters.private & filters.text & ~filters.command(["link", "batch", "cancel", "start"]))
async def native_conversation_listener(bot, message):
    user_id = message.from_user.id
    
    if user_id not in BATCH_STATE:
        message.continue_propagation()
        return
        
    state = BATCH_STATE[user_id]
    
    if state["mode"] == "count":
        if state["step"] == 1:
            c_id, msg_id = parse_link(message.text)
            if not msg_id: return await message.reply("❌ Invalid link. Try again:")
            if not await verify_access(bot, message, c_id, msg_id):
                raise StopPropagation
            state["c_id"] = c_id
            state["start_msg_id"] = msg_id
            state["step"] = 2
            await message.reply("🔢 How many messages do you want to fetch after this? (e.g., 10)")
        elif state["step"] == 2:
            if not message.text.isdigit(): return await message.reply("❌ Send a valid number:")
            count = int(message.text)
            file_data = [{"chat_id": state["c_id"], "msg_id": i} for i in range(state["start_msg_id"], state["start_msg_id"] + count)]
            await finalize_batch(bot, message, user_id, file_data)
            
    elif state["mode"] == "range":
        if state["step"] == 1:
            c_id, msg_id = parse_link(message.text)
            if not msg_id: return await message.reply("❌ Invalid link. Try again:")
            if not await verify_access(bot, message, c_id, msg_id):
                raise StopPropagation
            state["c_id"] = c_id
            state["start_msg_id"] = msg_id
            state["step"] = 2
            await message.reply("🔗 Send the link of the <b>LAST</b> message:")
        elif state["step"] == 2:
            _, end_msg_id = parse_link(message.text)
            if not end_msg_id: return await message.reply("❌ Invalid link. Try again:")
            file_data = [{"chat_id": state["c_id"], "msg_id": i} for i in range(state["start_msg_id"], end_msg_id + 1)]
            await finalize_batch(bot, message, user_id, file_data)
            
    elif state["mode"] == "manual":
        c_id, msg_id = parse_link(message.text)
        await message.delete() 
        if not c_id:
            await message.reply("❌ Invalid link.")
            raise StopPropagation
            
        if not await verify_access(bot, message, c_id, msg_id):
            raise StopPropagation
            
        state["files"].append({"chat_id": c_id, "msg_id": msg_id})
        btn = InlineKeyboardMarkup([[InlineKeyboardButton("✅ Done", callback_data="manual_done")]])
        try:
            await bot.edit_message_text(user_id, state["prompt_id"], f"✅ Accepted {len(state['files'])} links.\nSend next or click Done.", reply_markup=btn)
        except Exception:
            pass

    raise StopPropagation
@Client.on_callback_query(filters.regex(r"^manual_done"))
async def manual_done_callback(bot, query):
    user_id = query.from_user.id
    if user_id in BATCH_STATE and BATCH_STATE[user_id]["mode"] == "manual":
        await finalize_batch(bot, query.message, user_id, BATCH_STATE[user_id]["files"])

async def finalize_batch(bot, message, user_id, file_data):
    del BATCH_STATE[user_id] 
    
    if not file_data:
        return await message.reply("❌ Operation cancelled. No valid links provided.")

    hash_id = gen_hash()
    await db.save_store_hash(hash_id, file_data)
    
    bot_info = await bot.get_me()
    deep_link = f"https://t.me/{bot_info.username}?start=store_{hash_id}"
    text = f"""<b>╭─[ 📦 ʙᴀᴛᴄʜ ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ]─⍟
├ 📂 ꜱᴛᴀᴛᴜꜱ : ✅ ꜱᴜᴄᴄᴇꜱꜱ
├ 🔢 ꜰɪʟᴇꜱ : {len(file_data)} ꜰɪʟᴇ(ꜱ)
├ 🪪 ʜᴀꜱʜ ɪᴅ : <code>{hash_id}</code>
╰──────────────────────⍟

<blockquote>📥 ʏᴏᴜʀ ꜱᴇᴄᴜʀᴇ ᴅᴇᴇᴘ ʟɪɴᴋ:
<code>{deep_link}</code></blockquote></b>"""

    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("📤 ꜱʜᴀʀᴇ ʟɪɴᴋ", url=f"https://t.me/share/url?url={deep_link}&text=Here%20is%20your%20secure%20file%20batch!")],
        [InlineKeyboardButton("🗑️ ʀᴇᴠᴏᴋᴇ ʟɪɴᴋ", callback_data=f"revokelink_{hash_id}")]
    ])
    
    await message.reply(text, disable_web_page_preview=True, reply_markup=btn)

@Client.on_message(filters.command("linkslist") & filters.private & filters.user(ADMINS))
async def list_active_links(bot, message):
    hashes = await db.get_all_store_hashes()
    
    if not hashes:
        await message.reply("<b>╭─[ 🗄️ ᴀᴄᴛɪᴠᴇ ꜰɪʟᴇ ꜱᴛᴏʀᴇ ʟɪɴᴋꜱ ]─⍟\n├ 📂 ꜱᴛᴀᴛᴜꜱ : ᴇᴍᴘᴛʏ (0 ʟɪɴᴋꜱ)\n╰──────────────────────⍟</b>")
        raise StopPropagation
        
    bot_info = await bot.get_me()
    text = f"<b>╭─[ 🗄️ ᴀᴄᴛɪᴠᴇ ꜰɪʟᴇ ʟɪɴᴋꜱ ({len(hashes)}) ]─⍟\n</b>"
    
    for idx, h in enumerate(hashes, 1):
        hash_id = h['hash']
        files_count = len(h['files'])
        link = f"https://t.me/{bot_info.username}?start=store_{hash_id}"
        
        # Premium Formatting
        text += f"<b>├ 📦 <code>{files_count}</code> ꜰɪʟᴇ(ꜱ) | 🪪 <code>{hash_id}</code>\n</b>"
        text += f"<b>├ 🔗 <code>{link}</code>\n</b>"
        
        # Add a subtle separator between links, except for the last one
        if idx < len(hashes):
            text += "<b>├ ┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈\n</b>"
            
    text += "<b>╰──────────────────────⍟\n\n💡 <i>ᴛᴀᴘ ᴀɴʏ ʟɪɴᴋ ᴏʀ ʜᴀꜱʜ ᴛᴏ ᴄᴏᴘʏ ɪᴛ!</i></b>"
    
    # Send in chunks if the list gets massive (Telegram has a 4096 character limit)
    if len(text) > 4000:
        for x in range(0, len(text), 4000):
            await message.reply(text[x:x+4000], disable_web_page_preview=True)
    else:
        await message.reply(text, disable_web_page_preview=True)
        
    raise StopPropagation

# --- Revoke a Link ---
@Client.on_message(filters.command("revoke") & filters.private & filters.user(ADMINS))
async def revoke_link(bot, message):
    if len(message.command) < 2:
        await message.reply("⚠️ Usage: <code>/revoke [hash_id_or_link]</code>")
        raise StopPropagation
        
    input_str = message.command[1]
    if "start=store_" in input_str:
        hash_id = input_str.split("start=store_")[1]
    else:
        hash_id = input_str
    data = await db.get_store_hash(hash_id)
    if not data:
        await message.reply("❌ <b>Hash or Link not found or already deleted.</b>")
        raise StopPropagation
        
    await db.delete_store_hash(hash_id)
    await message.reply(f"✅ <b>Link Revoked!</b>\nHash <code>{hash_id}</code> has been permanently wiped from the database.")
    raise StopPropagation

# --- Inline Revoke Button Handler ---
@Client.on_callback_query(filters.regex(r"^revokelink_"))
async def inline_revoke_cb(bot, query):
    if query.from_user.id not in ADMINS:
        return await query.answer("⚠️ Admin only!", show_alert=True)
        
    hash_id = query.data.split("_")[1]
    data = await db.get_store_hash(hash_id)
    
    if not data:
        return await query.answer("❌ Hash not found or already deleted.", show_alert=True)
        
    await db.delete_store_hash(hash_id)
    
    # Edits the message to visually show it was destroyed
    await query.message.edit_text(
        f"<b>╭─[ 🗑️ ʟɪɴᴋ ʀᴇᴠᴏᴋᴇᴅ ]─⍟\n├ 🪪 ʜᴀꜱʜ ɪᴅ : <code>{hash_id}</code>\n├ ꜱᴛᴀᴛᴜꜱ : ᴘᴇʀᴍᴀɴᴇɴᴛʟʏ ᴡɪᴘᴇᴅ\n╰──────────────────────⍟</b>"
    )