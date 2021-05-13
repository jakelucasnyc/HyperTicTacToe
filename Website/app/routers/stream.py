from fastapi import APIRouter, Response, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from app.db import db
import asyncio
import json
from asyncpg import Pool

router = APIRouter()

@router.post('/game/{id}/events')
async def getGameEvents(id: int, pool: Pool = Depends(db.getPool)):
	db.execute('LISTEN games;')
	db.connection.poll()

