from fastapi import APIRouter, Response, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from app.db import db
import random
from app.pydanticModels import createGame
import asyncio
import json
from asyncpg import Pool

router = APIRouter()

@router.post('/create', status_code=201)
async def createGame(data: createGame, pool: Pool = Depends(db.getPool)):

	async with pool.acquire() as conn:
		dataDict = {
			'limit': int(data.limit),
			'increment': int(data.increment)
		}

		if data.name:
			if data.side == 'X':
				dataDict.update({'player_x': data.name})
			else:
				dataDict.update({'player_o': data.name})


		tableNameFormatList = []
		valueFormatList = []

		for i in range(len(dataDict)):

			currentKey = list(dataDict.keys())[i]
			currentVal = dataDict[currentKey]

			tableNameFormatList.append(f'"{currentKey}"')

			if type(currentVal) == str:
				print('val is string')
				valueFormatList.append(f"'{currentVal}'")
			else:
				print('val is not a string')
				valueFormatList.append(f'{currentVal}')

			

		tableNameFormatString = ', '.join(tableNameFormatList)
		valueFormatString = ', '.join(valueFormatList)

		createGameQuery = '''INSERT INTO games ({0})
											VALUES ({1});'''.format(tableNameFormatString, valueFormatString)

		# print(createGameQuery)

		id = await conn.execute(createGameQuery)
		return JSONResponse(content={'id': id})


@router.post('/{id}/move/{move}', status_code=200)
async def move(id: int, move: str, pool: Pool = Depends(db.getPool)):

	async with pool.acquire() as conn:

		#getting current moves
		selectGame = '''
								 SELECT moves FROM public.games
								 WHERE id = $1;
								 '''

		game = await conn.fetchrow(selectGame, id)

		# if the game doesn't exist yet
		if not 'moves' in game.keys():
			raise HTTPException(status_code=404, detail=f"Game with id '{id}' doesn't exist")

		gameMoves = game['moves']
		#if at least one move has been made
		if gameMoves:
			gameMoves += ' '

		gameMoves += move
		updateMoves = '''
									UPDATE public.games
										SET
											moves = $1

										WHERE id = $2;
									'''
		await conn.execute(updateMoves, gameMoves, id)
		return JSONResponse(content={'ok': True})



