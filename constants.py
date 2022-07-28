# Constants


ROWS = 6
COLUMNS = 6
ACTION_SPACE = ["moveUp", "moveDown", "moveLeft", "moveRight", "heal", "bite"]

# Player role variables
ROLE_TO_ROLE_NUM = {"Government": 1, "Zombie": -1}
ROLE_TO_ROLE_BOOLEAN = {"Government": False, "Zombie": True}

# Pygame constants
BACKGROUND = "#1C1C1C"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CELL_COLOR = (100, 100, 100)
DIVIDER_COLOR = (68, 67, 67)
LINE_WIDTH = 5
IMAGE_ASSETS = [
    "person_normal.png",
    "person_vax.png",
    "person_zombie.png",
    "zombie_stage_1.png",
    "zombie_stage_2.png"
]
GAME_WINDOW_DIMENSIONS = (1200, 800)
RESET_MOVE_COORDS = (800, 600)
RESET_MOVE_DIMS = (200, 50)
CURE_BITE_COORDS = (950, 200)
KILL_COORDS = (950, 87)
CURE_BITE_DIMS = (200, 200)
CELL_DIMENSIONS = (100, 100)  # number of pixels (x, y) for each cell
CUR_MOVE_COORDS = (800, 400)
MARGIN_X = 300  # Number of pixels to offset grid to the top-left side
MARGIN_Y = 100
SCORE_DIMS = (200,100)
SCORE_COORDS = (950, 30)
LAST_MOVE_COORDS = (300, 725)
STEPS_COORDS = (30, 30)
#STEPS_COORDS = (800, 750)
CURRENT_SCORE = 0
SCORE_VALUES = { # TEMPORARY VALUES
    "heal":250,
    "kill":-100,
    "move":-25,
    "bite":-500,
    "repetitiveMove":-50


}
TIME_BETWEEN_ZOMBIE_MOVE = 1000 # ms

CURE_SUCCESS_RATES = [1, 0.9, 0.8, 0.5] # these are temporary values

NUM_MOVES_UNTIL_STAGE_2 = 2
NUM_MOVES_UNTIL_STAGE_3 = 3

STAGE_2_BITE_RATE = .5
STAGE_3_BITE_RATE = 0.75

HEART_SELECTED = False
SKULL_SELECTED = False

number_steps = 0

TURN_INDICATOR_DIMS = (231,100)
TURN_INDICATOR_COORDS = (935,550)

QUIT_COORDS = (110, 725)
QUIT_DIMS = (80, 50)

KEY_COORDS = (20, 105)
KEY_DIMS = (260, 590)

RIGHT_DIVIDER_COORDS =(920, 105)

CLEAR_COORDS = (950,313)
