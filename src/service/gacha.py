from src.connect.mongo import client as mongoclient
from pymongo.database import Database

database: Database = mongoclient.get_database('gacha')

from fastapi import APIRouter

router = APIRouter()


async def users():
    return 

async def printAll():
    cur = database.get_collection('test').find()
    print(cur)


if __name__ == '__main__':
    import asyncio
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(printAll())
