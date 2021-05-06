from app import db

class Game(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	moves = db.Column(db.Text, default='')
	xPlayerName = db.Column(db.String(30), nullable=False, default='Player_X')
	oPlayerName = db.Column(db.String(30), nullable=False, default='Player_O')

	def __repr__(self):

		return f'Game(X: "{self.xPlayerName}", O: "{self.oPlayerName}", moves: "{self.moves}", id: {self.id})'


