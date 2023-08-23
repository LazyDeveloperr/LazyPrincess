import logging
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from info import ADMINS, LAZY_RENAMERS
from info import INDEX_REQ_CHANNEL as LOG_CHANNEL
from info import LAZY_MODE 
from database.ia_filterdb import save_file
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import temp
import re
import humanize
from info import ADMINS 
from lazybot import LazyPrincessBot 


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lock = asyncio.Lock()
semaphore = asyncio.Semaphore(1) # create a semaphore with initial value of 1

@Client.on_callback_query(filters.regex(r'^index'))
async def index_files(bot, query):
    if query.data.startswith('index_cancel'):
        temp.CANCEL = True
        return await query.answer("Cancelling Indexing")
    _, raju, chat, lst_msg_id, from_user = query.data.split("#")
    if raju == 'reject':
        await query.message.delete()
        await bot.send_message(int(from_user),
                               f'Your Submission for indexing {chat} has been decliened by our moderators.',
                               reply_to_message_id=int(lst_msg_id))
        return

    if lock.locked():
        return await query.answer('Wait until previous process complete.', show_alert=True)
    msg = query.message

    await query.answer('Processing...⏳', show_alert=True)
    if int(from_user) not in ADMINS:
        await bot.send_message(int(from_user),
                               f'Your Submission for indexing {chat} has been accepted by our moderators and will be added soon.',
                               reply_to_message_id=int(lst_msg_id))
    await msg.edit(
        "Starting Indexing",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('Cancel', callback_data='index_cancel')]]
        )
    )
    try:
        chat = int(chat)
    except:
        chat = chat
    await index_files_to_db(int(lst_msg_id), chat, msg, bot)


@Client.on_message((filters.forwarded | (filters.regex("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")) & filters.text ) & filters.private & filters.incoming)
async def send_for_index(bot, message):
    if message.text:
        regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(message.text)
        if not match:
            return await message.reply('Invalid link')
        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id  = int(("-100" + chat_id))
    elif message.forward_from_chat.type == enums.ChatType.CHANNEL:
        last_msg_id = message.forward_from_message_id
        chat_id = message.forward_from_chat.username or message.forward_from_chat.id
    else:
        return
    try:
        await bot.get_chat(chat_id)
    except ChannelInvalid:
        return await message.reply('This may be a private channel / group. Make me an admin over there to index the files.')
    except (UsernameInvalid, UsernameNotModified):
        return await message.reply('Invalid Link specified.')
    except Exception as e:
        logger.exception(e)
        return await message.reply(f'Errors - {e}')
    try:
        k = await bot.get_messages(chat_id, last_msg_id)
    except:
        return await message.reply('Make Sure That i am An Admin In The Channel, if channel is private')
    if k.empty:
        return await message.reply('This may be group and i am not a admin of the group.')

    if message.from_user.id in ADMINS:
        if (LAZY_MODE==True):
            file = getattr(message, message.media.value)
            filename = file.file_name
            filesize = humanize.naturalsize(file.file_size) 
            buttons = [
                [ InlineKeyboardButton("📝✧ S𝚝ar𝚝 re𝚗aᗰi𝚗g ✧📝", callback_data="rename") ],
                [ InlineKeyboardButton('📇✧✧  S𝚝ar𝚝 iŋdᗴＸi𝚗g  ✧✧📇',callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')],
                [ InlineKeyboardButton('⨳  C L Ф S Ξ  ⨳', callback_data='cancel'),]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            return await message.reply(
                f'\n⨳ *•.¸♡ LΛＺ𝐲 ＭⓄｄ𝓔 ♡¸.•* ⨳\n\n**__What do you want me to do with this file.?__**\n\n🪬Chat ID/ Username: <code>{chat_id}</code>\nℹ️Last Message ID: <code>{last_msg_id}</code> \n\n🎞**File Name** :- `{filename}`\n\n⚙️**File Size** :- `{filesize}`',
                reply_to_message_id=message.id,
                reply_markup=reply_markup)
        else:
            buttons = [
                [
                    InlineKeyboardButton('Yes',
                                         callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')
                ],
                [
                    InlineKeyboardButton('⨳  C L Ф S Ξ  ⨳', callback_data='close_data'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            return await message.reply(
                f'Do you Want To Index This Channel/ Group ?\n\nChat ID/ Username: <code>{chat_id}</code>\nLast Message ID: <code>{last_msg_id}</code>',
                reply_markup=reply_markup)

    if type(chat_id) is int:
        try:
            link = (await bot.create_chat_invite_link(chat_id)).invite_link
        except ChatAdminRequired: 
            return await message.reply('Make sure i am an admin in the chat and have permission to invite users.')
    else:
        link = f"@{message.forward_from_chat.username}"
    buttons = [
        [
            InlineKeyboardButton('Request Index',
                                 callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')
        ],
        [
            InlineKeyboardButton('Reject Index',
                                 callback_data=f'index#reject#{chat_id}#{message.id}#{message.from_user.id}'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await bot.send_message(LOG_CHANNEL,
                           f'#IndexRequest\n\nBy : {message.from_user.mention} (<code>{message.from_user.id}</code>)\nChat ID/ Username - <code> {chat_id}</code>\nLast Message ID - <code>{last_msg_id}</code>\nInviteLink - {link}',
                           reply_markup=reply_markup)
    if (LAZY_MODE == True):
        if message.from_user.id in LAZY_RENAMERS:
            k = await message.reply('🎉\n\n\n❤️ Thank You For the Contribution, Wait For My Moderators to verify the files.\n\n\n🎁')
            buttons = [
                        [InlineKeyboardButton("📝✧✧ S𝚝ar𝚝 re𝚗aᗰi𝚗g ✧✧📝", callback_data="rename") ],
                        [InlineKeyboardButton('⨳  C L Ф S Ξ  ⨳', callback_data='cancel')]]
            reply_markup = InlineKeyboardMarkup(buttons)
            file = getattr(message, message.media.value)
            filename = file.file_name
            filesize = humanize.naturalsize(file.file_size) 
            await message.reply(
                                f".\n⨳ *•.¸♡ LΛＺ𝐲 ＭⓄｄ𝓔 ♡¸.•* ⨳\n\nBecause you are an Authentic user, please don't hesitate to ask me for any other help...\n\n🪬Chat ID/ Username: <code>{chat_id}</code>\nℹ️Last Message ID: <code>{last_msg_id}</code> \n\n🎞**File Name** :- `{filename}`\n\n⚙️**File Size** :- `{filesize}`\n\nYou can simply close this window or perform following actions, it's upon you",
                                reply_to_message_id=message.id,
                                reply_markup=reply_markup)
            await asyncio.sleep(600)
            await k.delete()
        else :      
            await message.reply('🎉\n\n\n❤️ Thank You For the Contribution, Wait For My Moderators to verify the files.\n\n\n🎁')
            buttons = [
                        [InlineKeyboardButton("📝✧✧ S𝚝ar𝚝 re𝚗aᗰi𝚗g ✧✧📝", callback_data="requireauth") ],
                        [InlineKeyboardButton('⨳  C L Ф S Ξ  ⨳', callback_data='cancel')]]
            reply_markup = InlineKeyboardMarkup(buttons)
            file = getattr(message, message.media.value)
            filename = file.file_name
            filesize = humanize.naturalsize(file.file_size) 
            k = await message.reply(
                                f"\n⨳ *•.¸♡ LΛＺ𝐲 ＭⓄｄ𝓔 ♡¸.•* ⨳\n\n🤩 Do you know LazyPrincess can do a lot of things at a time...\nWould you like to try some of it's amazing features... \n\n🪬Chat ID/ Username: <code>{chat_id}</code>\nℹ️Last Message ID: <code>{last_msg_id}</code> \n\n🎞**File Name** :- `{filename}`\n\n⚙️**File Size** :- `{filesize}`",
                                reply_to_message_id=message.id,
                                reply_markup=reply_markup)
            await asyncio.sleep(600)
            await k.delete()
    else:
        await message.reply('🎉\n\n\n❤️ Thank You For the Contribution, Wait For My Moderators to verify the files.\n\n\n🎁')
 

@Client.on_message(filters.command('setskip') & filters.user(ADMINS))
async def set_skip_number(bot, message):
    if ' ' in message.text:
        _, skip = message.text.split(" ")
        try:
            skip = int(skip)
        except:
            return await message.reply("Skip number should be an integer.")
        await message.reply(f"Successfully set SKIP number as {skip}")
        temp.CURRENT = int(skip)
    else:
        await message.reply("Give me a skip number")



async def index_files_to_db(lst_msg_id, chat, msg, bot):
    total_files = 0
    duplicate = 0
    errors = 0
    deleted = 0
    no_media = 0
    unsupported = 0
    async with lock:
        try:
            current = temp.CURRENT
            temp.CANCEL = False
            async for message in bot.iter_messages(chat, lst_msg_id, temp.CURRENT):
                if temp.CANCEL:
                    await msg.edit(f"Successfully Cancelled!!\n\nSaved <code>{total_files}</code> files to dataBase!\nDuplicate Files Skipped: <code>{duplicate}</code>\nDeleted Messages Skipped: <code>{deleted}</code>\nNon-Media messages skipped: <code>{no_media + unsupported}</code>(Unsupported Media - `{unsupported}` )\nErrors Occurred: <code>{errors}</code>")
                    break
                current += 1
                if current % 20 == 0:
                    can = [[InlineKeyboardButton('Cancel', callback_data='index_cancel')]]
                    reply = InlineKeyboardMarkup(can)
                    await msg.edit_text(
                        text=f"Total messages fetched: <code>{current}</code>\nTotal messages saved: <code>{total_files}</code>\nDuplicate Files Skipped: <code>{duplicate}</code>\nDeleted Messages Skipped: <code>{deleted}</code>\nNon-Media messages skipped: <code>{no_media + unsupported}</code>(Unsupported Media - `{unsupported}` )\nErrors Occurred: <code>{errors}</code>",
                        reply_markup=reply)
                if message.empty:
                    deleted += 1
                    continue
                elif not message.media:
                    no_media += 1
                    continue
                elif message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.AUDIO, enums.MessageMediaType.DOCUMENT]:
                    unsupported += 1
                    continue
                media = getattr(message, message.media.value, None)
                if not media:
                    unsupported += 1
                    continue
                media.file_type = message.media.value
                media.caption = message.caption
                aynav, vnay = await save_file(media)
                if aynav:
                    total_files += 1
                elif vnay == 0:
                    duplicate += 1
                elif vnay == 2:
                    errors += 1
        except Exception as e:
            logger.exception(e)
            await msg.edit(f'Error baby: {e}')
        else:
            await msg.edit(f'Succesfully saved <code>{total_files}</code> to dataBase!\nDuplicate Files Skipped: <code>{duplicate}</code>\nDeleted Messages Skipped: <code>{deleted}</code>\nNon-Media messages skipped: <code>{no_media + unsupported}</code>(Unsupported Media - `{unsupported}` )\nErrors Occurred: <code>{errors}</code>')
