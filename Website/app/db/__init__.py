import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
import asyncpg
from app import app
import logging
from sqlalchemy.util import concurrency
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5432/hypertictactoe'

log = logging.getLogger(__name__)

class DB:

	def __init__(self):
		self._engine = None

	async def startup(self):
		self._engine = create_async_engine(DATABASE_URL, echo=True, echo_pool=True, pool_size=10)

	async def shutdown(self):
		await self._engine.close()

	def getEngine(self):
		print(f'returned pool: type {type(self._pool)}')
		return self._engine

db = DB()

@app.on_event('startup')
async def startup():
	await db.startup()

@app.on_event('shutdown')
async def startup():
	await db.shutdown()

