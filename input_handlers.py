import tcod
from game_states import GameStates
from functions.render import get_mouse_xy

def handle_keys(key, game_state):
    if game_state is GameStates.PLAYERS_TURN:
        return handle_pc_turn_keys(key)
    elif game_state is GameStates.TARGETING_MODE:
        return handle_targeting_keys(key)
    elif game_state is GameStates.PLAYER_DEAD:
        return handle_pc_dead_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key) 

    return {}

def handle_targeting_keys(key):
    if key.vk is tcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_pc_turn_keys(key):
    '''
    Recieves the pressed key as input and outputs a dictionary 
    containing the command and its parameters
    '''
    key_char = chr(key.c)

    #Movimentação
    if key.vk == tcod.KEY_UP or key.vk == tcod.KEY_KP8:
        return {'move': (0,-1)}#UP
    elif key.vk == tcod.KEY_DOWN or key.vk == tcod.KEY_KP2:
        return {'move': (0,1)}#DOWN
    elif key.vk == tcod.KEY_LEFT or key.vk == tcod.KEY_KP4:
        return {'move': (-1,0)}#LEFT
    elif key.vk == tcod.KEY_RIGHT or key.vk == tcod.KEY_KP6:
        return {'move': (1,0)}#RIGHT
    #Diagonals
    elif key.vk == tcod.KEY_KP3:
        return {'move': (1,1)}# DOWN RIGHT
    elif key.vk == tcod.KEY_KP9:
        return {'move': (1,-1)}# UP RIGHT
    elif key.vk == tcod.KEY_KP1:
        return {'move': (-1,1)}# DOWN LEFT
    elif key.vk == tcod.KEY_KP7:
        return {'move': (-1,-1)}# UP LEFT

    #Tutorial actions
    if key_char == 'h' or key_char == 'p':
        return {'pickup': True}

    if key_char == 'd':
        return {'drop_inventory': True}

    if key_char == 'i':
        return {'show_inventory': True}

    #MY Personal actions
    elif key.vk == tcod.KEY_KP5 or key_char == 'w':
        return {'wait': True}

    if key_char == 'f':
        return {'fire': True}

    if key_char == 't':
        return {'teleport': True}

    #Debug Stuff
    if key_char == 'd':
        return {'debug': True}

    if key_char == 'b':
        return {'break_wall': True}

    if key_char == 'c':
        return {'create_wall': True}

    if key_char == 'r':
        return {'remap': True}

    if key_char == 'g':
        return {'god_toggle': True}



    #Other keys
    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.vk == tcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}

def handle_inventory_keys(key):
    index = key.vk - tcod.KEY_1 #???

    if index >= 0:
        return {'inventory_index': index}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        #Alt+Enter => toggle full screen
        return {'fullscreen': True}
    elif key.vk == tcod.KEY_ESCAPE:
        #Exit the menu
        return {'exit': True}

    return {}


def handle_pc_dead_keys(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        #Alt+Enter => toggle full screen
        return {'fullscreen': True}
    elif key.vk == tcod.KEY_ESCAPE:
        #Exit the menu
        return {'exit': True}

    return {}

def handle_mouse(mouse):
    (x, y) = get_mouse_xy(mouse)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}