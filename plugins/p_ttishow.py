from pyrogram import Client, filters, enums, StopPropagation
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ChatPermissions, ChatMemberUpdated
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from info import *
from database.users_chats_db import db, db2
from database.ia_filterdb import Media, Media2, db as db_stats, db2 as db2_stats
from utils import get_size, save_group_settings, temp, get_settings, get_readable_time, delete_after_delay, is_check_admin
from Script import script
from pyrogram.errors import ChatAdminRequired, MessageNotModified
import asyncio
import psutil
import time
from time import time
from datetime import datetime, timedelta
from bot import botStartTime
from logging_helper import LOGGER


"""-----------------------------------------https://t.me/SilentXBotz--------------------------------------"""

@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    r_j_check = [u.id for u in message.new_chat_members]
    if temp.ME in r_j_check:
        if not await db.get_chat(message.chat.id):
            total=await bot.get_chat_members_count(message.chat.id)
            r_j = message.from_user.mention if message.from_user else "Anonymous" 
            await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, r_j))       
            await db.add_chat(message.chat.id, message.chat.title)
        if message.chat.id in temp.BANNED_CHATS:
            
            buttons = [[
                InlineKeyboardButton('📌 ᴄᴏɴᴛᴀᴄᴛ ꜱᴜᴘᴘᴏʀᴛ 📌', url=OWNER_LNK)
            ]]
            reply_markup=InlineKeyboardMarkup(buttons)
            k = await message.reply(
                text='<b>ᴄʜᴀᴛ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ 🐞\n\nᴍʏ ᴀᴅᴍɪɴꜱ ʜᴀꜱ ʀᴇꜱᴛʀɪᴄᴛᴇᴅ ᴍᴇ ꜰʀᴏᴍ ᴡᴏʀᴋɪɴɢ ʜᴇʀᴇ ! ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ɪᴛ ᴄᴏɴᴛᴀᴄᴛ ꜱᴜᴘᴘᴏʀᴛ.</b>',
                reply_markup=reply_markup,
            )

            try:
                await k.pin()
            except:
                pass
            await bot.leave_chat(message.chat.id)
            return
        buttons = [[
                    InlineKeyboardButton("📌 ᴄᴏɴᴛᴀᴄᴛ ꜱᴜᴘᴘᴏʀᴛ 📌", url=OWNER_LNK)
                  ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=f"<b>Thankyou For Adding Me In {message.chat.title} ❣️\n\nIf you have any questions & doubts about using me contact support.</b>",
            reply_markup=reply_markup)
        try:
            await db.connect_group(message.chat.id, message.from_user.id)
        except Exception as e:
            LOGGER.error(f"DB error connecting group: {e}")
    else:
        settings = await get_settings(message.chat.id)
        if settings["welcome"]:
            for u in message.new_chat_members:
                if (temp.MELCOW).get('welcome') is not None:
                    try:
                        await (temp.MELCOW['welcome']).delete()
                    except:
                        pass
                temp.MELCOW['welcome'] = await message.reply_video(
                                                 video=(MELCOW_VID),
                                                 caption=(script.MELCOW_ENG.format(u.mention, message.chat.title)),
                                                 reply_markup=InlineKeyboardMarkup(
                                                                         [[
                                                                           InlineKeyboardButton("📌 ᴄᴏɴᴛᴀᴄᴛ ꜱᴜᴘᴘᴏʀᴛ 📌", url=OWNER_LNK)
                                                                         ]]
                                                 ),
                                                 parse_mode=enums.ParseMode.HTML
                )
                
        if settings["auto_delete"]:
            await asyncio.sleep(600)
            if 'welcome' in temp.MELCOW:
                try:
                    await temp.MELCOW['welcome'].delete()
                except Exception:
                    pass
                
# 1. THE SILENT TRACKER: Only tracks when existing members invite new people
@Client.on_chat_member_updated(group=5)
async def booster_score_tracker(bot,update: ChatMemberUpdated):
    if not update.new_chat_member:
        return
    if update.old_chat_member:
        if update.old_chat_member.status not in [enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.BANNED]:
            return
        
    if update.new_chat_member.status not in [enums.ChatMemberStatus.MEMBER, enums.ChatMemberStatus.RESTRICTED]:
        return
    if update.new_chat_member.user.is_bot:
        return    

    chat_id = update.chat.id
    settings = await get_settings(chat_id)
    
    if not settings.get("member_booster", False):
        return

    inviter_id = None
    if update.invite_link and update.invite_link.creator:
        inviter_id = update.invite_link.creator.id
    elif update.from_user and update.from_user.id != update.new_chat_member.user.id:
        inviter_id = update.from_user.id
    if not inviter_id:
        return
    if inviter_id in ADMINS:
        return        
    bypassed_users = settings.get("booster_bypass", [])
    if inviter_id in bypassed_users:
        return
    
    #current_count = await db.get_booster_count(chat_id, inviter_id)
    #await db.inc_booster_count(chat_id, inviter_id, 1)
    #new_score = await db.get_booster_count(chat_id, inviter_id)
    
    required_count = settings.get("booster_count", 1)

    # 1. Atomically add the point AND get the new score in a single line!
    new_score = await db.inc_booster_count(chat_id, inviter_id, 1)

    if new_score == required_count:
        try:
            # Unrestrict the inviter
            unrestrict_perms = ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=False,
                can_add_web_page_previews=False,
                can_send_polls=False,
                can_invite_users=True 
            )
            await bot.restrict_chat_member(chat_id, inviter_id, unrestrict_perms)
            
            # Fetch the inviter's profile to mention them
            inviter = await bot.get_users(inviter_id)
            success = await bot.send_message(
                chat_id, 
                f"🎉 **Congratulations {inviter.mention}!** You have added {required_count} members and permanently unlocked messaging!"
            )
            asyncio.create_task(delete_after_delay(success, 30))
        except Exception as e:
            LOGGER.error(f"Advanced Tracker Error: {e}")


# 2. THE MESSAGE INTERCEPTOR: Scans all text/media and nukes it if target isn't met
@Client.on_message(filters.group & ~filters.new_chat_members & ~filters.left_chat_member & ~filters.service, group=-100)
async def booster_message_interceptor(bot, message):
    LOGGER.info("=========================================")
    LOGGER.info(f"1. MESSAGE INTERCEPTED: '{message.text}' from User ID: {message.from_user.id}")
    
    try:
        if not message.from_user:
            LOGGER.info("-> EXITING: No user attached to message.")
            return

        chat_id = message.chat.id
        user_id = message.from_user.id
        
        settings = await get_settings(chat_id)

        # --- LAZY AUTO-RESET ENGINE ---
        import time as time_module
        auto_reset = settings.get("booster_auto_reset", "OFF")
        if auto_reset != "OFF":
            last_reset = settings.get("booster_last_reset", 0)
            now_ts = time_module.time() # Fixed: Using datetime to avoid module conflicts
            
            # Calculate time limit
            if auto_reset == "2 MINS":
                time_limit = 120
            elif auto_reset == "WEEKLY":
                time_limit = 604800
            else: # MONTHLY
                time_limit = 2592000
            
            # If the time limit has passed since the last reset, wipe everything silently
            if (now_ts - last_reset) > time_limit:
                await db.reset_all_booster_scores(chat_id)
                await save_group_settings(chat_id, "booster_last_reset", now_ts)
                LOGGER.info(f"Auto-Reset Engine triggered for group {chat_id} ({auto_reset})")
    # ------------------------------

        is_booster_on = settings.get("member_booster", False)
        LOGGER.info(f"2. BOOSTER STATUS FOR THIS GROUP ({chat_id}): {is_booster_on}")
        
        if not is_booster_on:
            LOGGER.info("-> EXITING: Booster is turned OFF in settings. Letting message pass to spellchecker.")
            return

        bypassed = settings.get("booster_bypass", [])
        required_count = settings.get("booster_count", 1)

        if user_id in ADMINS:
            LOGGER.info("-> EXITING: User is a global ADMIN. Letting message pass.")
            return
            
        if user_id in bypassed:
            LOGGER.info("-> EXITING: User is in the Bypass list. Letting message pass.")
            return

        is_admin = await is_check_admin(bot, chat_id, user_id)
        if is_admin:
            LOGGER.info("-> EXITING: User is an admin of this specific group. Letting message pass.")
            return

        current_count = await db.get_booster_count(chat_id, user_id)
        LOGGER.info(f"3. USER SCORE CHECK: User has added {current_count} members. Target is {required_count}.")
        
        if current_count >= required_count:
            LOGGER.info("-> EXITING: User has hit the target! Letting message pass to spellchecker.")
            return 

        LOGGER.info("4. ACTION TRIGGERED: User failed check. Muting and nuking message.")
        
        try:
            await message.delete()
        except Exception as e:
            LOGGER.error(f"Error deleting message: {e}")

        try:
            until_date = datetime.now() + timedelta(minutes=1)
            restrict_perms = ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_add_web_page_previews=False,
                can_send_polls=False,
                can_invite_users=True 
            )
            await bot.restrict_chat_member(chat_id, user_id, restrict_perms, until_date=until_date)
            
            btn = [[InlineKeyboardButton("How many users have I added?", callback_data=f"check_adds_{user_id}")]]
            warning = await message.reply(
                f'👉 Dear "{message.from_user.mention}" user, you need to add {required_count} of your contacts to the group then you can send message!',
                reply_markup=InlineKeyboardMarkup(btn)
            )
            asyncio.create_task(delete_after_delay(warning, 60))
            LOGGER.info("5. WARNING SENT AND USER MUTED SUCCESSFULLY.")
        except Exception as e:
            LOGGER.error(f"Failed to mute/warn user: {e}")
        
        LOGGER.info("6. THROWING KILL SWITCH: Stopping spellchecker from seeing this message.")
        raise StopPropagation
        
    except StopPropagation:
        LOGGER.info("-> KILL SWITCH ACTIVATED SUCCESSFULLY.")
        raise
    except Exception as e:
        LOGGER.error(f"CRITICAL ERROR IN INTERCEPTOR: {e}")
    finally:
        LOGGER.info("=========================================")


@Client.on_message(filters.group & (filters.new_chat_members | filters.left_chat_member), group=-98)
async def builtin_join_hider(bot, message):
    chat_id = message.chat.id
    settings = await get_settings(chat_id)
    
    # Check if the admin turned the feature ON
    if settings.get("join_hider", False):
        try:
            await message.delete()
        except Exception:
            pass
        
@Client.on_message(filters.command('leave') & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        chat = chat
    try:
        buttons = [[
                  InlineKeyboardButton("📌 ᴄᴏɴᴛᴀᴄᴛ ꜱᴜᴘᴘᴏʀᴛ 📌", url=OWNER_LNK)
                  ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat,
            text='<b>ʜᴇʟʟᴏ ꜰʀɪᴇɴᴅꜱ, \nᴍʏ ᴀᴅᴍɪɴ ʜᴀꜱ ᴛᴏʟᴅ ᴍᴇ ᴛᴏ ʟᴇᴀᴠᴇ ꜰʀᴏᴍ ɢʀᴏᴜᴘ, ꜱᴏ ɪ ʜᴀᴠᴇ ᴛᴏ ɢᴏ !/nɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴀᴅᴅ ᴍᴇ ᴀɢᴀɪɴ ᴄᴏɴᴛᴀᴄᴛ ꜱᴜᴘᴘᴏʀᴛ.</b>',
            reply_markup=reply_markup,
        )

        await bot.leave_chat(chat)
        await message.reply(f"left the chat `{chat}`")
    except Exception as e:
        await message.reply(f'Error - {e}')

@Client.on_message(filters.command('disable') & filters.user(ADMINS))
async def disable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat_ = int(chat)
    except:
        return await message.reply('Give Me A Valid Chat ID')
    cha_t = await db.get_chat(int(chat_))
    if not cha_t:
        return await message.reply("Chat Not Found In DB")
    if cha_t['is_disabled']:
        return await message.reply(f"This chat is already disabled:\nReason-<code> {cha_t['reason']} </code>")
    await db.disable_chat(int(chat_), reason)
    temp.BANNED_CHATS.append(int(chat_))
    await message.reply('Chat Successfully Disabled')
    try:
        buttons = [[
            InlineKeyboardButton('📌 ᴄᴏɴᴛᴀᴄᴛ ꜱᴜᴘᴘᴏʀᴛ 📌', url=OWNER_LNK)
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat_, 
            text=f'<b>ʜᴇʟʟᴏ ꜰʀɪᴇɴᴅꜱ, \nᴍʏ ᴀᴅᴍɪɴ ʜᴀꜱ ᴛᴏʟᴅ ᴍᴇ ᴛᴏ ʟᴇᴀᴠᴇ ꜰʀᴏᴍ ɢʀᴏᴜᴘ, ꜱᴏ ɪ ʜᴀᴠᴇ ᴛᴏ ɢᴏ ! \nɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴀᴅᴅ ᴍᴇ ᴀɢᴀɪɴ ᴄᴏɴᴛᴀᴄᴛ ꜱᴜᴘᴘᴏʀᴛ..</b> \nReason : <code>{reason}</code>',
            reply_markup=reply_markup)
        await bot.leave_chat(chat_)
    except Exception as e:
        await message.reply(f"Error - {e}")


@Client.on_message(filters.command('enable') & filters.user(ADMINS))
async def re_enable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat_ = int(chat)
    except:
        return await message.reply('Give Me A Valid Chat ID')
    sts = await db.get_chat(int(chat))
    if not sts:
        return await message.reply("Chat Not Found In DB !")
    if not sts.get('is_disabled'):
        return await message.reply('This chat is not yet disabled.')
    await db.re_enable_chat(int(chat_))
    temp.BANNED_CHATS.remove(int(chat_))
    await message.reply("Chat Successfully re-enabled")

@Client.on_message(filters.command('stats') & filters.user(ADMINS))
async def get_stats(bot, message):
    try:
        SilentXBotz = await message.reply('ᴀᴄᴄᴇꜱꜱɪɴɢ ꜱᴛᴀᴛᴜꜱ ᴅᴇᴛᴀɪʟꜱ...')
        total_users = await db.total_users_count()
        totl_chats = await db.total_chat_count()
        premium = await db.all_premium_users()
        file1 = await Media.count_documents()
        DB_SIZE = 512 * 1024 * 1024
        dbstats = await db_stats.command("dbStats")
        db_size = dbstats['dataSize']
        free = DB_SIZE - db_size
        uptime = get_readable_time(time() - botStartTime)
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent()
        if MULTIPLE_DB == False:
            await SilentXBotz.edit(script.STATUS_TXT.format(
                total_users, totl_chats, premium, file1, get_size(db_size), get_size(free), uptime, ram, cpu))                                               
            return
        file2 = await Media2.count_documents()
        db2stats = await db2_stats.command("dbStats")
        db2_size = db2stats['dataSize']
        free2 = DB_SIZE - db2_size
        await SilentXBotz.edit(script.MULTI_STATUS_TXT.format(
            total_users, totl_chats, premium, file1, get_size(db_size), get_size(free),
            file2, get_size(db2_size), get_size(free2), uptime, ram, cpu, (int(file1) + int(file2))
        ))
    except Exception as e:
        LOGGER.error(e)
        

@Client.on_message(filters.command('invite') & filters.user(ADMINS))
async def gen_invite(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        return await message.reply('Give Me A Valid Chat ID')
    try:
        link = await bot.create_chat_invite_link(chat)
    except ChatAdminRequired:
        return await message.reply("Invite Link Generation Failed, Iam Not Having Sufficient Rights")
    except Exception as e:
        return await message.reply(f'Error {e}')
    await message.reply(f'Here is your Invite Link {link.invite_link}')

@Client.on_message(filters.command('ban') & filters.user(ADMINS))
async def ban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a user id / username')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("This is an invalid user, make sure I have met him before.")
    except IndexError:
        return await message.reply("This might be a channel, make sure its a user.")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if jar['is_banned']:
            return await message.reply(f"{k.mention} is already banned\nReason: {jar['ban_reason']}")
        await db.ban_user(k.id, reason)
        temp.BANNED_USERS.append(k.id)
        await message.reply(f"Successfully banned {k.mention}")
    
@Client.on_message(filters.command('unban') & filters.user(ADMINS))
async def unban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a user id / username')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("This is an invalid user, make sure ia have met him before.")
    except IndexError:
        return await message.reply("Thismight be a channel, make sure its a user.")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if not jar['is_banned']:
            return await message.reply(f"{k.mention} is not yet banned.")
        await db.remove_ban(k.id)
        temp.BANNED_USERS.remove(k.id)
        await message.reply(f"Successfully unbanned {k.mention}")
 
@Client.on_message(filters.command('users') & filters.user(ADMINS))
async def list_users(bot, message):
    raju = await message.reply('Getting List Of Users')
    users = await db.get_all_users()
    out = "Users Saved In DB Are:\n\n"
    async for user in users:
        out += f"<a href=tg://user?id={user['id']}>{user['name']}</a>"
        if user['ban_status']['is_banned']:
            out += '( Banned User )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('users.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('users.txt', caption="List Of Users")

@Client.on_message(filters.command('chats') & filters.user(ADMINS))
async def list_chats(bot, message):
    raju = await message.reply('Getting List Of chats')
    chats = await db.get_all_chats()
    out = "Chats Saved In DB Are:\n\n"
    async for chat in chats:
        out += f"**Title:** `{chat['title']}`\n**- ID:** `{chat['id']}`"
        if chat['chat_status']['is_disabled']:
            out += '( Disabled Chat )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('chats.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('chats.txt', caption="List Of Chats")
