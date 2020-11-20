import pygame

class HTTT:

    pygame.init()

    #display data
    WIDTH = 1200
    HEIGHT = 800

    #title screen data
    HYPER = 'HYPER'
    TTT = 'TIC TAC TOE'
    START = 'START'
    START_X = 535
    START_Y = 400
    START_WIDTH = 140
    START_HEIGHT = 60

    #different colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    NBOX_COLOR = [255, 0, 0, 70]

    #fonts
    TFONT = pygame.font.Font('SIFONN_PRO.otf', 100)
    SFONT = pygame.font.Font('SIFONN_PRO.otf', 36)

    #locations of the grid edges
    START_CORD = 40
    END_CORD = 760

    #locations of the little boxes
    LBOX_SIZE = 80
    LX_CORDS = list(range(START_CORD,END_CORD + 1,LBOX_SIZE))
    LY_CORDS = list(range(START_CORD,END_CORD + 1,LBOX_SIZE))
    LBOX_CORDS = [LX_CORDS, LY_CORDS]

    #locations of the big boxes
    BBOX_SIZE = 3*LBOX_SIZE
    BX_CORDS = list(range(START_CORD,END_CORD + 1,BBOX_SIZE))
    BY_CORDS = list(range(START_CORD,END_CORD + 1,BBOX_SIZE))
    BBOX_CORDS = [BX_CORDS, BY_CORDS]

    #different line widths
    GLINE_WIDTH = 2
    BGLINE_WIDTH = 5
    LXO_LINE_WIDTH = 9
    BXO_LINE_WIDTH = 18

    #X and O formatting offsets
    X_OFFSET = 10
    O_OFFSET = 7

    #socket variables
    HEADERSIZE = 10