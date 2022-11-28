from typing import Dict, List
from motor.core import Database


from .model import Doctor, Gacha

def defaultRouter(database: Database):
    from fastapi import APIRouter
    router = APIRouter()

    @router.get('/doctors/map')
    async def doctorsMap() -> Dict[str, Doctor]:
        return {
            doc['uid']: doc
            async for doc in database.get_collection('doctors').find(
                filter={},
                projection={
                    '_id': False,
                    '__v': False,
                    'token': False,
                }
            )
        }

    @router.get('/gachas/list')
    async def gachasList(uid: str = None, page: int = 0,  size: int = 10) -> List[Gacha]:
        filter = {'uid': uid}
        return [
            gacha async for gacha in database.get_collection('gachas').find(
                filter={
                    key: filter[key] for key in filter if filter[key]
                },
                projection={
                    '_id': False,
                },
            ).skip(page*size).limit(size)
        ]

    from .analyst import analystOne, analysts
    @router.on_event('startup')
    async def analystAll():
        from loguru import logger
        import time
        
        begin = time.time()
        async for gd in database.get_collection('gachas').find(filter={},projection={'_id':False}):
            try:
                gacha = Gacha(**gd)
            except Exception:
                logger.error({'uid':gd['uid'], 'ts':gd['ts']})
            else:
                analystOne(gacha=gacha)
        end = time.time()
        summary = analysts['']['']
        logger.info({k:summary[k] for k in summary})
        logger.info(f'analystAll() speed {(end-begin):.2f}s')

    @router.get('/analyst')
    async def analyst(uid: str = None):
        return analysts[uid]

    return router
