import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
import asyncpg
from app import app
import logging
from sqlalchemy.util import concurrency


DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/hypertictactoe'

log = logging.getLogger(__name__)

class DB:

	def __init__(self):
		self._pool = None

	async def startup(self):
		self._pool = await asyncpg.create_pool(dsn=DATABASE_URL, min_size=10, max_size=10, max_inactive_connection_lifetime=60)

	async def shutdown(self):
		await self._pool.close()

	def getPool(self):
		print(f'returned pool: type {type(self._pool)}')
		return self._pool

db = DB()

@app.on_event('startup')
async def startup():
	await db.startup()

@app.on_event('shutdown')
async def startup():
	await db.shutdown()

