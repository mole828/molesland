
from connect.mongo import client
from motor.core import Database, Collection

async def main():
    print(await client.list_database_names())
    db:Database = client.get_database('arknights')
    print(await db.list_collection_names())
    col:Collection = db.get_collection('user')
    try:
        await col.insert_one({
            '_id': '16259809679',
            'pwd': '42466583',
        })
    except Exception as e:
        print('catch: ',e)
    finally:
        print('finally')

    async for user in col.find({}):
        print(user)

    # docs = db.get_collection('doctors')
    # dic:dict = await docs.find_one({'uid': '14697657'})
    # from service.gacha.model import Doctor
    # doc = Doctor(**dic)
    # print(doc)
    # from service.gacha.ArkNightsApi import gachaiter
    # col = db.get_collection('gachas')
    # for gacha in gachaiter(doc.token):
    #     print(gacha)
    #     await col.update_one({'uid':gacha.uid, 'ts':gacha.ts},{'$set':gacha.dict()})

if __name__ == '__main__':
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())