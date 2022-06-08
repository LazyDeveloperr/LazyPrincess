from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.connections_mdb import add_connection, all_connections, if_active, delete_connection
from info import ADMINS
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


@Client.on_message((filters.private | filters.group) & filters.command('connect'))
async def addconnection(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"Oye Anzaan Admin ji, kripaa kr ye command ko mujhe kopche m bhejo 👉 Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == "private":
        try:
            cmd, group_id = message.text.split(" ", 1)
        except:
            await message.reply_text(
                "<b>Enter in correct format!</b>\n\n"
                "<code>/connect groupid</code>\n\n"
                "<i>Group id lene liye, mujhe us group mei add kr ke ye command dein 👉 <code>/id</code></i>",
                quote=True
            )
            return

    elif chat_type in ["group", "supergroup"]:
        group_id = message.chat.id

    try:
        st = await client.get_chat_member(group_id, userid)
        if (
                st.status != "administrator"
                and st.status != "creator"
                and userid not in ADMINS
        ):
            await message.reply_text("Pehle aapko is group mei Admin banna prega.", quote=True)
            return
    except Exception as e:
        logger.exception(e)
        await message.reply_text(
            "Group ID galat hai!\n\nAgar sahi hai, toh ek dfa check kijiye ki main is group main hu ya nhi!!",
            quote=True,
        )

        return
    try:
        st = await client.get_chat_member(group_id, "me")
        if st.status == "administrator":
            ttl = await client.get_chat(group_id)
            title = ttl.title

            addcon = await add_connection(str(group_id), str(userid))
            if addcon:
                await message.reply_text(
                    f"Badhai ho! main **{title}** se connect ho gyi hu...\n Ab aap mujhe kopche mei milo!",
                    quote=True,
                    parse_mode="md"
                )
                if chat_type in ["group", "supergroup"]:
                    await client.send_message(
                        userid,
                        f"Connected to **{title}** !",
                        parse_mode="md"
                    )
            else:
                await message.reply_text(
                    "Arey jaanemann ! Main is chat se already judi hui hu... 🤦‍♀️ !",
                    quote=True
                )
        else:
            await message.reply_text("Group mei mujhe Admin bnaao", quote=True)
    except Exception as e:
        logger.exception(e)
        await message.reply_text('kya grbr krr daala re, ek dfa fir se try kro 🤦‍♀️!', quote=True)
        return


@Client.on_message((filters.private | filters.group) & filters.command('disconnect'))
async def deleteconnection(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"Oye Anzaan Admin ji, kripaa kr ye command ko mujhe kopche m bhejo 👉 Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == "private":
        await message.reply_text("Connected groups ko dekhne ke liye ya group ko disconnect krne ke liye /connections type kro !", quote=True)

    elif chat_type in ["group", "supergroup"]:
        group_id = message.chat.id

        st = await client.get_chat_member(group_id, userid)
        if (
                st.status != "administrator"
                and st.status != "creator"
                and str(userid) not in ADMINS
        ):
            return

        delcon = await delete_connection(str(userid), str(group_id))
        if delcon:
            await message.reply_text("Chal Sona, Chat disconnect ho gya , ab aage kya krna hai ?", quote=True)
        else:
            await message.reply_text("Sona ! is chat se toh main connected hu hi nhi!\nAgar connect krna h toh mujhe /connect command do !", quote=True)


@Client.on_message(filters.private & filters.command(["connections"]))
async def connections(client, message):
    userid = message.from_user.id

    groupids = await all_connections(str(userid))
    if groupids is None:
        await message.reply_text(
            "Sona ! Main ab tk kisi v chat se connected nhi hu!! Pehle kisi group se connect kro mujhe !",
            quote=True
        )
        return
    buttons = []
    for groupid in groupids:
        try:
            ttl = await client.get_chat(int(groupid))
            title = ttl.title
            active = await if_active(str(userid), str(groupid))
            act = " - ACTIVE" if active else ""
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                    )
                ]
            )
        except:
            pass
    if buttons:
        await message.reply_text(
            "Your connected group details;\n\n",
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
    else:
        await message.reply_text(
            "Sona ! Main ab tk kisi v group se connected nhi hu!! Pehle kisi group se connect kro mujhe !",
            quote=True
        )
