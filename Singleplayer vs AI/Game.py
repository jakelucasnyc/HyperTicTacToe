import pygame
import sys
import numpy as np
from Player import Player
# from AI import AI

class Game:

    #display data
    WIDTH = 1200
    HEIGHT = 800

    SIDE_X = 1
    SIDE_O = 2

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    NBOX_COLOR = RED

    #locations of the grid edges
    START_CORD = 40
    END_CORD = 760

    #locations of the little boxes
    LBOX_SIZE = 80
    LX_CORDS = list(range(START_CORD,END_CORD,LBOX_SIZE))
    LY_CORDS = list(range(START_CORD,END_CORD,LBOX_SIZE))
    LBOX_CORDS = [LX_CORDS, LY_CORDS]    

    #locations of the big boxes
    BBOX_SIZE = 3*LBOX_SIZE
    BX_CORDS = list(range(START_CORD,END_CORD,BBOX_SIZE))
    BY_CORDS = list(range(START_CORD,END_CORD,BBOX_SIZE))
    BBOX_CORDS = [BX_CORDS, BY_CORDS]

    #different line widths
    GLINE_WIDTH = 2
    BGLINE_WIDTH = 5
    LXO_LINE_WIDTH = 9
    BXO_LINE_WIDTH = 18

    #X and O formatting offsets
    X_OFFSET = 10
    O_OFFSET = 7



    def __init__(self, player1Exists=True, player2Exists=True):
        pygame.init()
        self.screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
        self.player1Exists = player1Exists
        self.player2Exists = player2Exists
        self.game_moves = 0
        self.game_record = np.zeros([9,9]) #array keeping track of the whole game grid
        self.big_grid_record = np.zeros([3,3]) #array keeping track of the big boxes that are completed
        self.small_grid_record = np.zeros([3,3]) #array representing the big box that I've clicked into and the values of each of the 9 boxes within it
        self.nsmall_grid_record = np.zeros([3,3]) #array representing the big box that I should go into next and the values of each of the 9 boxes within it

        self.next_b_cords = None




    def start(self):

        

        if (self.player1Exists):
            self.player1 = Player(Game.SIDE_X)
        else:
            self.player1 = AI(Game.SIDE_X)

        if (self.player2Exists):
            self.player2 = Player(Game.SIDE_O)
        else:
            self.player2 = AI(Game.SIDE_O)

    def draw_grid(self, box_cords, linewidth, screen):
        
        for i in range(2):
            for cord in box_cords[i][1:]: #Not drawing the first and last line so that the board doesn't look like a sudoku board
                if i == 0:
                    self.start_pos = [cord, Game.START_CORD]
                    self.end_pos = [cord, Game.END_CORD]
                elif i == 1:
                    self.start_pos = [Game.START_CORD, cord]
                    self.end_pos = [Game.END_CORD, cord]
                pygame.draw.line(screen, Game.BLACK, self.start_pos, self.end_pos, linewidth)



    def draw_shapes(self, grid_record, size, linewidth, screen):

        if self.next_b_cords is None or self.b_cords is None:
            return
        for row in range(len(grid_record[:,1])):
            row_cord = row*size+Game.START_CORD
            for col in range(len(grid_record[1,:])):
                col_cord = col*size+Game.START_CORD


                if size == Game.BBOX_SIZE and grid_record[row,col] != 0: #covering up smaller shapes if a box has been won
                    pygame.draw.rect(screen, Game.WHITE, [row_cord, col_cord, size, size])


                if grid_record[row,col] == 1:
                    pygame.draw.line(screen, Game.BLACK, [row_cord+Game.X_OFFSET, col_cord+Game.X_OFFSET], [row_cord+size-Game.X_OFFSET, col_cord+size-Game.X_OFFSET], linewidth)
                    pygame.draw.line(screen, Game.BLACK, [row_cord+Game.X_OFFSET, col_cord+size-Game.X_OFFSET], [row_cord+size-Game.X_OFFSET, col_cord+Game.X_OFFSET], linewidth)

                elif grid_record[row,col] == 2:
                    pygame.draw.ellipse(screen, Game.BLACK, [row_cord+Game.O_OFFSET, col_cord+Game.O_OFFSET, size-2*Game.O_OFFSET, size-2*Game.O_OFFSET], linewidth)



    def draw_rects(self, big_grid_record, screen, size):
        if self.next_b_cords is None or self.b_cords is None:
            return
        for row in range(len(big_grid_record[:,1])):
            row_cord = row*size+Game.START_CORD
            for col in range(len(big_grid_record[1,:])):
                col_cord = col*size+Game.START_CORD

                if (row_cord == self.b_cords[0] and col_cord == self.b_cords[1]): #covering up the previously red boxes
                        pygame.draw.rect(screen, Game.WHITE, [row_cord, col_cord, size, size])

                elif (row_cord == self.next_b_cords[0] and col_cord == self.next_b_cords[1]): #making the next box red
                    pygame.draw.rect(screen, Game.NBOX_COLOR, [row_cord, col_cord, size, size])


    def input(self, obj):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                obj.mouse_pos = obj.get_mouse_pos()
                obj.clicked = True

            else:
                obj.clicked = False

    def update_objects(self, obj):
        if obj.mouse_pos is None:
            return
        self.cords, self.cords_idx = self._find_box(obj.mouse_pos, Game.LBOX_CORDS, Game.LBOX_SIZE)
        #print("cords", self.cords)
        #print("cords_idx", self.cords_idx)
        self.b_cords, self.b_cords_idx = self._find_box(obj.mouse_pos, Game.BBOX_CORDS, Game.BBOX_SIZE)
        #print("b_cords", self.b_cords)
        #print("b_cords_idx", self.b_cords_idx)
        if ((self.game_moves == 0) or

            (obj.mouse_pos[0] >= self.next_b_cords[0] and 
            obj.mouse_pos[0] < self.next_b_cords[0]+Game.BBOX_SIZE and 
            obj.mouse_pos[1] >= self.next_b_cords[1] and 
            obj.mouse_pos[1] < self.next_b_cords[1]+Game.BBOX_SIZE and
            not np.all(self.nsmall_grid_record)) or

            np.all(self.nsmall_grid_record)):

            self.game_moves += 1
            self._update_grid_record(obj, self.game_record, self.cords_idx)
            self._isolate_little_box(self.game_record, self.cords_idx)
            self._identify_next_big_box(self.small_grid_elems, self.game_record)
            self.winning_box_side = self._grid_win_check(self.small_grid_record)
            if self.winning_box_side and self.winning_box_side == obj.side:
                self._update_grid_record(obj, self.big_grid_record, self.b_cords_idx)



    def _find_box(self, mouse_pos, box_cords, size):
        cords = []
        cords_idx = []
        for i in [0, 1]:
            for cord in reversed(box_cords[i]):
                if cord <= mouse_pos[i] and mouse_pos[i] < Game.END_CORD:
                    cords.append(cord)
                    cords_idx.append(int((cord-Game.START_CORD)/size))
                    break
        return cords, cords_idx

    def _update_grid_record(self, obj, grid_record, cords_idx):

        if grid_record[cords_idx[0], cords_idx[1]] == 0:
            grid_record[cords_idx[0], cords_idx[1]] = obj.side


    def _isolate_little_box(self, game_record, cords_idx):
        for x in [0, 3, 6]:
            if cords_idx[0] < x+3 and cords_idx[0] >= x:
                for y in [0, 3, 6]:
                    if cords_idx[1] < y+3 and cords_idx[1] >= y:
                        self.small_grid_record = self.game_record[x:x+3, y:y+3]
                        self.small_grid_elems = [cords_idx[0]-x, cords_idx[1]-y]

    
    def _identify_next_big_box(self, small_grid_elems, game_record):
        self.next_b_cords = [(small_grid_elems[0]*Game.BBOX_SIZE)+Game.START_CORD, (small_grid_elems[1]*Game.BBOX_SIZE)+Game.START_CORD]
        self.next_cords = [small_grid_elems[0]*3, small_grid_elems[1]*3]
        self.nsmall_grid_record = game_record[self.next_cords[0]:self.next_cords[0]+3, self.next_cords[1]:self.next_cords[1]+3]


    def _grid_win_check(self, grid_record):

        for winning_side in [1, 2]:

            for row_or_col in [0, 1, 2]:
                if np.all(grid_record[row_or_col, :] == winning_side):
                    return winning_side
                if np.all(grid_record[:, row_or_col] == winning_side):
                    return winning_side

            if grid_record[0,0] == winning_side and grid_record[0,0] == grid_record[1,1] and grid_record[0,0] == grid_record[2,2]:
                return winning_side
            
            if grid_record[0,2] == winning_side and grid_record[0,2] == grid_record[1,1] and grid_record[0,2] == grid_record[2,0]:
                return winning_side

        else:
            return 0


    def end(self):
        pass


if __name__ == "__main__":
    game_inst = Game()
    game_inst.screen.fill(Game.WHITE)
    while True:
        game_inst.start()
        if game_inst.game_moves % 2 == 0:
            game_inst.input(game_inst.player1)
            game_inst.update_objects(game_inst.player1)
        elif game_inst.game_moves % 2 == 1:
            game_inst.input(game_inst.player2)
            game_inst.update_objects(game_inst.player2)
        game_inst.draw_rects(game_inst.big_grid_record, game_inst.screen, Game.BBOX_SIZE)
        game_inst.draw_shapes(game_inst.game_record, Game.LBOX_SIZE, Game.LXO_LINE_WIDTH, game_inst.screen)
        game_inst.draw_shapes(game_inst.big_grid_record, Game.BBOX_SIZE, Game.BXO_LINE_WIDTH, game_inst.screen)
        game_inst.draw_grid(Game.LBOX_CORDS, Game.GLINE_WIDTH, game_inst.screen)
        game_inst.draw_grid(Game.BBOX_CORDS, Game.BGLINE_WIDTH, game_inst.screen)
        pygame.display.update()


