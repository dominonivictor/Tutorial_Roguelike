import tcod


def handle_keys(key):
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
    
    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.vk == tcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}