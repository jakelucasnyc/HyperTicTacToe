import random

class AI:

    START_CORD = 40
    END_CORD = 760
    BBOX_SIZE = 80*3
    BOARD_SIZE = END_CORD-START_CORD

    def __init__(self, side):
        self.side = side
        self.clicked = False
        self.mouse_pos = None
        self.AI_turn = False
        self.game_moves = 0
        self.game_over = False

    def get_game_moves(self, game_moves):
        self.game_moves = game_moves
        if self.game_moves % 2 == self.side-1 and self.game_over == False:
            self.AI_turn = True
        else:
            self.AI_turn = False

    def get_info(self, game_over, next_b_cords, game_record):
        self.game_over = game_over
        self.next_b_cords = next_b_cords

    def get_mouse_pos(self):
        if not self.next_b_cords:
            move_cords = [random.randint(AI.START_CORD, AI.END_CORD), random.randint(AI.START_CORD, AI.END_CORD)]
            return move_cords

        move_cords = [random.randint(self.next_b_cords[0], self.next_b_cords[0]+AI.BBOX_SIZE-1), random.randint(self.next_b_cords[1], self.next_b_cords[1]+AI.BBOX_SIZE-1)]

        print("move_cords ", move_cords)

        return move_cords

    