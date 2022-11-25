
from connect.mongo import client

from motor.motor_asyncio import AsyncIOMotorDatabase
from motor.core import Database

async def main():
    db:Database = client.get_database('moles')
    print(await db.list_collection_names())
    docs = db.get_collection('doctors')
    dic:dict = await docs.find_one({'uid': '14697657'})
    from service.gacha.model import Doctor
    doc = Doctor(**dic)
    print(doc)
    from service.gacha.ArkNightsApi import gachaiter
    col = db.get_collection('gachas')
    for gacha in gachaiter(doc.token):
        print(gacha)
        await col.update_one({'uid':gacha.uid, 'ts':gacha.ts},{'$set':gacha.dict()})

import asyncio
asyncio.get_event_loop().run_until_complete(main())