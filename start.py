import os
import asyncio
import uvicorn
from database.db_connection import init_models
from dotenv import load_dotenv
from api.api import app

async def start():
    load_dotenv()
    HOST = os.getenv('LOCALHOST')
    PORT = int(os.getenv('BACKEND_PORT'))

    config = uvicorn.Config(app, host=HOST, port=PORT, log_level="info", )
    await init_models()
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == '__main__':
    asyncio.run(start())