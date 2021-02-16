import pygame
from Button import Button
import sys
import random

class Title:

    pygame.init()

    #display data
    WIDTH = 1200
    HEIGHT = 800
    CENTER_X = WIDTH//2
    CENTER_Y = HEIGHT//2

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    SADDLEBROWN = (139, 69, 19)
    GRAY = (110, 110, 110)
    MELLOW_YELLOW = (248, 222, 126)

    TITLE_FONT = pygame.font.Font('../resources/SIFONN_PRO.otf', 100)
    BUTTON_FONT = pygame.font.Font('../resources/SIFONN_PRO.otf', 36)

    def __init__(self):
        self.screen = pygame.display.set_mode((Title.WIDTH, Title.HEIGHT))
        self.clock = pygame.time.Clock()
        # self.clock.tick(60)
        self.mouse_pos = (0, 0)
        self.clicked = False
        self.game_started = False


    def input(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos = pygame.mouse.get_pos()
                self.clicked = True

            else:
                self.clicked = False

    def title_aesthetics(self):

        self.screen.fill(Title.BLACK)
        self.screen.blit(Title.TITLE_FONT.render("HYPER", True, Title.WHITE), (425, 70))
        self.screen.blit(Title.TITLE_FONT.render("TIC-TAC-TOE", True, Title.WHITE), (270, 190))
        pygame.draw.rect(self.screen, Title.WHITE, (271, 312, 649, 5))

        self.two_player = Button(Title.CENTER_X-160, 420, 320, 80, Title.GREEN, Title.BUTTON_FONT, "Two-Player", self.screen)
        self.two_player.draw_button()

        self.player_vs_AI = Button(Title.CENTER_X-160, 540, 320, 80, Title.BLUE, Title.BUTTON_FONT, "Player vs AI", self.screen)
        self.player_vs_AI.draw_button()

        pygame.display.update()

    def button_logic(self): #return flags for the Game class instance

        if self.two_player.is_clicked(self.mouse_pos) and self.clicked:
            self.game_started = True
            return (True, True)

        elif self.player_vs_AI.is_clicked(self.mouse_pos) and self.clicked:
            rand = random.randint(1, 100)
            if rand <= 50:
                self.game_started = True
                return (True, False)

            else:
                self.game_started = True
                return (False, True)

        else:
            self.game_started = False
            return None





