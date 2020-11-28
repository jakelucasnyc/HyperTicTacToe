import socket
import threading
import sys
import pickle
import numpy as np
from htttconstants import HTTT
import random
import pygame

class HTTTServer:

    pygame.init()

    SERVER_IP = '192.168.1.22'

    SERVER_PORT = 5555

    max_num_clients = 2


    def __init__(self):
        #connection variables
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.thread = None
        self.data = None
        # self.server = ip
        # self.port = port
        self.addr = None
        self.threads = []
        self.lock = threading.Lock()

        #game variables
        self.game_moves = 0
        self.game_over = False #boolean keeping track of if the game has ended
        self.winning_side = None #variable tracking who wins the game
        self.won_box = False
        self.winning_box_side = None
        self.game_record = np.zeros([9,9]) #array keeping track of the whole game
        self.big_grid_record = np.zeros([3,3]) #array keeping track of the big boxes that are completed
        self.small_grid_record = np.zeros([3,3]) #array representing the big box that I've clicked into and the values of each of the 9 boxes within it
        self.nsmall_grid_record = np.zeros([3,3]) #array representing the big box that I should go into next and the values of each of the 9 boxes within it
        self.rand = random.random() #random value
        self.first_conn_side = None #side of the first connection to the server
        self.second_conn_side = None #side of the second connection to the server

        #input variables
        self.left_clicked = False
        self.right_clicked = False
        self.mouse_pos = pygame.mouse.get_pos() #value keeping track of the mouse position everytime the mouse is clicked

        #initializing useful public attributes for later use
        self.loc_elems = [None, None] 
        self.disp_loc_elems = [None, None] 
        self.nextb_cords = [None, None]
        self.next_cords = [None, None]
        self.cords = [None, None]
        self.bcords = [None, None]

        #private attributes for _separate_pos_neg()
        self._pos = []
        self._neg = []

        #private attributes for find_box()
        self._mouse_pos_subtracted = [[],[]]
        self._pos_neg = [[],[]]
        self._neg_val = None
        self._cords_idx = [-1, -1]
        self._cords = [-1, -1]

        #communicated data
        self.game_dict = {

            'game_moves': self.game_moves, 
            'game_record': self.game_record, 
            'big_grid_record': self.big_grid_record,
            'small_grid_record': self.small_grid_record,
            'nsmall_grid_record': self.nsmall_grid_record,
            'mouse_pos': self.mouse_pos, 
            'left_clicked': self.left_clicked, 
            'right_clicked': self.right_clicked, 
            'game_over': self.game_over,
            'winning_side': self.winning_side,
            'nextb_cords': self.nextb_cords

            } #data to be sent from server to client




    #GAME CALCULATION AND DATA MANIPULATION METHODS

    def pick_side(self):
        if self.rand < 0.5:
            self.first_conn_side = int(0) #X
            self.second_conn_side = int(1) #O

        elif self.rand >= 0.5:
            self.first_conn_side = int(1) #O
            self.second_conn_side = int(0) #X


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
        return [self._pos, self._neg]



    def find_box(self, box_cords, mouse_pos):
        """
        Method finding the top left coordinate of the box that is clicked on
        """
        self._cords_idx = [-1, -1]
        self._cords = [-1, -1]
        self._mouse_pos_subtracted = [[], []]
        
        for i in [0,1]:
            for cord in box_cords[i]:

                self._mouse_pos_subtracted[i].append(cord-mouse_pos[i])
                print('mouse_pos_subtracted:', self._mouse_pos_subtracted)

            self._pos_neg = self._sep_pos_neg(self._mouse_pos_subtracted[i])
            print('_pos_neg:', self._pos_neg)

            self._neg_val = max(self._pos_neg[1])
            print('_neg_val:', self._neg_val)

            self._cords_idx[i] = self._mouse_pos_subtracted[i].index(self._neg_val)
            print('_cords_idx:', self._cords_idx)

            self._cords[i] = box_cords[i][self._cords_idx[i]]
            print('_cords:', self._cords)

        return self._cords

    def _compute_move_values(self):
        """
        Method computing a bunch of helper values to aid in calculating game mechanics
        """

        for x in [0, 3, 6]:
            if int((self.cords[0] - HTTT.START_CORD)/HTTT.LBOX_SIZE) < x+3 and int((self.cords[0] - HTTT.START_CORD)/HTTT.LBOX_SIZE) >= x:

                for y in [0, 3, 6]:
                    if int((self.cords[1] - HTTT.START_CORD)/HTTT.LBOX_SIZE) < y+3 and int((self.cords[1] - HTTT.START_CORD)/HTTT.LBOX_SIZE) >= y:

                        self.small_grid_record = self.game_record[x:x+3, y:y+3] #identifying the small 3x3 grid where the shape will be placed (used for further calculatiions)
                        self.loc_elems[0] = int((self.cords[0] - HTTT.START_CORD)/HTTT.LBOX_SIZE) #used for translating pixel size into integers for indexing the recording array x cord
                        self.loc_elems[1] = int((self.cords[1] - HTTT.START_CORD)/HTTT.LBOX_SIZE) #used for translating pixel size into integers for indexing the recording array y cord
                        self.disp_loc_elems[0] = int((self.cords[0] - HTTT.START_CORD)/HTTT.LBOX_SIZE - x) #used for translating pixel size into integers for indexing the small grid recording array x cord
                        self.disp_loc_elems[1] = int((self.cords[1] - HTTT.START_CORD)/HTTT.LBOX_SIZE - y) #used for translating pixel size into integers for indexing the small grid recording array y cord
                        self.nextb_cords[0] = (self.disp_loc_elems[0]*HTTT.BBOX_SIZE) + HTTT.START_CORD #used for identifying the next small 3x3 grid that the next move is to take place in x cord
                        self.nextb_cords[1] = (self.disp_loc_elems[1]*HTTT.BBOX_SIZE) + HTTT.START_CORD #used for identifying the next small 3x3 grid that the next move is to take place in y cord
                        self.next_cords[0] = self.disp_loc_elems[0]*3 #translates upper cords used in the small grid for the big grid
                        self.next_cords[1] = self.disp_loc_elems[1]*3 #translates upper cords used in the small grid for the big grid

                        self.nsmall_grid_record = self.game_record[self.next_cords[0]:self.next_cords[0]+3, self.next_cords[1]:self.next_cords[1]+3]

                    else:
                        pass

            else:
                pass

    def grid_completion_check(self, grid_record, winning_side=None):

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



    def update_game_data(self, data, shapenum):
        """
        Amalgamation method which puts together all procedures to calculate the updates to the game data
        """
        self.game_dict = data
        HTTT._update_vars_from_dict(self, self.game_dict)

        self.cords = self.find_box(HTTT.LBOX_CORDS, self.mouse_pos)
        self.bcords = self.find_box(HTTT.BBOX_CORDS, self.mouse_pos)

        self.loc_elems[0] = int((self.cords[0] - HTTT.START_CORD)/HTTT.LBOX_SIZE) #used for translating pixel size into integers for indexing the recording array x cord (purely for ease of use, but this must be updated after find_box())
        self.loc_elems[1] = int((self.cords[1] - HTTT.START_CORD)/HTTT.LBOX_SIZE) #used for translating pixel size into integers for indexing the recording array y cord (purely for ease of use, but this must be updated after find_box())

        if (self.game_moves == 0 or
        (self.mouse_pos[0] > self.nextb_cords[0] and self.mouse_pos[0] < (self.nextb_cords[0] + HTTT.BBOX_SIZE) and self.mouse_pos[1] > self.nextb_cords[1] and self.mouse_pos[1] < (self.nextb_cords[1] + HTTT.BBOX_SIZE) and (self.game_record[int((self.cords[0] - HTTT.START_CORD)/HTTT.LBOX_SIZE), int((self.cords[1] - HTTT.START_CORD)/HTTT.LBOX_SIZE)]) == 0 and not np.all(self.nsmall_grid_record)) or 
        (np.all(self.nsmall_grid_record) and self.game_record[int((self.loc_elems[0]), int(self.loc_elems[1]))] == 0)):

            self.game_moves += 1
            print('game_moves:', self.game_moves)
            self.game_record[self.loc_elems[0], self.loc_elems[1]] = shapenum
            print('game_record post change', self.game_record)

        self._compute_move_values()

        self.won_box, self.winning_box_side = self.grid_completion_check(self.game_record)

        if self.won_box:
            self.small_grid_record[self.small_grid_record == 0] = 3

            self.big_grid_record[int((self.bcords[0] - HTTT.START_CORD)/HTTT.BBOX_SIZE), int((self.bcords[1] - HTTT.START_CORD)/HTTT.BBOX_SIZE)] = self.winning_side #changing the big_grid_record if a small box is won


        self.game_over, self.winning_side = self.grid_completion_check(self.big_grid_record)

        if self.game_over:
            #reset for next game?
            pass

        HTTT._update_dict_from_vars(self, self.game_dict)



    #CONNECTION AND HANDLING METHODS

    def server_bind(self):
        try:
            self.s.bind((HTTTServer.SERVER_IP, HTTTServer.SERVER_PORT))

        except socket.error as e:
            print(e)


    def threaded_client(self, conn, side, connected=True):


        if side == 0:
            conn.send(pickle.dumps(self.first_conn_side))
        elif side == 1:
            conn.send(pickle.dumps(self.second_conn_side))

        print('threaded_client started')
        while connected:
            
            try:
                self.lock.acquire()
                self.data = pickle.loads(conn.recv(2048))

                try: 
                    print('game_record', self.data['game_record'])
                    print('big_grid_record', self.data['big_grid_record'])
                    print('mouse_pos', self.data['mouse_pos'])
                except:
                    pass

                if self.data == HTTT.DISCONNECT or self.data['game_over']:
                    connected = False
                    break

                if (self.first_conn_side == 0 and side == 0) or (self.second_conn_side == 0 and side == 1):
                    if self.data['game_moves'] % 2 == 0 and self.data['game_over'] == False:
                        #calculate the data from this side
                        self.update_game_data(self.data, 1) #1 = X

                    else:
                        pass

                elif (self.first_conn_side == 1 and side == 0) or (self.second_conn_side == 1 and side == 1):
                    if self.data['game_moves'] % 2 == 1 and self.data['game_over'] == False:
                        #calculate the data from this side
                        self.update_game_data(self.data, 2) #2 = O
                    else:
                        pass



                conn.sendall(pickle.dumps(self.game_dict))
                print('game data sent')
                self.lock.release()

            except socket.error as e:
                print(e)
                print('[ERROR] Error Sending Or Receiving Data')
                connected = False

            print('[LOST CONNECTION] Lost connection with Side ', side)
            conn.close()



    def start_thread(self):
        self.s.listen(HTTTServer.max_num_clients)
        print(f'[LISTENING] Server is listening on {HTTTServer.SERVER_IP}')
        while True:
            self.conn, self.addr = self.s.accept()
            print('[CONNECTED TO] ', self.addr)

            self.thread = threading.Thread(target=self.threaded_client, args=[self.conn, threading.activeCount() - 1])
            self.thread.start()
            self.threads.append(self.thread)
            print(f'\n[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')

    def main(self):
        self.server_bind()
        self.pick_side()
        self.start_thread()

if __name__ == "__main__":
    server = HTTTServer()
    server.main()