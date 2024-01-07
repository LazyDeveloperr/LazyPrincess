# with Love @LazyDeveloperr 💘
# Subscribe YT @LazyDeveloperr - to learn more about this for free...

import math
import json
import asyncio
import shutil
import os
import requests
from database.users_chats_db import db
from pyrogram.types import Thumbnail
from database.add import add_user_to_database
from lazybot.ran_text import random_char
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import enums
from database.lazy_utils import  humanbytes
from pyrogram import Client
from pyrogram import filters
from Script import script
import time
from urllib.parse import urlparse
from info import LOG_CHANNEL, DOWNLOAD_LOCATION, HTTP_PROXY, AUTH_CHANNEL, BANNED_USERS, CHUNK_SIZE,ADMINS,PRIME_DOWNLOADERS
from PIL import Image
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Client.on_message(filters.private & filters.user(ADMINS) & filters.regex(pattern=".*http.*"))
async def echo(client, message):
    if LOG_CHANNEL:
        try:
            log_message = await message.forward(LOG_CHANNEL)
            log_info = "Message Sender Information\n"
            log_info += "\nFirst Name: " + message.from_user.first_name
            log_info += "\nUser ID: " + str(message.from_user.id)
            log_info += "\nUsername: @" + message.from_user.username if message.from_user.username else ""
            log_info += "\nUser Link: " + message.from_user.mention
            await log_message.reply_text(
                text=log_info,
                disable_web_page_preview=True,
                quote=True
            )
        except Exception as error:
            print(error)
    if not message.from_user:
        return await message.reply_text("What the hell is this 🤐")

    logger.info(message.from_user)
    url = message.text
    youtube_dl_username = None
    youtube_dl_password = None
    file_name = None

    print(f"{url}")
    if "|" in url:
        url_parts = url.split("|")
        if len(url_parts) == 2:
            url = url_parts[0]
            file_name = url_parts[1]
        elif len(url_parts) == 4:
            url = url_parts[0]
            file_name = url_parts[1]
            youtube_dl_username = url_parts[2]
            youtube_dl_password = url_parts[3]
        else:
            for entity in message.entities:
                if entity.type == "text_link":
                    url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    l = entity.length
                    url = url[o:o + l]
        if url is not None:
            url = url.strip()
        if file_name is not None:
            file_name = file_name.strip()
        # https://stackoverflow.com/a/761825/4723940
        if youtube_dl_username is not None:
            youtube_dl_username = youtube_dl_username.strip()
        if youtube_dl_password is not None:
            youtube_dl_password = youtube_dl_password.strip()
        logger.info(url)
        logger.info(file_name)
    else:
        for entity in message.entities:
            if entity.type == "text_link":
                url = entity.url
            elif entity.type == "url":
                o = entity.offset
                l = entity.length
                url = url[o:o + l]
    
    ######################## 
    if "youtu" in url or "youtube" in url:
        logger.info('cant define file size for youtube videos')
    else:
        xLAZY_BAAPUx_d_size = requests.head(url)    
        xLAZY_BAAPUx_t_length = int(xLAZY_BAAPUx_d_size.headers.get("Content-Length", 0))
        xLAZY_BAAPUx_path = urlparse(url).path
        xLAZY_BAAPUx_u_name = os.path.basename(xLAZY_BAAPUx_path)
        total_length = humanbytes(xLAZY_BAAPUx_t_length)
    logger.info(total_length)
    size = "undefined" if "youtu" in url or "youtube" in url else total_length
    namee = "undefined" if "youtu" in url or "youtube" in url else xLAZY_BAAPUx_u_name

    usr_id = message.chat.id
    user_data = await db.get_user_data(usr_id)
    if not user_data:
        await message.edit("Failed to fetch your data from database!")
        return
    upload_as_doc = user_data.get("upload_as_doc", False)
    upload_type = f" {'🎥 ᴠɪᴅᴇᴏ' if upload_as_doc else '🗃️ ғɪʟᴇ'}"
    ######################## 
    
    if HTTP_PROXY != "":
        command_to_exec = [
            "yt-dlp",
            "--no-warnings",
            "--youtube-skip-dash-manifest",
            "-j",
            url,
            "--proxy", HTTP_PROXY
        ]
    else:
        command_to_exec = [
            "yt-dlp",
            "--no-warnings",
            "--youtube-skip-dash-manifest",
            "-j",
            url
        ]
    try:
        if youtube_dl_username is not None:
            command_to_exec.append("--username")
            command_to_exec.append(youtube_dl_username)
        if youtube_dl_password is not None:
            command_to_exec.append("--password")
            command_to_exec.append(youtube_dl_password)
        logger.info(command_to_exec)
        chk = await client.send_message(
                chat_id=message.chat.id,
                text=f'<b>Analysing url.... </b>',
                disable_web_page_preview=True,
                reply_to_message_id=message.id
            )
        process = await asyncio.create_subprocess_exec(
            *command_to_exec,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        logger.info(e_response)
        t_response = stdout.decode().strip()
        if e_response and "nonnumeric port" not in e_response:
            # logger.warn("Status : FAIL", exc.returncode, exc.output)
            error_message = e_response.replace("please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output.", "")
            if "This video is only available for registered users." in error_message:
                error_message += script.SET_CUSTOM_USERNAME_PASSWORD
            await chk.delete()
            time.sleep(3)
            await client.send_message(
                chat_id=message.chat.id,
                text=script.NO_VOID_FORMAT_FOUND.format(str(error_message)),
                reply_to_message_id=message.id,
                parse_mode=enums.ParseMode.HTML,
                disable_web_page_preview=True
            )
            return False
        
        if t_response:
            # logger.info(t_response)
            x_reponse = t_response
            if "\n" in x_reponse:
                x_reponse, _ = x_reponse.split("\n")
            response_json = json.loads(x_reponse)
            randem = random_char(5)
            save_ytdl_json_path = DOWNLOAD_LOCATION + \
                "/" + str(message.from_user.id) + f'{randem}' + ".json"
            with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
                json.dump(response_json, outfile, ensure_ascii=False)
            inline_keyboard = []
            duration = None
            if "duration" in response_json:
                duration = response_json["duration"]
            if "formats" in response_json:
                for formats in response_json["formats"]:
                    format_id = formats.get("format_id")
                    format_string = formats.get("format_note")
                    if format_string is None:
                        format_string = formats.get("format")
                    format_ext = formats.get("ext")
                    approx_file_size = ""
                    if "filesize" in formats:
                        approx_file_size = humanbytes(formats["filesize"])
                    cb_string_video = "{}|{}|{}|{}".format(
                        "video", format_id, format_ext, randem)
                    cb_string_file = "{}|{}|{}|{}".format(
                        "file", format_id, format_ext, randem)
                    if format_string is not None and not "audio only" in format_string:
                        ikeyboard = [
                            InlineKeyboardButton(
                                "🎬 " + format_string + " " + format_ext + " " + approx_file_size + " ",
                                callback_data=(cb_string_video).encode("UTF-8")
                            )
                        ]
                        """if duration is not None:
                            cb_string_video_message = "{}|{}|{}|{}|{}".format(
                                "vm", format_id, format_ext, ran, randem)
                            ikeyboard.append(
                                InlineKeyboardButton(
                                    "VM",
                                    callback_data=(
                                        cb_string_video_message).encode("UTF-8")
                                )
                            )"""
                    else:
                        # special weird case :\
                        ikeyboard = [
                            InlineKeyboardButton(
                                "🎬 [" +
                                "] ( " +
                                approx_file_size + " )",
                                callback_data=(cb_string_video).encode("UTF-8")
                            )
                        ]
                    inline_keyboard.append(ikeyboard)
                if duration is not None:
                    cb_string_64 = "{}|{}|{}|{}".format("audio", "64k", "mp3", randem)
                    cb_string_128 = "{}|{}|{}|{}".format("audio", "128k", "mp3", randem)
                    cb_string = "{}|{}|{}|{}".format("audio", "320k", "mp3", randem)
                    inline_keyboard.append([
                        InlineKeyboardButton(
                            "🎵 ᴍᴘ𝟹 " + "(" + "64 ᴋʙᴘs" + ")", callback_data=cb_string_64.encode("UTF-8")),
                        InlineKeyboardButton(
                            "🎵 ᴍᴘ𝟹 " + "(" + "128 ᴋʙᴘs" + ")", callback_data=cb_string_128.encode("UTF-8"))
                    ])
                    inline_keyboard.append([
                        InlineKeyboardButton(
                            "🎵 ᴍᴘ𝟹 " + "(" + "320 ᴋʙᴘs" + ")", callback_data=cb_string.encode("UTF-8"))
                    ])
                    inline_keyboard.append([                 
                        InlineKeyboardButton(
                            "🔒 Close", callback_data='close')               
                    ])
            else:
                format_id = response_json["format_id"]
                format_ext = response_json["ext"]
                cb_string_file = "{}|{}|{}|{}".format(
                    "file", format_id, format_ext, randem)
                cb_string_video = "{}|{}|{}|{}".format(
                    "video", format_id, format_ext, randem)
                inline_keyboard.append([
                    InlineKeyboardButton(
                        "🎬 sᴍᴇᴅɪᴀ",
                        callback_data=(cb_string_video).encode("UTF-8")
                    )
                ])

                cb_string_file = "{}={}={}".format(
                    "file", format_id, format_ext)
                cb_string_video = "{}={}={}".format(
                    "video", format_id, format_ext)
                inline_keyboard.append([
                    InlineKeyboardButton(
                        "🎥 ᴠɪᴅᴇᴏ",
                        callback_data=(cb_string_video).encode("UTF-8")
                    )
                ])

            reply_markup = InlineKeyboardMarkup(inline_keyboard)
            await chk.delete()
            await client.send_message(
                chat_id=message.chat.id,
                text= f"⏯<b>File Name:</b> {namee}\n\n🧬<b>File Size:</b> {size} \n<b>⩙ Upload Type:</b> {upload_type}" + script.FORMAT_SELECTION.format(Thumbnail) + "\n" + script.SET_CUSTOM_USERNAME_PASSWORD,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=message.id
            )
        else:
            # fallback for nonnumeric port a.k.a seedbox.io
            inline_keyboard = []
            cb_string_file = "{}={}={}".format(
                "file", "LFO", "NONE")
            cb_string_video = "{}={}={}".format(
                "video", "OFL", "ENON")
            inline_keyboard.append([
                InlineKeyboardButton(
                    "🎬 ᴍᴇᴅɪᴀ",
                    callback_data=(cb_string_video).encode("UTF-8")
                )
            ])

            
            reply_markup = InlineKeyboardMarkup(inline_keyboard)
            await chk.delete(True)
            await client.send_message(
                chat_id=message.chat.id,
                text=f"⏯<b>File 🎥:</b> {namee}\n\n🧬<b>File Size:</b> {size}",
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=message.id
            )
    except Exception as e:
        logger.error(f"An error occurred: {e}")
