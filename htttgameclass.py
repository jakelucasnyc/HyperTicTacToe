import pygame
import numpy as np
import sys
import socket
import pickle
# from htttnetwork import HTTTNetwork

class Button:

    def __init__(self, x, y, width, height, color, font, text, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.font = font
        self.text = text
        self.screen = screen

    def draw_button(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))
        rendered_text = self.font.render(self.text, True, HTTT.WHITE)
        if self.width > rendered_text.get_rect().width:
            text_cords = [int(self.x + ((self.width-rendered_text.get_rect().width)/2)), int(self.y + ((self.height-rendered_text.get_rect().height)/1.5))] #there's a 1.5 here because the buttons look better that way
        else:
            raise Exception('The button rect must be wider than the text width')
        self.screen.blit(rendered_text, text_cords)

    def is_clicked(self, mouse_pos):
        if mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width and mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height:
            return True

class HTTT:

    pygame.init()

    #display data
    WIDTH = 1200
    HEIGHT = 800

    #title screen data
    HYPER = 'HYPER'
    TTT = 'TIC TAC TOE'
    START = 'START'
    START_X = 535
    START_Y = 400
    START_WIDTH = 140
    START_HEIGHT = 60

    #different colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    NBOX_COLOR = [255, 0, 0, 70]

    #fonts

    # C:/Users/jakel/OneDrive/Documents/Coding/Python/HyperTicTacToe/
    TFONT = pygame.font.Font('SIFONN_PRO.otf', 100)
    SFONT = pygame.font.Font('SIFONN_PRO.otf', 36)

    #locations of the grid edges
    START_CORD = 40
    END_CORD = 760

    #locations of the little boxes
    LBOX_SIZE = 80
    LX_CORDS = list(range(START_CORD,END_CORD + 1,LBOX_SIZE))
    LY_CORDS = list(range(START_CORD,END_CORD + 1,LBOX_SIZE))
    LBOX_CORDS = [LX_CORDS, LY_CORDS]

    #locations of the big boxes
    BBOX_SIZE = 3*LBOX_SIZE
    BX_CORDS = list(range(START_CORD,END_CORD + 1,BBOX_SIZE))
    BY_CORDS = list(range(START_CORD,END_CORD + 1,BBOX_SIZE))
    BBOX_CORDS = [BX_CORDS, BY_CORDS]

    #different line widths
    GLINE_WIDTH = 2
    BGLINE_WIDTH = 5
    LXO_LINE_WIDTH = 9
    BXO_LINE_WIDTH = 18

    #X and O formatting offsets
    X_OFFSET = 10
    O_OFFSET = 7



    def __init__(self):

        # self.screen = pygame.display.set_mode((HTTT.WIDTH, HTTT.HEIGHT))
        self.exit = False #boolean keeping track of it we exit the application or not
        self.game_started = False
        self.quit_to_title = False #boolean keeping track of if we quit to title or not
        self.game_moves = 0 #track of number of game moves
        self.game_record = np.zeros([9,9]) #array keeping track of the whole game
        self.big_grid_record = np.zeros([3,3]) #array keeping track of the big boxes that are completed
        self.small_grid_record = np.zeros([3,3]) #array representing the big box that I've clicked into and the values of each of the 9 boxes within it
        self.nsmall_grid_record = np.zeros([3,3]) #array representing the big box that I should go into next and the values of each of the 9 boxes within it

        #initializing useful public attributes for later use
        self.loc_elems = [None, None] 
        self.disp_loc_elems = [None, None] 
        self.nextb_cords = [None, None]
        self.next_cords = [None, None]
        self.cords = [None, None]
        self.bcords = [None, None]
        # self.nextb_cords = [(self.loc_elems[0]*HTTT.BBOX_SIZE) + HTTT.START_CORD, (self.loc_elems[1]*HTTT.BBOX_SIZE) + HTTT.START_CORD] #top left cords of the next big box to be used in the game

        self.mouse_pos = pygame.mouse.get_pos() #value keeping track of the mouse position everytime the mouse is clicked

        #private attributes for _separate_pos_neg()
        self._pos = []
        self._neg = []
        #private attributes for find_box()
        self._mouse_pos_subtracted = [[],[]]
        self._pos_neg = [[],[]]
        self._neg_val = None
        self._cords_idx = [-1, -1]
        self._cords = [-1, -1]
        

    def game_init(self):
        self.screen = pygame.display.set_mode((HTTT.WIDTH, HTTT.HEIGHT))
        self.clock = pygame.time.Clock()
        if self.game_started and not self.quit_to_title:
            pygame.display.set_caption('Game Screen')
        else:
            pygame.display.set_caption('Title Screen')

    def title_screen_aesthetics(self):
        #making title
        self.screen.fill(HTTT.BLACK)
        self.screen.blit(HTTT.TFONT.render(HTTT.HYPER, True, HTTT.WHITE), (425, 70))
        self.screen.blit(HTTT.TFONT.render(HTTT.TTT, True, HTTT.WHITE), (270, 190))
        pygame.draw.rect(self.screen, HTTT.WHITE, (271, 312, 649, 5))

        #start button 
        self.start_button = Button(HTTT.START_X, HTTT.START_Y, HTTT.START_WIDTH, HTTT.START_HEIGHT, HTTT.RED, HTTT.SFONT, HTTT.START, self.screen)  
        self.start_button.draw_button()
        if self.start_button.is_clicked(self.mouse_pos):
            self.game_started = True

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


    def game_screen_aesthetics(self):
        self.screen.fill(HTTT.WHITE)
        self.draw_grid(HTTT.LBOX_CORDS, HTTT.GLINE_WIDTH)
        self.draw_grid(HTTT.BBOX_CORDS, HTTT.BGLINE_WIDTH)
   

    def _sep_pos_neg(self, numlist):
        """
        Method separating positive and negative numbers in a list
        """
        self._pos = []
        self._neg = []
        for num in numlist:
            if num >= 0:
                self._pos.append(num)
            else:
                self._neg.append(num)
        return self._pos, self._neg

    def find_box(self, box_cords):
        """
        Method finding the top left coordinate of the box which is clicked on
        """
        self._cords_idx = [-1, -1]
        self._cords = [-1, -1]
        self._mouse_pos_subtracted = [[], []]
        
        for i in range(2):
            for cord in box_cords[i]:
                self._mouse_pos_subtracted[i].append(cord-self.mouse_pos[i])
            print(self._mouse_pos_subtracted)
            self._pos_neg = self._sep_pos_neg(self._mouse_pos_subtracted[i])
            print(self._pos_neg)
            self._neg_val = max(self._pos_neg[1])
            print(self._neg_val)
            self._cords_idx[i] = self._mouse_pos_subtracted[i].index(self._neg_val)
            print(self._cords_idx)
            self._cords[i] = box_cords[i][self._cords_idx[i]]
            print(self._cords)
            return self._cords

    def _compute_move_values(self):

        for x in [0, 3, 6]:
            if int((self.cords[0] - HTTT.START_CORD)/HTTT.LBOX_SIZE) < x+3 and int((self.cords[0] - HTTT.START_CORD)/HTTT.LBOX_SIZE) >= x:

                for y in [0, 3, 6]:
                    if int((self.cords[1] - HTTT.START_CORD)/HTTT.LBOX_SIZE) < y+3 and int((self.cords[1] - HTTT.START_CORD)/HTTT.LBOX_SIZE) >= y:

                        self.small_grid_record = self.game_record[x:x+3, y:y+3]
                        self.loc_elems[0] = int((self.cords[0] - HTTT.START_CORD)/HTTT.LBOX_SIZE)
                        self.loc_elems[1] = int((self.cords[1] - HTTT.START_CORD)/HTTT.LBOX_SIZE)
                        self.disp_loc_elems[0] = int((self.cords[0] - HTTT.START_CORD)/HTTT.LBOX_SIZE - x)
                        self.disp_loc_elems[1] = int((self.cords[1] - HTTT.START_CORD)/HTTT.LBOX_SIZE - y)
                        self.nextb_cords[0] = (self.disp_loc_elems[0]*HTTT.BBOX_SIZE) + HTTT.START_CORD
                        self.nextb_cords[1] = (self.disp_loc_elems[1]*HTTT.BBOX_SIZE) + HTTT.START_CORD
                        self.next_cords[0] = self.disp_loc_elems[0]*3
                        self.next_cords[1] = self.disp_loc_elems[1]*3

                        self.nsmall_grid_record = self.game_record[self.next_cords[0]:self.next_cords[0]+3, self.next_cords[1]:self.next_cords[1]+3]

                    else:
                        pass

            else:
                pass

    def make_move(self):
        self.cords = self.find_box(HTTT.LBOX_CORDS)
        self.bcords = self.find_box(HTTT.BBOX_CORDS)
        self._compute_move_values()
        if (self.game_moves == 0 or
        (self.mouse_pos[0] > self.nextb_cords[0] and self.mouse_pos[0] < (self.nextb_cords[0] + HTTT.BBOX_SIZE) and self.mouse_pos[1] > self.nextb_cords[1] and self.mouse_pos[1] < (self.nextb_cords[1] + HTTT.BBOX_SIZE) and (self.game_record[int((self.cords[0] - HTTT.START_CORD)/HTTT.LBOX_SIZE), int((self.cords[1] - HTTT.START_CORD)/HTTT.LBOX_SIZE)]) == 0 and not np.all(self.nsmall_grid_record)) or 
        (np.all(self.nsmall_grid_record) and self.game_record[int((self.loc_elems[0]), int(self.loc_elems[1]))] == 0)):

            if self.game_moves % 2 == 0:
                self.update_game_moves()
                self.game_record[self.loc_elems[0], self.loc_elems[1]] = 1

            elif self.game_moves % 2 == 1:
                self.update_game_moves()
                self.game_record[self.loc_elems[0], self.loc_elems[1]] = 2


    def grid_completion_check(self, grid_record):
        pass

    def draw_shapes(self, size, linewidth):
        for row in range(len(self.game_record[:,1])):
            self.row_cord = (row*size+HTTT.START_CORD)
            
            for col in range(len(self.game_record[1,:])):
                self.col_cord = (col*size+HTTT.START_CORD)
                
                if self.game_record[row, col] == 1:
                    pygame.draw.line(self.screen, HTTT.BLACK, [self.row_cord + HTTT.X_OFFSET, self.col_cord + HTTT.X_OFFSET], [self.row_cord + size - HTTT.X_OFFSET, self.col_cord + size - HTTT.X_OFFSET], linewidth)
                    pygame.draw.line(self.screen, HTTT.BLACK, [self.row_cord + size - HTTT.X_OFFSET, self.col_cord + HTTT.X_OFFSET], [self.row_cord + HTTT.X_OFFSET, self.col_cord + size - HTTT.X_OFFSET], linewidth)

                elif self.game_record[row, col] == 2:
                    pygame.draw.ellipse(self.screen, HTTT.BLACK, [self.row_cord + HTTT.O_OFFSET, self.col_cord + HTTT.O_OFFSET, size - 2*HTTT.O_OFFSET, size - 2*HTTT.O_OFFSET], linewidth)


    def update_game_moves(self):
        """
        Method updating game moves
        """
        self.game_moves += 1

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
        while not self.exit:
            self.title_screen_aesthetics()
            self.if_input()
            pygame.display.update()
            while self.game_started and not self.quit_to_title:
                self.game_init()
                self.game_screen_aesthetics()
                self.if_input()
                self.make_move()
                self.draw_shapes(HTTT.LBOX_SIZE, HTTT.LXO_LINE_WIDTH)
                self.draw_shapes(HTTT.BBOX_SIZE, HTTT.BXO_LINE_WIDTH)
                pygame.display.update()


if __name__ == '__main__':
    httt = HTTT()
    httt.main()