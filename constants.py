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
KILL_COORDS = (750, 200)
CURE_BITE_DIMS = (200, 200)
CELL_DIMENSIONS = (100, 100)  # number of pixels (x, y) for each cell
CUR_MOVE_COORDS = (800, 400)
MARGIN = 150  # Number of pixels to offset grid to the top-left side
SCORE_DIMS = (200,100)
SCORE_COORDS = (950, 10)
TRY_AGAIN_COORDS = (950, 50)
LAST_MOVE_COORDS = (10, 10)
STEPS_COORDS = (10, 50)
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
TURN_INDICATOR_COORDS = (850,480)

QUIT_COORDS = (800, 650)
QUIT_DIMS = (80, 50)
