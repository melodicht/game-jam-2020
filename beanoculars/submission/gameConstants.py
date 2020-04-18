# Constants
WINDOW_WIDTH = 512
WINDOW_HEIGHT = 512
WINDOW_TITLE = 'Main Game Window'

TILE_SIZE = 32  # x32 = 256px
PLAYER_SCALING = 1
TILE_SCALING = 1

LEFT_FACING = 0
RIGHT_FACING = 1
DOWN_FACING = 2
UP_FACING = 3

# ENTITY TYPES
E_ANT = 0
E_MOSQUITO = 1
E_SPIDER = 2
E_DUNG_BEETLE = 3

T_SPRAY = 10
T_LAMP = 11
T_VACUUM = 12

DEBUG_MODE = True
if DEBUG_MODE:
    PATH_ADD = ''
else:
    PATH_ADD = 'submission\\'
