import pygame
import sys
import random
import numpy as np
import socket
import pickle


pygame.init()

#display data
WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#time data
clock = pygame.time.Clock()

#title screen data
HYPER = 'HYPER'
TTT = 'TIC TAC TOE'
START = 'START'
START_X = 535
START_Y = 400
START_WIDTH = 140
START_HEIGHT = 60

#formatting data
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
TFONT = pygame.font.Font('SIFONN_PRO.otf', 100)
SFONT = pygame.font.Font('SIFONN_PRO.otf', 36)

exit = False

#TITLE SCREEN LOOP
while not exit:

    #TITLE SCREEN INFO
    
    screen.fill(BLACK)

    #making title
    screen.blit(TFONT.render(HYPER, True, WHITE), (425, 70))
    screen.blit(TFONT.render(TTT, True, WHITE), (270, 190))
    pygame.draw.rect(screen, WHITE, (271, 312, 649, 5))

    #making start button
    pygame.draw.rect(screen, RED, (START_X, START_Y, START_WIDTH, START_HEIGHT))
    screen.blit(SFONT.render(START, True, WHITE), (550, 415))
    pygame.display.update()

    clock.tick(30)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()


        #game start
        if event.type == pygame.MOUSEBUTTONDOWN:
        #if True:
            if event.button == 1:
            #if True:
                mouse_pos = pygame.mouse.get_pos()

                #if cursor is on the start button
                if mouse_pos[0] >= START_X and mouse_pos[0] <= (START_X + START_WIDTH) and mouse_pos[1] >= START_Y and mouse_pos[1] <= (START_Y + START_HEIGHT):
                #if True:

                    #display data
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    screen.fill(WHITE)

                    #time data
                    clock = pygame.time.Clock()

                    #edge cords of the board
                    START_CORD = 40
                    END_CORD = 760

                    #locations of the little boxes
                    little_box_size = 80
                    X_CORDS = list(range(START_CORD,END_CORD + 1,little_box_size))
                    Y_CORDS = list(range(START_CORD,END_CORD + 1,little_box_size))


                    #different line widths
                    LINE_WIDTH = 2
                    BLINE_WIDTH = 5
                    X_O_LINE_WIDTH = 9

                    #locations of the big boxes
                    big_box_size = 3*little_box_size
                    BX_CORDS = list(range(START_CORD,END_CORD + 1,big_box_size))
                    BY_CORDS = list(range(START_CORD,END_CORD + 1,big_box_size))

                    #locations of the new elements within small_grid_record
                    loc_x_elem = -1 #this is a random value not between 0 and 9
                    loc_y_elem = -1 #this is a random value not between 0 and 9
                    nextbx_cord = (loc_x_elem*big_box_size) + START_CORD
                    nextby_cord = (loc_y_elem*big_box_size) + START_CORD
                    next_box_color = [255, 0, 0, 70]

                    #X and O formatting offsets
                    xy_offset = 10
                    O_offset = 7


                    game_moves = 0
                    game_record = np.zeros([9,9])
                    big_grid_record = np.zeros([3,3])
                    game_dict = {'game_record':game_record, 'big_grid_record':big_grid_record, 'game_moves':game_moves}
                    small_grid_record = np.zeros([3,3])
                    nsmall_grid_record = np.zeros([3,3])


                    disconnect_msg = '!DISCONNECT'

                    class Network:


                        def __init__(self):
                            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            self.server = '192.168.1.22'
                            self.port = 5555
                            self.addr = (self.server, self.port)
                            self.side = self.connect()

                        def getSide(self):
                            return self.side
                        
                        def connect(self):
                            try:
                                self.client.connect(self.addr)
                                # self.client.settimeout(50)
                                return pickle.loads(self.client.recv(2048))
                            except:
                                print('[ERROR] Error connecting to server or receiving information')

                        def game_info_send(self, game_dict=game_dict, game_moves=game_moves):
                            
                            try: 
                                self.client.send(pickle.dumps(game_dict))
                                return pickle.loads(self.client.recv(2048))
                            except socket.error as e:
                                print(e)

                        def disconnect(self, disconnect_msg=disconnect_msg):
                            try:
                                self.client.send(pickle.dumps(disconnect_msg))
                            except socket.error as e:
                                print(e)


                    # online data
                    #n = Network()
                    game_side = 0
                    #print(game_side)

                    def separate_plus_minus(numbers_list):
                        """
                        Function that separates positive and negative numbers within a list
                        """
                        positive = []
                        negative = []
                        for number in numbers_list:
                            if number >= 0:
                                positive.append(number)
                            else:
                                negative.append(number)
                        return positive, negative



                    def find_big_box(BX_CORDS, BY_CORDS, mouse_pos):
                        """
                        Function finding the coordinates of the top left of the big box whenever a mouse is clicked within it's bounds
                        """

                        #finding the left x cord of the big box
                        mouse_pos_sub_X = []
                        
                        for x in BX_CORDS:
                            mouse_pos_sub_X.append(x-mouse_pos[0])

                        pos_neg_X = separate_plus_minus(mouse_pos_sub_X)

                        neg_val_X = max(pos_neg_X[1])

                        idx_X = mouse_pos_sub_X.index(neg_val_X)

                        f_cord_X = BX_CORDS[idx_X]

                        #finding the top y cord of the big box
                        mouse_pos_sub_Y = []

                        for y in BY_CORDS:
                            mouse_pos_sub_Y.append(y-mouse_pos[1])

                        pos_neg_Y = separate_plus_minus(mouse_pos_sub_Y)

                        neg_val_Y = max(pos_neg_Y[1])

                        idx_Y = mouse_pos_sub_Y.index(neg_val_Y)

                        f_cord_Y = BY_CORDS[idx_Y]

                        return f_cord_X, f_cord_Y
                    


                    def find_little_box(X_CORDS, Y_CORDS, mouse_pos):
                        """
                        Function finding the coordinates of the top left of a little box whenever that blox is clicked anywhere within its bounds
                        """
                        
                        #finding the left x cord of the little box
                        mouse_pos_sub_X = []
                        
                        for x in X_CORDS:
                            mouse_pos_sub_X.append(x-mouse_pos[0])

                        pos_neg_X = separate_plus_minus(mouse_pos_sub_X)

                        neg_val_X = max(pos_neg_X[1])

                        idx_X = mouse_pos_sub_X.index(neg_val_X)

                        f_cord_X = X_CORDS[idx_X]

                        #finding the top y cord of the little box
                        mouse_pos_sub_Y = []

                        for y in Y_CORDS:
                            mouse_pos_sub_Y.append(y-mouse_pos[1])

                        pos_neg_Y = separate_plus_minus(mouse_pos_sub_Y)

                        neg_val_Y = max(pos_neg_Y[1])

                        idx_Y = mouse_pos_sub_Y.index(neg_val_Y)

                        f_cord_Y = Y_CORDS[idx_Y]

                        return f_cord_X, f_cord_Y, idx_X, idx_Y

                    def update_game_moves():
                        """
                        Function updating the number of game moves played
                        """

                        global game_moves

                        game_moves = game_moves + 1


                    winning_side = 0
                    won = False


                    def grid_completion_check(grid_record):
                        """
                        Function checking if a small grid has been one by one side or the other
                        """

                        global winning_side
                        

                        for ws in [1, 2]:

                            for r_o_c in range(3):


                                if np.all(grid_record[r_o_c] == ws):
                                    winning_side = ws
                                    return True, winning_side

                                if np.all(grid_record[:,r_o_c] == ws):
                                    winning_side = ws
                                    return True, winning_side

                            if grid_record[0,0] == ws and grid_record[0,0] == grid_record[1,1] and grid_record[0,0] == grid_record[2,2]:
                                winning_side = ws
                                return True, winning_side
                            
                            if grid_record[0,2] == ws and grid_record[0,2] == grid_record[1,1] and grid_record[0,2] == grid_record[2,0]:
                                winning_side = ws
                                return True, winning_side
                        
                        else:
                            return False, winning_side    



                    def small_grid_record_corresponding_value_updates(x_displacement, y_displacement):
                        """
                        Function preventing copypasta and setting necessary values alongside the small_grid_record
                        """


                        #setting the location within small_grid_record of the newest update to the small grid
                        loc_x_elem = int((x_cord - START_CORD)/little_box_size - x_displacement)
                        loc_y_elem = int((y_cord - START_CORD)/little_box_size - y_displacement)

                        #setting the cords of the next big box to be used in the next turn
                        nextbx_cord = (loc_x_elem*big_box_size) + START_CORD
                        nextby_cord = (loc_y_elem*big_box_size) + START_CORD

                        #setting the top left cords for the small grid for the nsmall_grid_record
                        nextx_cord = loc_x_elem*3
                        nexty_cord = loc_y_elem*3

                        # print(small_grid_record)
                        # print(loc_x_elem, loc_y_elem)

                        return loc_x_elem, loc_y_elem, nextbx_cord, nextby_cord, nextx_cord, nexty_cord


                    def redraw(game_record, size, x_offset=xy_offset, o_offset=O_offset, START_CORD=START_CORD, linewidth=X_O_LINE_WIDTH, lwmult=1):
                        """
                        Function redrawing each of the symbols on the screen after every new rect drawing
                        """
                        for row in range(len(game_record[:,1])):
                            row_cord = (row*size+START_CORD)
                            for col in range(len(game_record[1,:])):
                                col_cord = (col*size+START_CORD)

                                if size == big_box_size and (row_cord != nextbx_cord or col_cord != nextby_cord) and (game_record[row, col] == 1 or game_record[row, col] == 2):
                                    pygame.draw.rect(screen, WHITE, [row_cord, col_cord, size, size])

                                elif size == big_box_size and (row_cord == nextbx_cord and col_cord == nextby_cord) and (game_record[row, col] == 1 or game_record[row, col] == 2):
                                    pygame.draw.rect(screen, next_box_color, [row_cord, col_cord, size, size])

                                else:
                                    pass

                                if game_record[row, col] == 1:
                                    pygame.draw.line(screen, BLACK, [row_cord + x_offset, col_cord + x_offset], [row_cord + size - x_offset, col_cord + size - x_offset], linewidth*lwmult)
                                    pygame.draw.line(screen, BLACK, [row_cord + size - x_offset, col_cord + x_offset], [row_cord + x_offset, col_cord + size - x_offset], linewidth*lwmult)

                                elif game_record[row, col] == 2:
                                    pygame.draw.ellipse(screen, BLACK, [row_cord + o_offset, col_cord + o_offset, size - 2*o_offset, size - 2*o_offset], linewidth*lwmult)

                                else:
                                    pass






                    quit_to_title = False

                    #GAME LOOP
                    while not quit_to_title:

                        clock.tick(30)

                        #filling in the lines for the board while keeping the outer edges out
                        for x in X_CORDS[1:-1]:
                            start_pos = [x, START_CORD]
                            end_pos = [x, END_CORD]
                            pygame.draw.line(screen, BLACK, start_pos, end_pos, LINE_WIDTH)

                        for y in Y_CORDS[1:-1]:
                            start_pos = [START_CORD, y]
                            end_pos = [END_CORD, y]
                            pygame.draw.line(screen, BLACK, start_pos, end_pos, LINE_WIDTH)

                        for x in BX_CORDS[1:-1]:
                            start_pos = [x, START_CORD]
                            end_pos = [x, END_CORD]
                            pygame.draw.line(screen, BLACK, start_pos, end_pos, BLINE_WIDTH)

                        for y in BY_CORDS[1:-1]:
                            start_pos = [START_CORD, y]
                            end_pos = [END_CORD, y]
                            pygame.draw.line(screen, BLACK, start_pos, end_pos, BLINE_WIDTH)

                        
                        pygame.display.update()


                        #formatting necessary data to send to server in a dictionary
                        # game_dict = {'game_record':ndarray_to_list(game_record), 'big_grid_record':ndarray_to_list(big_grid_record)}


                        # while True:
                        #sending data and receiving the same data (the other instance of the client will only receive)
                        #s_game_dict = n.game_info_send()

                        #using the server's response to define new data values for redrawing
                        #game_record = s_game_dict['game_record']
                        #big_grid_record = s_game_dict['big_grid_record']
                        #game_moves = s_game_dict['game_moves']
                    

                        
                    
                        #GAME EVENTS
                        for game_event in pygame.event.get():

                            if game_event.type == pygame.QUIT:
                                #n.disconnect()
                                quit_to_title = True

                            if game_event.type == pygame.MOUSEBUTTONDOWN:
                                if game_event.button == 1:
                                    mouse_pos = pygame.mouse.get_pos()

                                    x_cord, y_cord, x_cord_idx, y_cord_idx = find_little_box(X_CORDS[:-1], Y_CORDS[:-1], mouse_pos)

                                    bx_cord, by_cord = find_big_box(BX_CORDS[:-1], BY_CORDS[:-1], mouse_pos)

                                    print(nextbx_cord, nextby_cord)

                                    if ((game_moves == 0 and game_side == 0) or 
                                    (game_moves % 2 == game_side) and
                                    (mouse_pos[0] > nextbx_cord and mouse_pos[0] < (nextbx_cord + big_box_size) and mouse_pos[1] > nextby_cord and mouse_pos[1] < (nextby_cord + big_box_size) and (game_record[int((x_cord - START_CORD)/little_box_size), int((y_cord - START_CORD)/little_box_size)]) == 0 and not np.all(nsmall_grid_record)) or 
                                    (np.all(nsmall_grid_record) and game_record[int((x_cord - START_CORD)/little_box_size), int((y_cord - START_CORD)/little_box_size)] == 0)):

                                        if mouse_pos[0] > x_cord and mouse_pos[0] < (x_cord + little_box_size) and mouse_pos[1] > y_cord and mouse_pos[1] < (y_cord + little_box_size):
                                            #print(x_cord, y_cord)

                        
                                            
                                            #creating the "X" when an open box is clicked
                                            if game_moves % 2 == 0 and game_record[int((x_cord - START_CORD)/little_box_size), int((y_cord - START_CORD)/little_box_size)] == 0:

                                                update_game_moves()
                                                print(game_moves)

                                                #applying the location to game_record
                                                game_record[int((x_cord - START_CORD)/little_box_size), int((y_cord - START_CORD)/little_box_size)] = 1

                                            #creating the "O" when an open box is clicked
                                            elif game_moves % 2 == 1 and game_record[int((x_cord - START_CORD)/little_box_size), int((y_cord - START_CORD)/little_box_size)] == 0:

                                                update_game_moves()
                                                print(game_moves)
                                                #applying the location to game_record
                                                game_record[int((x_cord - START_CORD)/little_box_size), int((y_cord - START_CORD)/little_box_size)] = 2


                                            #isolating the small grid
                                            for x in [0, 3, 6]:
                                                if int((x_cord - START_CORD)/little_box_size) < x+3 and int((x_cord - START_CORD)/little_box_size) >= x:

                                                    for y in [0, 3, 6]:
                                                        if int((y_cord - START_CORD)/little_box_size) < y+3 and int((y_cord - START_CORD)/little_box_size) >= y:

                                                            small_grid_record = game_record[x:x+3, y:y+3]
                                                            loc_x_elem, loc_y_elem, nextbx_cord, nextby_cord, nextx_cord, nexty_cord = small_grid_record_corresponding_value_updates(x, y)

                                                            nsmall_grid_record = game_record[nextx_cord:nextx_cord+3, nexty_cord:nexty_cord+3]

                                                        else:
                                                            pass

                                                else:
                                                    pass


                                            #checking to see if the a small grid has been completed
                                            won, winning_side = grid_completion_check(small_grid_record)

                                            #what happens if the small grid is won by X
                                            if won == True and winning_side == 1:
                                                #stopping any other open squares in the now filled big box to be pressed (3 can be anything other than 0)
                                                small_grid_record[small_grid_record == 0] = 3
                                                #adding the record of a big box filled to the big_grid_record
                                                big_grid_record[int((bx_cord - START_CORD)/big_box_size), int((by_cord - START_CORD)/big_box_size)] = 1

                                            #what happends if the small grid is won by O
                                            elif won == True and winning_side == 2:
                                                #stopping any other open squares in the now filled big box to be pressed (3 can be anything other than 0)
                                                small_grid_record[small_grid_record == 0] = 3
                                                #adding the record of a big box filled to the big_grid_record
                                                big_grid_record[int((bx_cord - START_CORD)/big_box_size), int((by_cord - START_CORD)/big_box_size)] = 2


                                            # changing the previous red box back to white
                                            pygame.draw.rect(screen, WHITE, [bx_cord, by_cord, big_box_size, big_box_size])
                                            # outlining the box that needs to be played in
                                            pygame.draw.rect(screen, next_box_color, [nextbx_cord, nextby_cord, big_box_size, big_box_size])

                                            # redrawing in all of the signs that are present on the board
                                            redraw(game_record, little_box_size)
                                            redraw(big_grid_record, big_box_size, lwmult=2)


                                            #checking to see if the big grid has been completed
                                            won, winning_side = grid_completion_check(big_grid_record)

                                            #what happens if the game is won by X
                                            if won == True and winning_side == 1:

                                                pygame.draw.rect(screen, WHITE, [START_CORD, START_CORD, END_CORD-START_CORD, END_CORD-START_CORD])
                                                pygame.draw.line(screen, BLACK, [START_CORD + xy_offset, START_CORD + xy_offset], [END_CORD - xy_offset, END_CORD - xy_offset], X_O_LINE_WIDTH*4)
                                                pygame.draw.line(screen, BLACK, [END_CORD - xy_offset, START_CORD + xy_offset], [START_CORD + xy_offset, END_CORD - xy_offset], X_O_LINE_WIDTH*4)

                                            #what happens if the game is won by O
                                            elif won == True and winning_side == 2:

                                                pygame.draw.rect(screen, WHITE, [START_CORD, START_CORD, END_CORD-START_CORD, END_CORD-START_CORD])
                                                pygame.draw.ellipse(screen, BLACK, [START_CORD + O_offset, START_CORD + O_offset, START_CORD-END_CORD - 2*O_offset, START_CORD-END_CORD - 2*O_offset], X_O_LINE_WIDTH*4)

