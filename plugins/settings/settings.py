# with Love @LazyDeveloperr 💘
# Subscribe YT @LazyDeveloperr - to learn more about this for free...

import asyncio
from info import LOGGER
from pyrogram import types, errors
from database.users_chats_db import db
from pyrogram import enums

async def OpenSettings(m: "types.Message"):
    usr_id = m.chat.id
    user_data = await db.get_user_data(usr_id)
    if not user_data:
        await m.edit("Failed to fetch your data from database!")
        return
    upload_as_doc = user_data.get("upload_as_doc", False)
    caption = user_data.get("lazy_caption", None)
    apply_caption = user_data.get("apply_caption", True)
    thumbnail = user_data.get("thumbnail", None)
    buttons_markup = [
        [types.InlineKeyboardButton(f"ᴜᴘʟᴏᴀᴅ ᴀs {'🎥 ᴠɪᴅᴇᴏ' if upload_as_doc else '🗃️ ғɪʟᴇ'}",
                                    callback_data="triggerUploadMode")],
        [types.InlineKeyboardButton(f"{'ᴄʜᴀɴɢᴇ' if thumbnail else '🌃 sᴇᴛ'} ᴛʜᴜᴍʙɴᴀɪʟ",
                                    callback_data="setThumbnail")]
    ]
    if thumbnail:
        buttons_markup.append([types.InlineKeyboardButton("🌆 sʜᴏᴡ ᴛʜᴜᴍʙɴᴀɪʟ",
                                                          callback_data="showThumbnail")])
    buttons_markup.append([types.InlineKeyboardButton("👈 HOME",
                                                      callback_data="start"),
                            types.InlineKeyboardButton("🔒 Close",
                                                      callback_data="close_data")])

    try:
        await m.edit(
            text="**ʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ sᴇᴛᴜᴘ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs**",
            reply_markup=types.InlineKeyboardMarkup(buttons_markup),
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.MARKDOWN
        )
    except errors.MessageNotModified: pass
    except errors.FloodWait as e:
        await asyncio.sleep(e.x)
        await show_settings(m)
    except Exception as err:
        LOGGER.getLogger(__name__).error(err)

# with Love @LazyDeveloperr 💘
# Subscribe YT @LazyDeveloperr - to learn more about this for free...
