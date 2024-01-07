    # Credit @LazyDeveloper.
    # Please Don't remove credit.
    # Born to make history @LazyDeveloper !

    # Thank you LazyDeveloper for helping us in this Journey
    # 🥰  Thank you for giving me credit @LazyDeveloperr  🥰

    # for any error please contact me -> telegram@LazyDeveloperr or insta @LazyDeveloperr 

from pyrogram import Client, filters
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import random
import os
from PIL import Image

# the Strings used for this "thing"
from pyrogram import Client
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram import filters
from database.lazy_ffmpeg import take_screen_shot
from info import DOWNLOAD_LOCATION, AUTH_CHANNEL
from database.users_chats_db import db
from plugins.settings.settings import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ForceReply
from lazybot.forcesub import handle_force_subscribe
from database.add import add_user_to_database

@Client.on_message(filters.private & filters.command(['view_thumb','view_thumbnail','vt']))
async def viewthumb(client, message):
    if not message.from_user:
        return await message.reply_text("What the hell is this...")
    await add_user_to_database(client, message)
    if AUTH_CHANNEL:
      fsub = await handle_force_subscribe(client, message)
      if fsub == 400:
        return
    thumb = await db.get_thumbnail(message.from_user.id)
    if thumb:
       await client.send_photo(
	   chat_id=message.chat.id, 
	   photo=thumb,
       caption=f"Current thumbnail for direct renaming",
       reply_markup=InlineKeyboardMarkup([
           [InlineKeyboardButton("🗑️ ᴅᴇʟᴇᴛᴇ ᴛʜᴜᴍʙɴᴀɪʟ" , callback_data="deleteThumbnail")]
       ]))
    else:
        await message.reply_text("😔**Sorry ! No thumbnail found...**😔") 

@Client.on_message(filters.private & filters.command(['del_thumb','delete_thumb','dt']))
async def removethumb(client, message):
    if not message.from_user:
        return await message.reply_text("What the hell is this...")
    await add_user_to_database(client, message)
    if AUTH_CHANNEL:
      fsub = await handle_force_subscribe(client, message)
      if fsub == 400:
        return
    await db.set_thumbnail(message.from_user.id, file_id=None)
    await message.reply_text("**Okay sweetie, I deleted your custom thumbnail for direct renaming. Now I will apply default thumbnail. ✅️**✅️")

@Client.on_message(filters.private & filters.command(['set_thumbnail','set_thumb','st']))
async def addthumbs(client, message):
    replied = message.reply_to_message
    
    if not message.from_user:
        return await message.reply_text("What the hell is this...")
    
    await add_user_to_database(client, message)
    
    if AUTH_CHANNEL:
        fsub = await handle_force_subscribe(client, message)
        if fsub == 400:
            return
        
    LazyDev = await message.reply_text("Please Wait ...")
        # Check if there is a replied message and it is a photo
    if replied and replied.photo:
        # Save the photo file_id as a thumbnail for the user
        await db.set_thumbnail(message.from_user.id, file_id=replied.photo.file_id)
        await LazyDev.edit("**✅ Custom thumbnail set successfully!**")
    else:
        await LazyDev.edit("**❌ Please reply to a photo to set it as a custom thumbnail.**")

@Client.on_message(filters.private & filters.command(['view_lazy_thumb','vlt']))
async def viewthumbnail(client, message):    
    if not message.from_user:
        return await message.reply_text("What the hell is this...")
    await add_user_to_database(client, message) 
    if AUTH_CHANNEL:
      fsub = await handle_force_subscribe(client, message)
      if fsub == 400:
        return   
    thumbnail = await db.get_lazy_thumbnail(message.from_user.id)
    if thumbnail is not None:
        await client.send_photo(
        chat_id=message.chat.id,
        photo=thumbnail,
        caption=f"ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ sᴀᴠᴇᴅ ᴛʜᴜᴍʙɴᴀɪʟ 🦠",
        reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🗑️ ᴅᴇʟᴇᴛᴇ ᴛʜᴜᴍʙɴᴀɪʟ", callback_data="deleteurlthumbnail")]]
                ),
        reply_to_message_id=message.id)
    else:
        await message.reply_text(text=f"ɴᴏ ᴛʜᴜᴍʙɴᴀɪʟ ғᴏᴜɴᴅ 🤒")

@Client.on_message(filters.private & filters.command(['del_lazy_thumb','delete_lazy_thumb','dlt']))
async def removethumbnail(client, message):
    if not message.from_user:
        return await message.reply_text("What the hell is this...")
    await add_user_to_database(client, message)
    if AUTH_CHANNEL:
      fsub = await handle_force_subscribe(client, message)
      if fsub == 400:
        return

    await db.set_lazy_thumbnail(message.from_user.id, thumbnail=None)
    await message.reply_text(
        "**🗑️ Okay baby, I deleted your custom thumbnail for url downloading. Now I will apply default thumbnail. ☑**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⚙ ᴄᴏɴғɪɢᴜʀᴇ sᴇᴛᴛɪɴɢs 🎨", callback_data="openSettings")]
        ])
    )

@Client.on_message(filters.private & filters.command(['set_lazy_thumb','set_lazy_thumbnail', 'slt']))
async def add_thumbnail(client, message):
    replied = message.reply_to_message
    
    if not message.from_user:
        return await message.reply_text("What the hell is this...")
    
    await add_user_to_database(client, message)
    
    if AUTH_CHANNEL:
        fsub = await handle_force_subscribe(client, message)
        if fsub == 400:
            return
    
    editable = await message.reply_text("**👀 Processing...**")
    
    # Check if there is a replied message and it is a photo
    if replied and replied.photo:
        # Save the photo file_id as a thumbnail for the user
        await db.set_lazy_thumbnail(message.from_user.id, thumbnail=replied.photo.file_id)
        await editable.edit("**✅ Custom thumbnail set successfully!**")
    else:
        await editable.edit("**❌ Please reply to a photo to set it as a custom thumbnail.**")


async def Gthumb01(bot, update):
    thumb_image_path = DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    db_thumbnail = await db.get_lazy_thumbnail(update.from_user.id)
    if db_thumbnail is not None:
        thumbnail = await bot.download_media(message=db_thumbnail, file_name=thumb_image_path)
        Image.open(thumbnail).convert("RGB").save(thumbnail)
        img = Image.open(thumbnail)
        img.resize((100, 100))
        img.save(thumbnail, "JPEG")
    else:
        thumbnail = None

    return thumbnail

async def Gthumb02(bot, update, duration, download_directory):
    thumb_image_path = DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    db_thumbnail = await db.get_lazy_thumbnail(update.from_user.id)
    if db_thumbnail is not None:
        thumbnail = await bot.download_media(message=db_thumbnail, file_name=thumb_image_path)
    else:
        thumbnail = await take_screen_shot(download_directory, os.path.dirname(download_directory), random.randint(0, duration - 1))

    return thumbnail

async def Mdata01(download_directory):
          width = 0
          height = 0
          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds
              if metadata.has("width"):
                  width = metadata.get("width")
              if metadata.has("height"):
                  height = metadata.get("height")
          return width, height, duration

async def Mdata02(download_directory):
          width = 0
          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds
              if metadata.has("width"):
                  width = metadata.get("width")

          return width, duration

async def Mdata03(download_directory):

          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds

          return duration
