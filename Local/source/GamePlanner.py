from Game import Game
import pygame
import sys
import numpy as np
from Player import Player
from AI import AI
from Button import Button
from Title import Title
import copy



class GamePlanner(Game):

	def __init__(self, mainGame, player1IsHuman, player2IsHuman):
		super().__init__(player1IsHuman, player2IsHuman)

		for key, value in mainGame.__dict__.items():
			self.__dict__[key] = copy.deepcopy(value)

		self.right_clicked = False
		self.mouse_pos = None

	def input(self):

		for event in pygame.event.get():

			if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
				self.right_clicked = True
				self.mouse_pos = pygame.mouse.get_pos()

				





