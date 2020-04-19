import os

FULLSCREEN = False

# CONSTANTS
TILE_SIZE = 32  # x32 = 256px
PLAYER_SCALING = 1
TILE_SCALING = 1

WINDOW_WIDTH = 512*2
WINDOW_HEIGHT = 512
WINDOW_TITLE = 'Tricerasect'

LEFT_FACING = 0
RIGHT_FACING = 1
DOWN_FACING = 2
UP_FACING = 3

# SPEED
MOVE_SPEED = 50
MOVE_SPEED_CHARGED = 0.7 * MOVE_SPEED

ENTITY_MS = 1

# ENTITY TYPES
E_ANT = 0
E_MOSQUITO = 1
E_SPIDER = 2
E_DUNG_BEETLE = 3

T_SPRAY = 10
T_LAMP = 11
T_VACUUM = 12

VOLUME = 0.5

# UPDATE RATES FOR ENTITIES
UR_PLAYER = 1

UR_MOSQUITO = 3
UR_ANT = 10
UR_SPIDER = 10
UR_DUNG_BEETLE = 10

UR_SPRAY = 10
UR_LAMP = 10
UR_VACUUM = 10

from pathlib import Path

PATH = {}
PATH['project'] = Path(os.path.dirname(__file__))
PATH['img'] = PATH['project'] / "images"
PATH['sound'] = PATH['project'] / "sounds"
PATH['maps'] = PATH['project'] / "tmx_maps"
