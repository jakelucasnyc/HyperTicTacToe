import pygame
import numpy as np
import sys
import socket
import pickle
from network import Network
from htttconstants import HTTT



# class Button:

#     def __init__(self, x, y, width, height, color, font, text, screen):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.color = color
#         self.font = font
#         self.text = text
#         self.screen = screen

#     def draw_button(self):
#         pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))
#         rendered_text = self.font.render(self.text, True, HTTT.WHITE)
#         if self.width > rendered_text.get_rect().width:
#             text_cords = [int(self.x + ((self.width-rendered_text.get_rect().width)/2)), int(self.y + ((self.height-rendered_text.get_rect().height)/1.5))] #there's a 1.5 here because the buttons look better that way
#         else:
#             raise Exception('The button rect must be wider than the text width')
#         self.screen.blit(rendered_text, text_cords)

#     def is_clicked(self, mouse_pos):
#         if mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width and mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height:
#             return True

class HTTTClient:

    pygame.init()
    HTTT = HTTT()

    def __init__(self):

        self.screen = pygame.display.set_mode((HTTT.WIDTH, HTTT.HEIGHT))       
        self.exit = False #boolean keeping track of it we exit the application or not
        self.game_moves = 0
        self.mouse_pos = pygame.mouse.get_pos() #value keeping track of the mouse position everytime the mouse is clicked

        self.n = Network()


    def game_init(self):

        self.screen = pygame.display.set_mode((HTTT.WIDTH, HTTT.HEIGHT))
        self.clock = pygame.time.Clock()
        # if self.game_started and not self.quit_to_title:
        #     pygame.display.set_caption('Game Screen')
        # else:
        pygame.display.set_caption('Title Screen')


    def title_screen_aesthetics(self):
        #making title
        self.screen.fill(HTTT.BLACK)
        self.screen.blit(HTTT.TFONT.render(HTTT.HYPER, True, HTTT.WHITE), (425, 70))
        self.screen.blit(HTTT.TFONT.render(HTTT.TTT, True, HTTT.WHITE), (270, 190))
        pygame.draw.rect(self.screen, HTTT.WHITE, (271, 312, 649, 5))

        # #start button 
        # self.start_button = Button(HTTT.START_X, HTTT.START_Y, HTTT.START_WIDTH, HTTT.START_HEIGHT, HTTT.RED, HTTT.SFONT, HTTT.START, self.screen)  
        # self.start_button.draw_button()
        # if self.start_button.is_clicked(self.mouse_pos):
        #     self.game_started = True

    def draw_grid(self, box_cords, linewidth):
        """
        Method drawing the grid of the HTTT Board
        """
        for i in range(2):
            for cord in box_cords[i][1:-1]:
                if i == 0:
                    self.start_pos = [cord, HTTT.START_CORD]
                    self.end_pos = [cord, HTTT.END_CORD]
                elif i == 1:
                    self.start_pos = [HTTT.START_CORD, cord]
                    self.end_pos = [HTTT.END_CORD, cord]
                pygame.draw.line(self.screen, HTTT.BLACK, self.start_pos, self.end_pos, linewidth)


    def if_input(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_pos = pygame.mouse.get_pos()
                    print(self.mouse_pos)
                    self.left_clicked = True
                    self.right_clicked = False
                elif event.button == 2:
                    self.mouse_pos = pygame.mouse.get_pos()
                    print(self.mouse_pos)
                    self.right_clicked = True
                    self.left_clicked = False
            else:
                self.left_clicked = False
                self.right_clicked = False


    def main(self):
        pygame.init()
        self.game_init()
        # while not self.exit:
        while True:
            self.title_screen_aesthetics()
            self.if_input()
            self.n.send('hello')
            pygame.display.update()
            # print(self.n.send(self.mouse_pos))
            # while self.game_started and not self.quit_to_title:
            #     self.game_init()
            #     self.game_screen_aesthetics()
            #     self.if_input()
            #     self.make_move()
            #     self.draw_shapes(HTTT.LBOX_SIZE, HTTT.LXO_LINE_WIDTH)
            #     self.draw_shapes(HTTT.BBOX_SIZE, HTTT.BXO_LINE_WIDTH)
            #     pygame.display.update()



if __name__ == "__main__":
    client = HTTTClient()
    client.main()