from flask import render_template, jsonify, url_for, redirect, Blueprint
from app.models import Game

base = Blueprint('base', __name__)

@base.route('/home')
@base.route('/')
def home():
	return render_template('home.html')


@base.route('/game/')
def login():
	return render_template('game.html')