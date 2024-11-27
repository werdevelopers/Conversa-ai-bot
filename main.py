from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from vars import *
from pyrogram.enums import ChatAction
from database.userschat import db
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid, UserBannedInChannel, UserNotParticipant
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
import random
import string
import asyncio
import aiofiles
import os
import datetime
import time
import requests
from Mangandi import ImageUploader
responses_dict = {}
lock = asyncio.Lock()

aibot = Client(
    "werdeveloper_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)
#======================================================
async def broadcast_messages(user_id, message, pin):
    try:
        m = await message.copy(chat_id=user_id)
        if pin:
            await m.pin(both_sides=True)
        return "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message, pin)
    except Exception as e:
        await db.delete_user(int(user_id))
        return "Error"

def get_readable_time(seconds):
    periods = [('days', 86400), ('hour', 3600), ('min', 60), ('sec', 1)]
    result = ''
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            result += f'{int(period_value)}{period_name}'
    return result

class temp(object):
    ME = None
    CURRENT=int(os.environ.get("SKIP", 2))
    CANCEL = False
    U_NAME = None
    B_NAME = None
    B_LINK = None
    SETTINGS = {}
    FILES_ID = {}
    BANNED_USERS = []
    BANNED_CHATS = []
    USERS_CANCEL = False
    GROUPS_CANCEL = False    
    CHAT = {}
#======================================================

# ==========================================
# 		COMMANDS
# ==========================================

@aibot.on_message(filters.command("start"))
async def start(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await aibot.send_message(
            chat_id=LOG_CHANNEL, 
            text=f"**#NewUser\n\n👤 {message.from_user.mention}** (`{message.from_user.id}`)"
        )
    await message.reply_text(
        START_TEXT.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('✨ Updates Channel', url=f"https://t.me/{UPDATE_CHANNEL}")],
                [InlineKeyboardButton('Help', callback_data='help'), InlineKeyboardButton('About', callback_data='about')],
                [InlineKeyboardButton('Source Code', url='https://youtu.be/NOO7XVqIHmk')]
            ]
        ),
        disable_web_page_preview=True
    )

@aibot.on_message(filters.command("users") & filters.user(BOT_OWNER))
async def users(client, message):
    total_users = await db.total_users_count()
    text = f"**Total Users: {total_users}**"
    await message.reply_text(
        text=text,
        quote=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Close', callback_data='close')]]),
        disable_web_page_preview=True
    )


@aibot.on_message(filters.command(["broadcast", "pin_broadcast"]) & filters.user(BOT_OWNER) & filters.reply)
async def users_broadcast(bot, message):
    if lock.locked():
        return await message.reply('Currently broadcast processing, Wait for complete.')
    if message.command[0] == 'pin_broadcast':
        pin = True
    else:
        pin = False
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    b_sts = await message.reply_text(text='Broadcasting your users messages...')
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0

    async with lock:
        async for user in users:
            time_taken = get_readable_time(time.time()-start_time)
            if temp.USERS_CANCEL:
                temp.USERS_CANCEL = False
                await b_sts.edit(f"Users broadcast Cancelled!\nCompleted in {time_taken}\n\nTotal Users: <code>{total_users}</code>\nCompleted: <code>{done} / {total_users}</code>\nSuccess: <code>{success}</code>")
                return
            sts = await broadcast_messages(int(user['id']), b_msg, pin)
            if sts == 'Success':
                success += 1
            elif sts == 'Error':
                failed += 1
            done += 1
            if not done % 20:
                btn = [[
                    InlineKeyboardButton('CANCEL', callback_data=f'broadcast_cancel#users')
                ]]
                await b_sts.edit(f"Users broadcast in progress...\n\nTotal Users: <code>{total_users}</code>\nCompleted: <code>{done} / {total_users}</code>\nSuccess: <code>{success}</code>", reply_markup=InlineKeyboardMarkup(btn))
        await b_sts.edit(f"Users broadcast completed.\nCompleted in {time_taken}\n\nTotal Users: <code>{total_users}</code>\nCompleted: <code>{done} / {total_users}</code>\nSuccess: <code>{success}</code>")


# ==========================================
# 	CALLBACKS
# ==========================================

@aibot.on_callback_query(filters.regex('home'))
async def home_callback(client, callback_query):
    await callback_query.message.edit_text(
        text=START_TEXT.format(callback_query.from_user.mention),
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('✨ Updates Channel', url=f"https://t.me/{UPDATE_CHANNEL}")],
                [InlineKeyboardButton('About', callback_data='about'), InlineKeyboardButton('Help', callback_data='help')],
                [InlineKeyboardButton('Source Code', url='https://youtu.be/NOO7XVqIHmk')]
            ]
        ),
        disable_web_page_preview=True
    )

@aibot.on_callback_query(filters.regex('about'))
async def about_callback(client, callback_query):
    await callback_query.message.edit_text(
        text=ABOUT_TEXT.format(callback_query.from_user.mention, callback_query.from_user.id),
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('Home', callback_data="home"), InlineKeyboardButton('Help', callback_data='help')],
                [InlineKeyboardButton('Close', callback_data='close')]
            ]
        ),
        disable_web_page_preview=True
    )

@aibot.on_callback_query(filters.regex('help'))
async def help_callback(client, callback_query):
    await callback_query.message.edit_text(
        text=HELP_TEXT,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('Home', callback_data="home"), InlineKeyboardButton('About', callback_data='about')],
                [InlineKeyboardButton('Close', callback_data='close')]
            ]
        ),
        disable_web_page_preview=True
    )

@aibot.on_callback_query(filters.regex('tutorial'))
async def tutorial_callback(client, callback_query):
    sent_message = await aibot.send_video(
        chat_id=callback_query.message.chat.id,
        video=TUTORIAL_VIDEO_LINK,
        caption="**Here is the tutorial video for you!\n\n⚠️ This video will be deleted in 2 minutes.**",
    )
    await asyncio.sleep(120) # 2min set
    await sent_message.delete()

@aibot.on_callback_query(filters.regex('close'))
async def close_callback(client, callback_query):
    await callback_query.message.delete()



# ==========================================
# 		AI CHATS
# ==========================================


@aibot.on_message(filters.private & filters.text)
async def private_ai_reply(client, message):
    input_text = message.text
    if UPDATE_CHANNEL:
        try:
            user = await client.get_chat_member(UPDATE_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await message.reply_text(text="**You are banned 🚫**")
                return
        except UserNotParticipant:
            await message.reply_text(
                text=f"**{message.from_user.mention} 👋\n\nJoin My Updated Channel to use me. (without join you can't use me)**",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="Join Now", url=f"https://telegram.me/{UPDATE_CHANNEL}")]]
                )
            )
            return
        except Exception as error:
            print(error)
            await message.reply_text(
                text=f"<b>Something went wrong contact my <a href='https://telegram.me/{SUPPORT_USERNAME}'>Developer</a> ‼️</b>",
                disable_web_page_preview=True
            )
            return

    if message.from_user.id == BOT_OWNER:
        return

    if input_text.startswith("/"):
        return

    searching_message = await message.reply_text("🔍")
    query = f"{PROMPT}, so my question is ({input_text})"
    url = f"https://darkness.ashlynn.workers.dev/chat/?prompt={query}"
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("successful") == "success" and data.get("status") == 200:
            response_text = data.get("response")
            responses_dict[message.from_user.id] = response_text
            await aibot.send_message(
                chat_id=AI_LOGS,
                text=f"👤 {message.from_user.mention} (`{message.from_user.id}`)\n\n**Query:** `{input_text}`\n\n**AI Generated Response:**\n`{response_text}`",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Close', callback_data='close')]])
            )
            await searching_message.edit_text(
                f"**{message.from_user.mention},** {response_text}",
            )
        else:
            await searching_message.edit_text("**⚠️ Sorry, could not fetch a valid response. Please try again later.**")
    except Exception as e:
        await searching_message.edit_text("**⚠️ Sorry, an error occurred while fetching the response. Please try again later.**")
        print(f"Error: {e}")

# ==========================================
# 	    IMAGE SCAN CODE
# ==========================================

@aibot.on_message(filters.media)
async def handle_media(client, message):
    if UPDATE_CHANNEL:
        try:
            user = await client.get_chat_member(UPDATE_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await message.reply_text(text="**You are banned 🚫**")
                return
        except UserNotParticipant:
            await message.reply_text(
                text=f"**{message.from_user.mention} 👋\n\nJoin My Updated Channel to use me. (without join you can't use me)**",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(
                        text="Join Now", url=f"https://telegram.me/{UPDATE_CHANNEL}")]]
                )
            )
            return
        except Exception as error:
            print(error)
            await message.reply_text(
                text=f"<b>Something went wrong contact my <a href='https://telegram.me/{SUPPORT_USERNAME}'>Developer</a> ‼️</b>",
                disable_web_page_preview=True
            )
            return

    file_size_limit = 10 * 1024 * 1024  # 10 MB in bytes
    if (message.document and message.document.file_size > file_size_limit) or \
       (message.photo and message.photo.file_size > file_size_limit):
        await message.reply_text("<b>Send a media under 10MB ‼️</b>")
        return

    try:
        if message.photo:
            if message.caption:
                query = message.caption
            else:
                tutorial_button = InlineKeyboardButton(
                    "Tutorial 📌", callback_data="tutorial")
                reply_markup = InlineKeyboardMarkup([[tutorial_button]])
                await message.reply_text(
                    "**❗ Please send the photo with a caption. In the caption, describe the problem or query you want to check.**",
                    reply_markup=reply_markup
                )
                return

            downloading_message = await message.reply_text(f"**🔍 {message.from_user.mention}, Downloading your media....**")
            media_path = await message.download()
            await downloading_message.edit_text("**Uploading your media for processing....**")
            upload_url = "https://envs.sh"
            try:
                with open(media_path, 'rb') as file:
                    files = {'file': file}
                    response = requests.post(upload_url, files=files)

                    if response.status_code == 200:
                        image_url = response.text.strip()
                    else:
                        raise Exception(f"Upload failed with status code {response.status_code}")
            except Exception as upload_error:
                await downloading_message.edit_text(f"**Upload failed: {upload_error}**")
                return
            finally:
                try:
                    os.remove(media_path)
                except Exception as error:
                    print(f"Error removing file: {error}")

            await downloading_message.edit_text(f"**🔍 {message.from_user.mention}, Please wait....**")
            prompt = query.replace(" ", "+")
            api = "https://nexlynx.ashlynn.workers.dev/api/titan"
            response = requests.get(
                f"{api}?question={prompt}&image={image_url}")

            if response.status_code == 200:
                result = response.json()
                await downloading_message.edit_text(f"👤 {message.from_user.mention}, here's what I found:\n\n{result['message']}")
            else:
                await downloading_message.edit_text("⚠️ There was an error processing your request. Please try again later.")
        elif message.video or message.animation:
            await message.reply_text("❗ Please send me only a photo, not a video or GIF.")
    except Exception as e:
        await message.reply_text("❌ **An error occurred while processing your request.**")
        print(f"Error: {e}")


# ======================
# Upload to envs code
# ======================

def upload_image_requests(media_path):
    upload_url = "https://envs.sh"

    try:
        with open(media_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(upload_url, files=files)

            if response.status_code == 200:
                return response.text.strip()
            else:
                raise Exception(f"Upload failed with status code {response.status_code}")

    except Exception as e:
        print(f"Error during upload: {e}")
        return None


# ==========================================
#            RUN THE CODE
# ==========================================

aibot.run()

	
