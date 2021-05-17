from fastapi import APIRouter, Response, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from app.db import db, Games
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
import asyncio
import json
from sse_starlette.sse import EventSourceResponse, ServerSentEvent


router = APIRouter()

@router.get('/game/{id}/events')
async def getGameEvents(id: int, request: Request, engine: AsyncEngine = Depends(db.getEngine)):

	def createStatusFromGameInst(game):
		returnDict = {
			'moves': game.moves,
			'player_x': game.player_x,
			'player_o': game.player_o,
			'in_progress': game.in_progress,
			'x_joined': game.x_joined,
			'o_joined': game.o_joined,
			'outcome': game.outcome,
			'winner': game.winner
		}
		return returnDict

	async with AsyncSession(engine) as conn:
		currentGame = await conn.get(Games, id)

		if currentGame is None:
			return JSONResponse(status_code=404, content={'detail': f"Game with id {{{id}}} does not exist"})

		async def stream(engine: AsyncEngine = engine, 
													 request: Request = request, 
													 conn: AsyncSession = conn, 
													 currentGame: Games = currentGame):

			currentGame = await conn.get(Games, id)
			prevMoves = currentGame.moves

			while True:
				if await request.is_disconnected():
					print('Lost Connection. Exiting.')
					break

				await conn.refresh(currentGame)
				
				if prevMoves != currentGame.moves:
					print(f'\nCurrent != Prev\nmoves: {currentGame.moves}\n')
					prevMoves = currentGame.moves
					yield ServerSentEvent(data=createStatusFromGameInst(currentGame)).encode()
					await asyncio.sleep(0.5)
				else:
					print(f'\nCurrent == Prev\nmoves: {currentGame.moves}\n')
					await asyncio.sleep(3)

		headers = {
			'Connection': 'keep-alive',
			'Cache-Control': 'no-cache'
		}

		return EventSourceResponse(stream(engine, request, conn), headers=headers, media_type='text/event-stream')


