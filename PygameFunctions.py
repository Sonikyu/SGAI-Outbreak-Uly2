from typing import List, Tuple
import pygame
from constants import *
from Board import Board
import constants

# Initialize pygame
screen = pygame.display.set_mode(GAME_WINDOW_DIMENSIONS)
pygame.display.set_caption("Outbreak!")
pygame.font.init()
font = pygame.font.Font("Assets/MagiBlade.ttf", 30)
screen.fill(BACKGROUND)

HEART_SELECTED = False
SKULL_SELECTED = False

IS_TURN = True
PREVIOUS_MOVE = ' '

def get_action(GameBoard: Board, pixel_x: int, pixel_y: int):
    """
    Get the action that the click represents.
    If the click was on the heal button, returns "heal"
    Else, returns the board coordinates of the click (board_x, board_y) if valid
    Return None otherwise
    """
    # Check if the user clicked on the "heal" or "bite" icon, return "heal" or "bite" if so
    heal_bite_check = (
        pixel_x >= CURE_BITE_COORDS[0]
        and pixel_x <= CURE_BITE_COORDS[0] + CURE_BITE_DIMS[0]
        and pixel_y >= CURE_BITE_COORDS[1]
        and pixel_y <= CURE_BITE_COORDS[1] + CURE_BITE_DIMS[1]
    )
    kill_check = (
        pixel_x >= KILL_COORDS[0]
        and pixel_x <= KILL_COORDS[0] + CURE_BITE_DIMS[0]
        and pixel_y >= KILL_COORDS[1]
        and pixel_y <= KILL_COORDS[1] + CURE_BITE_DIMS[1]
    )
    reset_move_check = (
        pixel_x >= CLEAR_COORDS[0]
        and pixel_x <= CLEAR_COORDS[0] + CURE_BITE_DIMS[0]
        and pixel_y >= CLEAR_COORDS[1]
        and pixel_y <= CLEAR_COORDS[1] + CURE_BITE_DIMS[1]
    )
    quit_check = (
        pixel_x >= QUIT_COORDS[0]
        and pixel_x <= QUIT_COORDS[0] + QUIT_DIMS[0]
        and pixel_y >= QUIT_COORDS[1]
        and pixel_y <= QUIT_COORDS[1] + QUIT_DIMS[1]
    )
    board_x = int((pixel_x - MARGIN_X) / CELL_DIMENSIONS[0])
    board_y = int((pixel_y - MARGIN_Y) / CELL_DIMENSIONS[1])
    move_check = (
        board_x >= 0
        and board_x < GameBoard.columns
        and board_y >= 0
        and board_y < GameBoard.rows
    )

    if heal_bite_check:
        if GameBoard.player_role == "Government":
            return "heal"
        return "bite"
    elif kill_check:
        return "kill"
    elif reset_move_check:
        return "reset move"
    elif quit_check:
        return "quit"
    elif move_check:
        return board_x, board_y
    return None

def reset_images():
    global HEART_SELECTED 
    global SKULL_SELECTED  

    HEART_SELECTED = False
    SKULL_SELECTED = False

def display_curr_action(act):
    global HEART_SELECTED 
    global SKULL_SELECTED   
    
    if act == "heal":
        HEART_SELECTED = not HEART_SELECTED
        SKULL_SELECTED = False

    elif act == "kill":
        SKULL_SELECTED = not SKULL_SELECTED
        HEART_SELECTED = False

    else:
        HEART_SELECTED = False
        SKULL_SELECTED = False

def get_last_move(player, move, success):
    global PREVIOUS_MOVE
    global IS_TURN
    if (move == None and success == None):
        PREVIOUS_MOVE = ' INVALID MOVE!'
        IS_TURN = True
    elif (move == 'move'):
        if (player == 'Government'):
            PREVIOUS_MOVE = ' human moved'
            IS_TURN = False
        else:
            PREVIOUS_MOVE = ' zombie moved'
            IS_TURN = True
    else:
        if (success) :
            PREVIOUS_MOVE = ' ' + str(move) +' succeeded'
        elif(not success):
            PREVIOUS_MOVE = ' ' + str(move) +' failed '
        if (player == 'Government'):
            IS_TURN = False
        else:
            IS_TURN = True

def display_text (text, coords, font_size):
    font_temp = pygame.font.Font("Assets/Magiblade.ttf", font_size)
    score = font_temp.render(text, True, (255,255,255))
    screen.blit(score, coords)


def run(GameBoard: Board):
    """
    Draw the screen and return any events.
    """
    screen.fill(BACKGROUND)
    build_grid(GameBoard)  # Draw the grid
    # Draw the heal icon
    if GameBoard.player_role == "Government":
        pygame.draw.rect(
            screen,
            DIVIDER_COLOR,
            [
                RIGHT_DIVIDER_COORDS[0],
                RIGHT_DIVIDER_COORDS[1],
                KEY_DIMS[0],
                KEY_DIMS[1],
            ],
        )
       
        if HEART_SELECTED:
            display_image(screen, "Assets/highlighted heart icon.png", CURE_BITE_DIMS, CURE_BITE_COORDS)
        else:
            display_image(screen, "Assets/heart icon.png", CURE_BITE_DIMS, CURE_BITE_COORDS)

        if SKULL_SELECTED:
            display_image(screen, "Assets/highlighted skull icon.png", CURE_BITE_DIMS, KILL_COORDS)
        else:
            display_image(screen, "Assets/skull icon.png", CURE_BITE_DIMS, KILL_COORDS)

        if IS_TURN:
            display_image(screen, "Assets/yourturn.png", TURN_INDICATOR_DIMS, TURN_INDICATOR_COORDS)
        else:
            display_image(screen, "Assets/theirturn.png", TURN_INDICATOR_DIMS, TURN_INDICATOR_COORDS)
        #static variables
        display_text(f"Last Move:"+str(PREVIOUS_MOVE), LAST_MOVE_COORDS, 25) 
        display_image(screen, "Assets/clear move icon.png", CURE_BITE_DIMS, CLEAR_COORDS)
        display_text(f"Kill", KILL_TEXT_COORD, 25)
        display_text(f"Cure", CURE_TEXT_COORD, 25)
        display_text(f"Reset", RESET_TEXT_COORD, 25)
        
    display_people(GameBoard)
    #display_reset_move_button()

    #static ui 
    display_image(screen, "Assets/key.png", KEY_DIMS, KEY_COORDS)
    display_text(f"Score: {constants.CURRENT_SCORE}", SCORE_COORDS, 25)
    display_text(f"Steps Left: {100-constants.number_steps}", STEPS_COORDS, 25)
    display_text(f"QUIT?", QUIT_COORDS, 25)
    return pygame.event.get()

def display_reset_move_button():
    rect = pygame.Rect(
        RESET_MOVE_COORDS[0],
        RESET_MOVE_COORDS[1],
        RESET_MOVE_DIMS[0],
        RESET_MOVE_DIMS[1],
    )
    pygame.draw.rect(screen, BLACK, rect)
    screen.blit(font.render("Reset move?", True, WHITE), RESET_MOVE_COORDS)

def display_image(
    screen: pygame.Surface,
    itemStr: str,
    dimensions: Tuple[int, int],
    position: Tuple[int, int],
):
    """
    Draw an image on the screen at the indicated position.
    """
    v = pygame.image.load(itemStr).convert_alpha()
    v = pygame.transform.scale(v, dimensions)
    screen.blit(v, position)


def build_grid(GameBoard: Board):
    """
    Draw the grid on the screen.
    """
    grid_width = GameBoard.columns * CELL_DIMENSIONS[0]
    grid_height = GameBoard.rows * CELL_DIMENSIONS[1]
    # left
    pygame.draw.rect(
        screen,
        BLACK,
        [
            MARGIN_X,
            MARGIN_Y,
            LINE_WIDTH,
            grid_height + (LINE_WIDTH),
        ],
    )
    # right
    pygame.draw.rect(
        screen,
        BLACK,
        [
            MARGIN_X + grid_width,
            MARGIN_Y,
            LINE_WIDTH,
            grid_height + (LINE_WIDTH),
        ],
    )
    # bottom
    pygame.draw.rect(
        screen,
        BLACK,
        [
            MARGIN_X,
            MARGIN_Y + grid_height,
            grid_width + (LINE_WIDTH),
            LINE_WIDTH,
        ],
    )
    # top
    pygame.draw.rect(
        screen,
        BLACK,
        [
            MARGIN_X,
            MARGIN_Y,
            grid_width + (LINE_WIDTH),
            LINE_WIDTH,
        ],
    )
    # Fill the inside wioth the cell color
    pygame.draw.rect(
        screen,
        CELL_COLOR,
        [MARGIN_X+LINE_WIDTH, MARGIN_Y+LINE_WIDTH, grid_width-LINE_WIDTH, grid_height-LINE_WIDTH],
    )

    # Draw the vertical lines
    i = MARGIN_X + CELL_DIMENSIONS[0]
    while i < MARGIN_X + grid_width:
        pygame.draw.rect(screen, BLACK, [i, MARGIN_Y, LINE_WIDTH, grid_height])
        i += CELL_DIMENSIONS[0]
    # Draw the horizontal lines
    i = MARGIN_Y + CELL_DIMENSIONS[1]
    while i < MARGIN_Y + grid_height:
        pygame.draw.rect(screen, BLACK, [MARGIN_X, i, grid_width, LINE_WIDTH])
        i += CELL_DIMENSIONS[1]


def display_people(GameBoard: Board):
    """
    Draw the people (government, vaccinated, and zombies) on the grid.
    """
    for x in range(len(GameBoard.States)):
        if GameBoard.States[x].person != None:
            p = GameBoard.States[x].person
            coords = (
                int(x % GameBoard.rows) * CELL_DIMENSIONS[0] + MARGIN_X + 35,
                int(x / GameBoard.columns) * CELL_DIMENSIONS[1] + MARGIN_Y + 20,
            )
            coords_no_margin = (
                int(x % GameBoard.rows) * CELL_DIMENSIONS[0] + MARGIN_X+LINE_WIDTH,
                int(x / GameBoard.columns) * CELL_DIMENSIONS[1] + MARGIN_Y+LINE_WIDTH,
            )
            if GameBoard.States[x].location in GameBoard.statesSelected:
                square = "Assets/BlueSquare.png"
                if p.isZombie:
                    square = "Assets/RedSquare.png"
                display_image(screen, square, (100-LINE_WIDTH,100-LINE_WIDTH), coords_no_margin)
                    
            
            char = "Assets/" + IMAGE_ASSETS[0]
            if p.isZombie:
                if p.zombieStage==1:
                    char = "Assets/"+IMAGE_ASSETS[3]
                elif p.zombieStage==2:
                    char = "Assets/"+IMAGE_ASSETS[4]
                else:
                    char = "Assets/" + IMAGE_ASSETS[2]
            
            display_image(screen, char, (35, 60), coords)


def display_cur_move(cur_move: List):
    # Display the current action
    '''
    screen.blit(
        font.render("Your move is currently:", True, WHITE),
        CUR_MOVE_COORDS,
    )
    screen.blit(
        font.render(f"{cur_move}", True, WHITE),
        (
            CUR_MOVE_COORDS[0],
            CUR_MOVE_COORDS[1] + font.size("Your move is currently:")[1] * 2,
        ),
    )
    '''


def display_win_screen(dataCollector):
    dataCollector.print_attributes()
    screen.fill(BACKGROUND)
    screen.blit(
        font.render("You win!", True, WHITE),
        (500, 400),
    )
    display_text(f"Score: {constants.CURRENT_SCORE}", SCORE_COORDS, 32)
    pygame.display.update()

    # catch quit event
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


def display_lose_screen(dataCollector):
    dataCollector.print_attributes()
    screen.fill(BACKGROUND)
    screen.blit(
        font.render("You lose!", True, WHITE),
        (500, 400),
    )
    pygame.display.update()

    # catch quit event
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


def direction(coord1: Tuple[int, int], coord2: Tuple[int, int]):
    if coord2[1] > coord1[1]:
        return "moveDown"
    elif coord2[1] < coord1[1]:
        return "moveUp"
    elif coord2[0] > coord1[0]:
        return "moveRight"
    elif coord2[0] < coord1[0]:
        return "moveLeft"

def display_turn(myturn):
    global IS_TURN
    if myturn == 1:
        IS_TURN = True
    else:
        IS_TURN - False
    