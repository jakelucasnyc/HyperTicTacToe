from sqlalchemy.event import listens_for
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import asyncpg
from app import app
import logging
from sqlalchemy.util import concurrency
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.future import select

Base = declarative_base()

DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5432/hypertictactoe'

log = logging.getLogger(__name__)

class DB:

	def __init__(self):
		self._engine = None
		# self._meta = sqlalchemy.MetaData()
		# self.games = sqlalchemy.Table('games', self._meta,
		# 															sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
		# 															sqlalchemy.Column('player_x', sqlalchemy.String(30), default='Player_X'),
		# 															sqlalchemy.Column('player_o', sqlalchemy.String(30), default='Player_O'),
		# 															sqlalchemy.Column('moves', sqlalchemy.Text, default=''),
		# 															sqlalchemy.Column('limit', sqlalchemy.Integer, nullable=False),
		# 															sqlalchemy.Column('increment', sqlalchemy.Integer, nullable=False),
		# 															sqlalchemy.Column('in_progress', sqlalchemy.Boolean, default=True),
		# 															sqlalchemy.Column('x_joined', sqlalchemy.Boolean, default=False),
		# 															sqlalchemy.Column('o_joined', sqlalchemy.Boolean, default=False),
		# 															sqlalchemy.Column('outcome', sqlalchemy.String(20)),
		# 															sqlalchemy.Column('winner', sqlalchemy.String(1)),
		# 															)
		self.gameSession = sessionmaker(self._engine, class_=AsyncSession)

	async def startup(self):
		# , echo=True, echo_pool=True
		self._engine = create_async_engine(DATABASE_URL, echo_pool=True, pool_size=10)
		async with self._engine.begin() as conn:

			await conn.run_sync(Base.metadata.create_all)

	# async def shutdown(self):
	# 	await self._engine.close()

	def getEngine(self):
		return self._engine

	def getGameSession(self):
		return self.gameSession

	# @listens_for(self.gameSession, '')

db = DB()

@app.on_event('startup')
async def startup():
	await db.startup()

# @app.on_event('shutdown')
# async def startup():
# 	await db.shutdown()


class Games(Base):
	__tablename__ = 'games'

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False, autoincrement=True)
	player_x = sqlalchemy.Column(sqlalchemy.String(30), default='Player_X')
	player_o = sqlalchemy.Column(sqlalchemy.String(30), default='Player_O')
	moves = sqlalchemy.Column(sqlalchemy.Text, default='')
	limit = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
	increment = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
	in_progress = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
	x_joined = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
	o_joined = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
	outcome = sqlalchemy.Column(sqlalchemy.String(20))
	winner = sqlalchemy.Column(sqlalchemy.String(1))

	def __repr__(self):
		return f'Game(id={self.id}'


