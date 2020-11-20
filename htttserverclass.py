import socket
import threading
import sys
import pickle
import numpy as np
from htttconstants import HTTT

class HTTTServer:

    server = '192.168.1.22'

    port = 5555

    max_num_clients = 2


    def __init__(self):
        #connection variables
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.addr = None
        self.thread = None
        self.data = None

        #game variables
        self.game_moves = 0
        self.game_record = np.zeros([9,9]) #array keeping track of the whole game
        self.big_grid_record = np.zeros([3,3]) #array keeping track of the big boxes that are completed
        self.game_dict = {'game_moves': self.game_moves, 'game_record': self.game_record, 'big_grid_record': self.big_grid_record} #data to be sent from client to server
        self.small_grid_record = np.zeros([3,3]) #array representing the big box that I've clicked into and the values of each of the 9 boxes within it
        self.nsmall_grid_record = np.zeros([3,3]) #array representing the big box that I should go into next and the values of each of the 9 boxes within it
        self.rand = random.random() #random value
        self.first_conn_side = None #side of the first connection to the server
        self.second_conn_side = None #side of the second connection to the server



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
    """
    Method computing a bunch of helper values to aid in calculating game mechanics
    """

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



    #CONNECTION AND HANDLING METHODS

    def bind(self):
        try:
            self.s.bind((HTTTServer.server, HTTTServer.port))

        except socket.error as e:
            print(str(e))


    def threaded_client(self, conn, side, connected=True):

        if side == 0:
            conn.send(pickle.dumps(self.first_conn_side))
        if side == 1:
            conn.send(pickle.dumps(self.second_conn_side))

        print('threaded_client started')
        while connected:
            try:
                self.data = pickle.loads(conn.recv(2048))
                print('data received:', self.data)
                # game_record = data['game_record']
                # print(game_record)
                # big_grid_record = data['big_grid_record']
                # print(big_grid_record)

                # if data == disconnect_msg:
                #     connected = False

                # elif (data['game_record'] == game_dict['game_record']).all() == True and (data['big_grid_record'] == game_dict['big_grid_record']).all() == True:
                #     game_dict = data
                
                # elif data['game_record'].shape == game_dict['game_record'].shape and data['big_grid_record'].shape == game_dict['big_grid_record'].shape:
                #     game_dict = data
                #     update_game_moves()
                #     game_dict['game_moves'] = game_moves


                conn.send(pickle.dumps('hello world'))
                print('game data sent')

            except socket.error as e:
                print(e)
                print('[ERROR] Error Sending Or Receiving Data')
                connected = False

        print('[LOST CONNECTION] Lost connection with Side ', side)
        conn.close()



    def start_thread(self):
        self.s.listen(HTTTServer.max_num_clients)
        print(f'[LISTENING] Server is listening on {HTTTServer.server}')
        while True:
            self.conn, self.addr = self.s.accept()
            print('[CONNECTED TO] ', self.addr)

            self.thread = threading.Thread(target=self.threaded_client, args=[self.conn, threading.activeCount() - 1])
            self.thread.start()
            # current_side += 1
            print(f'\n[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')

    def main(self):
        self.bind()
        self.start_thread()

if __name__ == "__main__":
    server = HTTTServer()
    server.main()