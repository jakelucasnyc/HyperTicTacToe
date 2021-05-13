from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse, StreamingResponse
import asyncio
import json


router = APIRouter()

headers = {
	'Content-Type': 'application/json'
}

@router.get('/test/')
def test():

	returnDict = {
		'data' : 'randomness'
	}

	return returnDict

@router.post('/test/')
def testPost():
	pass

@router.get('/testStream')
async def testStream():

	async def streamer():
		for i in range(10):
			await asyncio.sleep(1)
			yield b"some fake video bytes\n"

	return StreamingResponse(streamer())

@router.get('/testStream/{id}')
async def testStreamId(id: int):

	async def streamer():
		for i in range(10):
			await asyncio.sleep(1)
			yield json.dumps({'id': id}) + '\n'

	return StreamingResponse(streamer())



	





