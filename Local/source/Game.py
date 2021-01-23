import pygame
import sys
import numpy as np
from Player import Player
from AI import AI
from Button import Button
# from AI import AI

class Game:
    pygame.init()

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
    SADDLEBROWN = (139, 69, 19)
    GRAY = (110, 110, 110)
    MELLOW_YELLOW = (248, 222, 126)
    NBOX_COLOR = RED
    CGRATS_COLOR = BLUE
    CGRATS_FONT = pygame.font.Font('../resources/SIFONN_PRO.otf', 90)
    BUTTON_FONT = pygame.font.Font('../resources/SIFONN_PRO.otf', 36)

    #board stats
    START_CORD = 40
    END_CORD = 760
    BOARD_SIZE = END_CORD-START_CORD
    BOARD_CENTER = (BOARD_SIZE/2)+40

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
    END_XO_LINE_WIDTH = 27

    #X and O formatting offsets
    X_OFFSET = 10
    O_OFFSET = 7

    #end aesthetics variables
    CGRATS_CENTER_DISP = [200, 100] #[x disp rom center, y disp from center]



    def __init__(self, player1IsHuman, player2IsHuman):
        self.screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
        self.clock = pygame.time.Clock()
        self.clock.tick(60)
        self.player1IsHuman = player1IsHuman
        self.player2IsHuman = player2IsHuman
        self.game_moves = 0
        self.game_over = False
        self.game_drawn = False
        self.game_record = np.zeros([9,9]) #array keeping track of the whole game grid
        self.big_grid_record = np.zeros([3,3]) #array keeping track of the big boxes that are completed
        self.small_grid_record = np.zeros([3,3]) #array representing the big box that I've clicked into and the values of each of the 9 boxes within it
        self.nsmall_grid_record = np.zeros([3,3]) #array representing the big box that I should go into next and the values of each of the 9 boxes within it

        self.next_b_cords = []
        self.next_box_list = []
        self.cords = []
        self.b_cords = []

        #icon color
        self.X_color = Game.GRAY
        self.O_color = Game.GRAY
        

        #post game
        self.post_game_mouse_pos = None
        self.post_game_clicked = False




    def init(self):

        if (self.player1IsHuman):
            self.player1 = Player(Game.SIDE_X)
        else:
            self.player1 = AI(Game.SIDE_X)

        if (self.player2IsHuman):
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

        if not self.next_b_cords or not self.b_cords:
            return
        for row in range(len(grid_record[:,1])):
            row_cord = row*size+Game.START_CORD
            for col in range(len(grid_record[1,:])):
                col_cord = col*size+Game.START_CORD


                if size == Game.BBOX_SIZE and grid_record[row,col] != 0 and (row_cord != self.next_b_cords[0] or col_cord != self.next_b_cords[1]): #covering up smaller shapes if a box has been won
                    pygame.draw.rect(screen, Game.WHITE, [row_cord, col_cord, size, size])

                elif size == Game.BBOX_SIZE and grid_record[row,col] != 0 and (row_cord == self.next_b_cords[0] and col_cord == self.next_b_cords[1]):
                    pygame.draw.rect(screen, Game.NBOX_COLOR, [row_cord, col_cord, size, size])


                if grid_record[row,col] == 1:
                    pygame.draw.line(screen, Game.BLACK, [row_cord+Game.X_OFFSET, col_cord+Game.X_OFFSET], [row_cord+size-Game.X_OFFSET, col_cord+size-Game.X_OFFSET], linewidth)
                    pygame.draw.line(screen, Game.BLACK, [row_cord+Game.X_OFFSET, col_cord+size-Game.X_OFFSET], [row_cord+size-Game.X_OFFSET, col_cord+Game.X_OFFSET], linewidth)

                elif grid_record[row,col] == 2:
                    pygame.draw.ellipse(screen, Game.BLACK, [row_cord+Game.O_OFFSET, col_cord+Game.O_OFFSET, size-2*Game.O_OFFSET, size-2*Game.O_OFFSET], linewidth)



    def draw_rects(self, big_grid_record, screen, size):
        if not self.next_b_cords or not self.b_cords:
            return
        for row in range(len(big_grid_record[:,1])):
            row_cord = row*size+Game.START_CORD
            for col in range(len(big_grid_record[1,:])):
                col_cord = col*size+Game.START_CORD

                if (row_cord == self.b_cords[0] and col_cord == self.b_cords[1]): #covering up the previously red boxes
                        pygame.draw.rect(screen, Game.WHITE, [row_cord, col_cord, size, size])

                if (row_cord == self.next_b_cords[0] and col_cord == self.next_b_cords[1]): #making the next box red
                    pygame.draw.rect(screen, Game.NBOX_COLOR, [row_cord, col_cord, size, size])

    def game_info_display(self):
        self.game_moves_display = Button(820, 40, 320, 80, Game.BLACK, Game.BUTTON_FONT, f"Game Moves: {self.game_moves}", self.screen)
        self.game_moves_display.draw_button()

        # self.resign_button = Button(820, 160, 320, 80, Game.GRAY, Game.BUTTON_FONT, "Resign", self.screen)
        # self.resign_button.draw_button()

        

        if self.game_moves % 2 == 0 and not self.game_over:
            self.X_color = Game.MELLOW_YELLOW
            self.O_color = Game.GRAY

        elif self.game_moves % 2 == 1 and not self.game_over:
            self.O_color = Game.MELLOW_YELLOW
            self.X_color = Game.GRAY

        else:
            self.X_color = Game.GRAY
            self.O_color = Game.GRAY

        self.X_icon = Button(860, 160, 80, 80, self.X_color, Game.BUTTON_FONT, "X", self.screen)
        self.X_icon.draw_button()

        self.O_icon = Button(1020, 160, 80, 80, self.O_color, Game.BUTTON_FONT, "O", self.screen)
        self.O_icon.draw_button()

        pygame.display.update()


    def inform_and_input(self, obj):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and isinstance(obj, Player):
                obj.mouse_pos = obj.get_mouse_pos()
                obj.clicked = True

            else:
                obj.clicked = False

        if isinstance(obj, AI): #sending the AI game info relevant to its moving
            obj.get_game_moves(self.game_moves)
            obj.get_info(self.game_over, self.next_b_cords, self.game_record)
            if obj.AI_turn: #if it's the AI's turn
                obj.mouse_pos = obj.get_mouse_pos()
                obj.clicked = True
            else:
                obj.clicked = False

    def update_objects(self, obj):
        if obj.mouse_pos is None:
            self.inform_and_input(obj) #take more input because no input was previously supplied
            return 
        self.cords, self.cords_idx = self._find_box(obj.mouse_pos, Game.LBOX_CORDS, Game.LBOX_SIZE)
        #print("cords", self.cords)
        #print("cords_idx", self.cords_idx)
        self.b_cords, self.b_cords_idx = self._find_box(obj.mouse_pos, Game.BBOX_CORDS, Game.BBOX_SIZE)
        #print("b_cords", self.b_cords)
        #print("b_cords_idx", self.b_cords_idx)
        if (not self.cords or not self.b_cords):
            self.inform_and_input(obj) #take more input because an invalid input was previously supplied
            return

        if ((self.game_moves == 0) or

            (obj.mouse_pos[0] >= self.next_b_cords[0] and 
            obj.mouse_pos[0] < self.next_b_cords[0]+Game.BBOX_SIZE and 
            obj.mouse_pos[1] >= self.next_b_cords[1] and 
            obj.mouse_pos[1] < self.next_b_cords[1]+Game.BBOX_SIZE and
            not np.all(self.nsmall_grid_record) and 
            self.game_record[self.cords_idx[0], self.cords_idx[1]] == 0)):

            self.game_moves += 1
            self._update_grid_record(obj, self.game_record, self.cords_idx)
            self._isolate_little_box(self.game_record, self.cords_idx)

            if self.big_grid_record[self.b_cords_idx[0], self.b_cords_idx[1]] == 0:
                self.winning_box_side = self._grid_win_check(self.small_grid_record)

            if self.winning_box_side and (self.winning_box_side == obj.side or self.winning_box_side == 3):
                self._update_grid_record(obj, self.big_grid_record, self.b_cords_idx)
                self.small_grid_record[self.small_grid_record == 0] = 3
                print(self.small_grid_record)
                print(self.game_record)

            self._identify_next_big_box(self.small_grid_elems, self.game_record)#big grid must be updated before this method can be called

            self.winning_game_side = self._grid_win_check(self.big_grid_record)
            if self.winning_game_side:
                self.game_over = True

            if np.all(self.game_record):
                self.game_over = True
                self.game_drawn = True





    def _find_box(self, mouse_pos, box_cords, size):
        cords = []
        cords_idx = []
        for i in [0, 1]:
            for cord in reversed(box_cords[i]):
                if cord <= mouse_pos[i] and mouse_pos[i] < Game.END_CORD:
                    cords.append(cord)
                    cords_idx.append(int((cord-Game.START_CORD)/size))
                    break
        if len(cords) != 2:
            cords = []
            cords_idx = []
        return cords, cords_idx

    def _update_grid_record(self, obj, grid_record, cords_idx):

        grid_record[cords_idx[0], cords_idx[1]] = obj.side


    def _isolate_little_box(self, game_record, cords_idx):
        for x in [0, 3, 6]:
            if cords_idx[0] < x+3 and cords_idx[0] >= x:
                for y in [0, 3, 6]:
                    if cords_idx[1] < y+3 and cords_idx[1] >= y:
                        self.small_grid_record = self.game_record[x:x+3, y:y+3]
                        self.small_grid_elems = [cords_idx[0]-x, cords_idx[1]-y]

    
    def _identify_next_big_box(self, small_grid_elems, game_record):
        

        if self.big_grid_record[self.small_grid_elems[0], self.small_grid_elems[1]] == 0: #if the proposed next big box has room for other shapes...

            self.next_cords = [small_grid_elems[0]*3, small_grid_elems[1]*3]
            self.next_box_list.append(self.next_cords)
            self.next_b_cords = [(small_grid_elems[0]*Game.BBOX_SIZE)+Game.START_CORD, (small_grid_elems[1]*Game.BBOX_SIZE)+Game.START_CORD]
            print(self.next_box_list)
        else:
            print("entered else clause of _identify_next_big_box")
            for prev_next_cords in reversed(self.next_box_list[:-1]):
                if self.big_grid_record[int(prev_next_cords[0]/3), int(prev_next_cords[1]/3)] == 0:
                    self.next_cords = prev_next_cords
                    self.next_b_cords = [(int(prev_next_cords[0]/3*Game.BBOX_SIZE)+Game.START_CORD), (int(prev_next_cords[1]/3*Game.BBOX_SIZE)+Game.START_CORD)] #setting the next box cords to the location of the newly proposed next box
                    print(self.next_cords)
                    break
            else:
                if not np.all(self.game_record):
                    raise Exception("No empty big box for the next shape to go into")


        self.nsmall_grid_record = game_record[self.next_cords[0]:self.next_cords[0]+3, self.next_cords[1]:self.next_cords[1]+3]
        print("nsmall_grid_record ", self.nsmall_grid_record)


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

        
            elif np.all(grid_record):
                return 3 #drawn

        else:
            return 0


    def end(self, winning_game_side):
        pygame.draw.rect(self.screen, Game.WHITE, [Game.START_CORD, Game.START_CORD, Game.BOARD_SIZE, Game.BOARD_SIZE])
        if self.winning_game_side == 1:
            pygame.draw.line(self.screen, Game.BLACK, [Game.START_CORD+Game.X_OFFSET, Game.START_CORD+Game.X_OFFSET], [Game.END_CORD-Game.X_OFFSET, Game.END_CORD-Game.X_OFFSET], Game.END_XO_LINE_WIDTH) #drawing big X
            pygame.draw.line(self.screen, Game.BLACK, [Game.START_CORD+Game.X_OFFSET, Game.END_CORD-Game.X_OFFSET], [Game.END_CORD-Game.X_OFFSET, Game.START_CORD+Game.X_OFFSET], Game.END_XO_LINE_WIDTH)
        elif self.winning_game_side == 2:
            pygame.draw.ellipse(self.screen, Game.BLACK, [Game.START_CORD+Game.O_OFFSET, Game.START_CORD+Game.O_OFFSET, Game.BOARD_SIZE-2*Game.O_OFFSET, Game.BOARD_SIZE-2*Game.O_OFFSET], Game.END_XO_LINE_WIDTH) #drawing big O
        elif self.game_drawn:
            pygame.draw.line(self.screen, Game.BLACK, [Game.START_CORD+Game.X_OFFSET, Game.START_CORD+Game.X_OFFSET], [Game.END_CORD-Game.X_OFFSET, Game.END_CORD-Game.X_OFFSET], Game.END_XO_LINE_WIDTH) #drawing big X
            pygame.draw.line(self.screen, Game.BLACK, [Game.START_CORD+Game.X_OFFSET, Game.END_CORD-Game.X_OFFSET], [Game.END_CORD-Game.X_OFFSET, Game.START_CORD+Game.X_OFFSET], Game.END_XO_LINE_WIDTH)
            pygame.draw.ellipse(self.screen, Game.BLACK, [Game.START_CORD+Game.O_OFFSET, Game.START_CORD+Game.O_OFFSET, Game.BOARD_SIZE-2*Game.O_OFFSET, Game.BOARD_SIZE-2*Game.O_OFFSET], Game.END_XO_LINE_WIDTH)

    def end_aesthetics(self, winning_game_side, game_drawn):
        if winning_game_side == 1:
            congrats = Button(Game.BOARD_CENTER-Game.CGRATS_CENTER_DISP[0], Game.BOARD_CENTER-Game.CGRATS_CENTER_DISP[1], Game.CGRATS_CENTER_DISP[0]*2, Game.CGRATS_CENTER_DISP[1]*2, Game.CGRATS_COLOR, Game.CGRATS_FONT, "X WINS!", self.screen)
            congrats.draw_button()
        elif winning_game_side == 2:
            congrats = Button(Game.BOARD_CENTER-Game.CGRATS_CENTER_DISP[0], Game.BOARD_CENTER-Game.CGRATS_CENTER_DISP[1], Game.CGRATS_CENTER_DISP[0]*2, Game.CGRATS_CENTER_DISP[1]*2, Game.CGRATS_COLOR, Game.CGRATS_FONT, "O WINS!", self.screen)
            congrats.draw_button()
        elif game_drawn:
            congrats = Button(Game.BOARD_CENTER-Game.CGRATS_CENTER_DISP[0], Game.BOARD_CENTER-Game.CGRATS_CENTER_DISP[1], Game.CGRATS_CENTER_DISP[0]*2, Game.CGRATS_CENTER_DISP[1]*2, Game.CGRATS_COLOR, Game.CGRATS_FONT, "DRAW!", self.screen)
            congrats.draw_button()

        self.replay_button = Button(Game.BOARD_CENTER-120, Game.BOARD_CENTER+120, 240, 80, Game.GREEN, Game.BUTTON_FONT, "Replay", self.screen)
        self.replay_button.draw_button()

        pygame.display.update()

    def post_game_input(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.post_game_mouse_pos = pygame.mouse.get_pos()
                self.post_game_clicked = True
            else:
                self.post_game_clicked = False

    def post_game_steps(self, main):
        if self.post_game_mouse_pos is None:
            return

        if self.replay_button.is_clicked(self.post_game_mouse_pos) and self.post_game_clicked:
            # print("Replay Clicked")
            main()


def main():
    game_inst = Game(True, True)
    game_inst.screen.fill(Game.WHITE)
    game_inst.draw_grid(Game.LBOX_CORDS, Game.GLINE_WIDTH, game_inst.screen)
    game_inst.draw_grid(Game.BBOX_CORDS, Game.BGLINE_WIDTH, game_inst.screen)
    pygame.display.update()
    while True:
        game_inst.init()
        if game_inst.game_moves % 2 == 0:
            game_inst.inform_and_input(game_inst.player1)
            game_inst.update_objects(game_inst.player1)
        elif game_inst.game_moves % 2 == 1:
            game_inst.inform_and_input(game_inst.player2)
            game_inst.update_objects(game_inst.player2)
        game_inst.game_info_display()
        if not game_inst.cords or not game_inst.b_cords:
            continue
        game_inst.draw_rects(game_inst.big_grid_record, game_inst.screen, Game.BBOX_SIZE)
        game_inst.draw_shapes(game_inst.game_record, Game.LBOX_SIZE, Game.LXO_LINE_WIDTH, game_inst.screen)
        game_inst.draw_shapes(game_inst.big_grid_record, Game.BBOX_SIZE, Game.BXO_LINE_WIDTH, game_inst.screen)
        if game_inst.game_over:
            game_inst.end(game_inst.winning_game_side)
        game_inst.draw_grid(Game.LBOX_CORDS, Game.GLINE_WIDTH, game_inst.screen)
        game_inst.draw_grid(Game.BBOX_CORDS, Game.BGLINE_WIDTH, game_inst.screen)
        while (game_inst.game_over):
        # while True:
            game_inst.end_aesthetics(game_inst.winning_game_side, game_inst.game_drawn)
            game_inst.post_game_input()
            game_inst.post_game_steps(main)

        pygame.display.update()

if __name__ == "__main__":
    main()



