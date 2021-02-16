import pygame
from Player import Player
from AI import AI
from Button import Button
from Title import Title
from Game import Game
from GamePlanner import GamePlanner


flags = (True, True)



def title():
    title_inst = Title()
    while True:
        title_inst.title_aesthetics()
        title_inst.input()
        if title_inst.button_logic() is not None:
            flags = title_inst.button_logic()
        if title_inst.game_started:
            return True, flags



def game_loop(flags):
    game_inst = Game(*flags)
    game_inst.screen.fill(Game.WHITE)
    game_inst.draw_grid(Game.LBOX_CORDS, Game.GLINE_WIDTH, game_inst.screen)
    game_inst.draw_grid(Game.BBOX_CORDS, Game.BGLINE_WIDTH, game_inst.screen)
    pygame.display.update()
    game_inst.init()
    while True:
        if game_inst.game_moves % 2 == 0:
            game_inst.inform_and_input(game_inst.player1)
            game_inst.update_objects(game_inst.player1)
        elif game_inst.game_moves % 2 == 1:
            game_inst.inform_and_input(game_inst.player2)
            game_inst.update_objects(game_inst.player2)
        if game_inst.quit:
            return True #preparing to restart the main loop
        game_inst.side_panel_display()
        if not game_inst.cords or not game_inst.b_cords:
            continue
        game_inst.draw_rects(game_inst.big_grid_record, game_inst.screen, Game.BBOX_SIZE)
        game_inst.draw_shapes(game_inst.game_record, Game.LBOX_SIZE, Game.LXO_LINE_WIDTH, game_inst.screen)
        game_inst.draw_shapes(game_inst.big_grid_record, Game.BBOX_SIZE, Game.BXO_LINE_WIDTH, game_inst.screen)
        # pygame.display.update()
        if game_inst.game_over:
            game_inst.end(game_inst.winning_game_side)

        game_inst.draw_grid(Game.LBOX_CORDS, Game.GLINE_WIDTH, game_inst.screen)
        game_inst.draw_grid(Game.BBOX_CORDS, Game.BGLINE_WIDTH, game_inst.screen)

        if game_inst.game_over:
            while True:
                game_inst.end_aesthetics(game_inst.winning_game_side, game_inst.game_drawn)
                game_inst.inform_and_input(game_inst.player1)
                game_inst.inform_and_input(game_inst.player2)
                if game_inst.quit:
                    return True #preparing to restart the main loop

        pygame.display.update()


def game_planner_loop(mainGame):

	game_planner_inst = GamePlanner(mainGame)
	while True:
		if game_planner_inst.game_moves % 2 == 0:
			game_planner_inst.input()
			game_planner_inst.update_objects(game_planner_inst.player1)
		elif game_inst.game_moves % 2 == 1:
            game_planner_inst.input()
            game_planner_inst.update_objects(game_planner_inst.player2)




if __name__ == "__main__":
    while True:
        game_started, flags = title()
        if game_started:
            quit = game_loop(flags)
        if quit:
            continue