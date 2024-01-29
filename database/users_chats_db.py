# https://github.com/odysseusmax/animated-lamp/blob/master/bot/database/database.py
import motor.motor_asyncio
import datetime
from info import DATABASE_NAME, DATABASE_URI, IMDB, IMDB_TEMPLATE, MELCOW_NEW_USERS, P_TTI_SHOW_OFF, SINGLE_BUTTON, SPELL_CHECK_REPLY, PROTECT_CONTENT, MAX_BTN

class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.grp = self.db.groups

    def new_user(self, id, name):
        return dict(    
            id = id,
            name = name,
            _id=int(id),                                   
            file_id=None,
            caption=None,
            lazy_caption=None,
            join_date=datetime.date.today().isoformat(),
            apply_caption=True,
            upload_as_doc=False,
            thumbnail=None,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
        )

    def new_group(self, id, title):
        return dict(
            id = id,
            title = title,
            chat_status=dict(
                is_disabled=False,
                is_lazy_verified=False,
                reason="",
            ),
        )
    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return bool(user)
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
    
    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_reason=''
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})
    
    async def ban_user(self, user_id, ban_reason="No Reason"):
        ban_status = dict(
            is_banned=True,
            ban_reason=ban_reason
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_reason=''
        )
        user = await self.col.find_one({'id':int(id)})
        if not user:
            return default
        return user.get('ban_status', default)

    async def get_all_users(self):
        return self.col.find({})
    
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})
                
    async def get_banned(self):
        users = self.col.find({'ban_status.is_banned': True})
        chats = self.grp.find({'chat_status.is_disabled': True})
        is_verified = self.grp.find({'chat_status.is_lazy_verified': True})
        b_chats = [chat['id'] async for chat in chats]
        b_users = [user['id'] async for user in users]
        lz_verified = [chat['id'] async for chat in is_verified]
        return b_users, b_chats, lz_verified

    async def add_chat(self, chat, title):
        chat = self.new_group(chat, title)
        await self.grp.insert_one(chat)
    
    async def get_chat(self, chat):
        chat = await self.grp.find_one({'id':int(chat)})
        return False if not chat else chat.get('chat_status')
    
    async def re_enable_chat(self, id):
        chat_status=dict(
            is_disabled=False,
            reason="",
            )
        await self.grp.update_one({'id': int(id)}, {'$set': {'chat_status': chat_status}})
        
    async def update_settings(self, id, settings):
        await self.grp.update_one({'id': int(id)}, {'$set': {'settings': settings}})
    
    async def get_settings(self, id):
        default = {
            'button': SINGLE_BUTTON,
            'botpm': P_TTI_SHOW_OFF,
            'file_secure': PROTECT_CONTENT,
            'imdb': IMDB,
            'spell_check': SPELL_CHECK_REPLY,
            'welcome': MELCOW_NEW_USERS,
            'template': IMDB_TEMPLATE,
            'max_btn': MAX_BTN,

        }
        chat = await self.grp.find_one({'id':int(id)})
        if chat:
            return chat.get('settings', default)
        return default

    async def disable_chat(self, chat, reason="No Reason"):
        chat_status=dict(
            is_disabled=True,
            reason=reason,
            )
        await self.grp.update_one({'id': int(chat)}, {'$set': {'chat_status': chat_status}})

    async def verify_lazy_chat(self, chat):
        chat_status=dict(
            is_lazy_verified=True,
            )
        await self.grp.update_one({'id': int(chat)}, {'$set': {'chat_status': chat_status}})
    

    async def total_chat_count(self):
        count = await self.grp.count_documents({})
        return count
    

    async def get_all_chats(self):
        return self.grp.find({})

    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']
    
    # Credit @LazyDeveloper.
    # Please Don't remove credit.
        # Born to make history @LazyDeveloper ! => Remember this name forever <=

    # Thank you LazyDeveloper for helping us in this Journey
    # Just for url Uploading feature

    async def set_apply_caption(self, id, apply_caption):
        await self.col.update_one({'id': id}, {'$set': {'apply_caption': apply_caption}})

    async def get_apply_caption(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('apply_caption', True)

    async def set_upload_as_doc(self, id, upload_as_doc):
        await self.col.update_one({'id': id}, {'$set': {'upload_as_doc': upload_as_doc}})

    async def get_upload_as_doc(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('upload_as_doc', False)

    async def set_lazy_thumbnail(self, id, thumbnail):
        await self.col.update_one({'id': id}, {'$set': {'thumbnail': thumbnail}})

    async def get_lazy_thumbnail(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('thumbnail', None)

    async def get_lazy_caption(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('lazy_caption', None)

    async def get_user_data(self, id) -> dict:
        user = await self.col.find_one({'id': int(id)})
        return user or None
        
    # Thank you LazyDeveloper for helping us in this Journey
    # Just for renamer @LazyDeveloper 
    async def set_thumbnail(self, id, file_id):
        await self.col.update_one({'id': int(id)}, {'$set': {'file_id': file_id}})
        
    async def get_thumbnail(self, id):
        try:
            thumbnail = await self.col.find_one({'id': int(id)})
            if thumbnail:
                return thumbnail.get('file_id')
            else:
                return None
        except Exception as e:
            print(e)
    # Born to make history @LazyDeveloper ! => Remember this name forever <=

    async def set_caption(self, id, caption):
        await self.col.update_one({'id': int(id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('caption', None)


db = Database(DATABASE_URI, DATABASE_NAME)
