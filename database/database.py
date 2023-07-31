#(©)CodeXBotz




import pymongo, os
from config import DB_URI, DB_NAME


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]


user_data = database['users']
req_data = database['reqs']


async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    if found:
        return True
    else:
        return False

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

async def add_req(user_id, channel_id):
    try:
        req_data.insert_one({"_id": str(user_id) + str(channel_id),
                             "user_id": int(user_id),
                             "channel_id": int(channel_id)})
    except Exception as e:
            print(f"Error adding request: {e}")


async def is_req_exist(user_id, channel_id):
    try:
        doc = req_data.find_one({"_id": str(user_id) + str(channel_id)})
        return doc is not None
    except Exception as e:
        print(f"Error checking if id exists: {e}")
        return False

async def get_req_count(channel_id):
    try:
        count = req_data.count_documents({"channel_id": int(channel_id)})
        return count
    except Exception as e:
        print(f"Error getting request count by channel_id: {e}")
        return 0

async def get_missing_channel_ids(user_id, channel_ids):
    try:
        saved_channel_ids = [str(user_id) + str(channel_id) for channel_id in channel_ids]
        docs = req_data.find({"_id": {"$in": saved_channel_ids}})
        saved_ids = [doc["_id"][len(str(user_id)):] for doc in docs]
        missing_ids = [channel_id for channel_id in channel_ids if channel_id not in saved_ids]
        return missing_ids
    except Exception as e:
        print(f"Error finding missing channel_ids: {e}")
        return channel_ids

async def is_requested(message, channel_ids):
    missing_channel_ids = await get_missing_channel_ids(message.from_user.id, channel_ids)
    if not missing_channel_ids or message.from_user.id in ADMINS:
        return True, missing_channel_ids
    return False, missing_channel_ids
    
async def delete_all_req(channel_id):
    try:
        await req_data.delete_many({"channel_id": int(channel_id)})
    except Exception as e:
        print(f"Error deleting requests by channel_id: {e}")
