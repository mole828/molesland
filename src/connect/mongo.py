from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient
uri = "mongodb://moleserver:27017"

client: AgnosticClient = AsyncIOMotorClient(uri)


async def __main():
    print('database_names:',await client.list_database_names())
    

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__main())