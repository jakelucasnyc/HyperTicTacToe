from flask import Blueprint, make_response, request, jsonify
from flask_cors import CORS
from app.models import Game
from app import db


api = Blueprint('api', __name__)
CORS(api)

headers = {
	'Content-Type': 'application/json'
}

@api.route('/test/', methods=['GET', 'POST'])
def test():

	returnDict = {
		'data' : 'randomness'
	}

	response = make_response(returnDict)
	# response.headers.add('Access-Control-Allow-Origin', '*')

	print('Data: ', request.data)
	print('JSON: ', request.get_json())
	print('Form: ', request.form)
	print('Args: ', request.values)
	print('Values: ', request.values)

	return response

@api.route('game/create/')
def createGame():
	game = Game()

@api.route('/game/<int:id>/all/', methods=['GET'])
def allGameData(id):
	pass

@api.route('/game/<int:id>/lastMove/', methods=['POST'])
def lastMove(id):
	pass



