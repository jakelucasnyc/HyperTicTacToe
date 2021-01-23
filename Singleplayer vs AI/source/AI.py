import random

class AI:

    START_CORD = 40
    END_CORD = 760
    BOARD_SIZE = END_CORD-START_CORD

    def __init__(self, side):
        self.side = side
        self.clicked = False
        self.mouse_pos = None
        self.AI_turn = False
        self.game_moves = 0

    def get_game_moves(self, game_moves):
        self.game_moves = game_moves
        if self.game_moves % 2 == self.side-1:
            self.AI_turn = True
        else:
            self.AI_turn = False

    def get_mouse_pos(self):
        while (self.game_moves % 2 == self.side-1):
            move_cords = [random.randint(AI.START_CORD, AI.END_CORD), random.randint(AI.START_CORD, AI.END_CORD)]

            return move_cords

    