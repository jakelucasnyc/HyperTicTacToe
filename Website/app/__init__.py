from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncpg
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)
log.setLevel(logging.INFO)
app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins = '*',
	allow_credentials = True,
	allow_methods = '*',
	allow_headers = '*'
)




from app.routers import api, game, stream

app.include_router(api.router, prefix='/api')
app.include_router(game.router, prefix='/api/game')
app.include_router(stream.router, prefix='/api/stream')
