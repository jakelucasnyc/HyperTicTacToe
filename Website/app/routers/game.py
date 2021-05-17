from fastapi import APIRouter, Response, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from app.db import db, Games
import random
from app.pydanticModels import createGame
import asyncio
import json

router = APIRouter()

@router.post('/create', status_code=201)
async def createGame(data: createGame, engine: AsyncEngine = Depends(db.getEngine)):

	async with AsyncSession(engine) as conn:
		async with conn.begin():
			dataDict = {
				'limit': int(data.limit),
				'increment': int(data.increment)
			}

			if data.name:
				if data.side == 'X':
					dataDict.update({'player_x': data.name})
				else:
					dataDict.update({'player_o': data.name})

			newGame = Games(**dataDict)
			conn.add(newGame)
			res = await conn.flush()
			id = newGame.id
		return JSONResponse(content={'id': id})


@router.post('/{id}/move/{move}', status_code=200)
async def move(id: int, move: str, engine: AsyncEngine = Depends(db.getEngine)):

	async with AsyncSession(engine) as conn:
		async with conn.begin():
			game = await conn.get(Games, id)

			if game is None:
				raise HTTPException(status_code=404, detail=f"Game with id '{id}' doesn't exist")

			if game.moves:
				game.moves = game.moves + ' '
			game.moves = game.moves + move
			await conn.flush()
			return JSONResponse(content={'ok': True})



