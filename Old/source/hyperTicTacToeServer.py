import socket
import sys
import pickle
import random
import numpy as np
import threading


server = '192.168.1.22'

port = 5555

max_num_clients = 2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

# def list_to_ndarray(l):
#     ndarray = np.array(l)
#     return ndarray

# def ndarray_to_list(ndarray):
#     l = ndarray.tolist()
#     return l

game_moves = 0

game_record = np.zeros([9,9])

big_grid_record = np.zeros([3,3])

game_dict = {'game_record':game_record, 'big_grid_record':big_grid_record, 'game_moves':game_moves}

rand = random.random()

def update_game_moves():
    """
    Function updating the number of game moves played
    """

    global game_moves

    game_moves = game_moves + 1

if rand < 0.5:
    first_conn_side = int(0)
    first_conn_type = 'X'
    second_conn_side = int(1)
    second_conn_type = 'O'

elif rand >= 0.5:
    first_conn_side = int(1)
    first_conn_type = 'O'
    second_conn_side = int(0)
    second_conn_type = 'X'


disconnect_msg = '!DISCONNECT'

# current_side = 0

def threaded_client(conn, side):

    global game_dict

    print('threaded_client started\n')

    if side == 0:
        conn.send(pickle.dumps(first_conn_side))
    elif side == 1:
        conn.send(pickle.dumps(second_conn_side))

    # conn.send(pickle.dumps(int(side)))

    connected = True
    while connected:
        try:
            data = pickle.loads(conn.recv(2048))
            print('game data received')
            game_record = data['game_record']
            print(game_record)
            big_grid_record = data['big_grid_record']
            print(big_grid_record)

            if data == disconnect_msg:
                connected = False

            elif (data['game_record'] == game_dict['game_record']).all() == True and (data['big_grid_record'] == game_dict['big_grid_record']).all() == True:
                game_dict = data
            
            elif data['game_record'].shape == game_dict['game_record'].shape and data['big_grid_record'].shape == game_dict['big_grid_record'].shape:
                game_dict = data
                update_game_moves()
                game_dict['game_moves'] = game_moves


            conn.send(pickle.dumps(game_dict))
            print('game data sent')

        except socket.error as e:
            print(e)
            print('[ERROR] Error Sending Or Receiving Data')
            connected = False

    print('[LOST CONNECTION] Lost connection with Side ', side)
    conn.close()

# threads = []

def start_thread():
    s.listen(max_num_clients)
    print(f'[LISTENING] Server is listening on {server}')
    while True:
        conn, addr = s.accept()
        print('[CONNECTED TO] ', addr)

        thread = threading.Thread(target=threaded_client, args=[conn, threading.activeCount() - 1])
        thread.start()
        # current_side += 1
        print('[ACTIVE CONNECTIONS]', threading.activeCount() - 1)



print("[SERVER STARTING]")
start_thread()