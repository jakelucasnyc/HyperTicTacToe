import pygame

class Player:

	def __init__(self, side): 
		self.side = side #equal to 1 (X) or 2 (O)
		self.left_clicked = False
		self.mouse_pos = None



	def get_mouse_pos(self):
		return pygame.mouse.get_pos()