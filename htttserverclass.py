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
        self.game_record = np.zeros([9,9]) #array keeping track of the whole game
        self.big_grid_record = np.zeros([3,3]) #array keeping track of the big boxes that are completed
        self.small_grid_record = np.zeros([3,3]) #array representing the big box that I've clicked into and the values of each of the 9 boxes within it
        self.nsmall_grid_record = np.zeros([3,3]) #array representing the big box that I should go into next and the values of each of the 9 boxes within it

    def bind(self):
        try:
            self.s.bind((HTTTServer.server, HTTTServer.port))

        except socket.error as e:
            print(str(e))

    def threaded_client(self, conn, side, connected=True):

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