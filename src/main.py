import logging
import fastapi
app = fastapi.FastAPI()
from connect.mongo import client

from service.gacha import defaultRouter as gachaRouter
app.include_router(gachaRouter(client.get_database('moles')), prefix='/ark')

@app.on_event('startup')
def test():
    from loguru import logger
    logger.info('app startup')

@app.get('/')
def _():
    return {'hello':'world'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)