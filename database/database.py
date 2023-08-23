#(©)CodeXBotz
import pymongo, os
from config import DB_URI, DB_NAME, ADMINS


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]


user_data = database['users']

req_one = database['req_one']  
req_two = database['req_two']

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


async def is_requested_one(message):
    user = await get_req_one(message.from_user.id)
    if user:
        return True
    if message.from_user.id in ADMINS:
        return True
    return False
    
async def is_requested_two(message):
    user = await get_req_two(message.from_user.id)
    if user:
        return True
    if message.from_user.id in ADMINS:
        return True
    return False

async def add_req_one(user_id):
    try:
        if not await get_req_one(user_id):
            await req_one.insert_one({"user_id": int(user_id)})
            return
    except:
        pass
        
async def add_req_two(user_id):
    try:
        if not await get_req_two(user_id):
            await req_two.insert_one({"user_id": int(user_id)})
            return
    except:
        pass

async def get_req_one(user_id):
    return req_one.find_one({"user_id": int(user_id)})

async def get_req_two(user_id):
    return req_two.find_one({"user_id": int(user_id)})

async def delete_all_one():
    req_one.delete_many({})

async def delete_all_two():
    req_two.delete_many({})

