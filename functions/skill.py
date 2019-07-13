
#Functions to excecute skills

#####################################################################################
#                    EARTH SKILLS
#####################################################################################

#create_wall
#break_wall
#push_wall
import tcod
from interface.game_messages import Message
from functions.fov import set_tile_fov
from entity import get_blocking_entity
from functions.pc_actions import move_action



def create_wall(*args, **kwargs):
    '''
    recieves 3 kwargs: the_game, target_x, target_y 
    '''
    the_game = kwargs.get('the_game')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    entities = the_game.entities
    game_map = the_game.game_map
    fov_map = the_game.fov_map
    fov_recompute = the_game.fov_recompute


    results = []

    if get_blocking_entity(entities, target_x, target_y):
        msg = Message('It\'s too heavy for you to create a wall here', tcod.yellow)
        results.append({'acted': False, 'message':msg})
    else:
        msg = Message('CRUNCH! A wall is created', tcod.light_green)
        results.append({'acted': True, 'message': msg})
        game_map.tiles[target_x][target_y].create_wall()
        fov_map = set_tile_fov(target_x, target_y, game_map, fov_map)
        fov_recompute = True #do i need to do this here??

    return results

def break_wall(*args, **kwargs):
    '''
    recieves 3 kwargs: the_game, target_x, target_y 
    '''
    the_game = kwargs.get('the_game')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    entities = the_game.entities
    game_map = the_game.game_map
    fov_map = the_game.fov_map
    fov_recompute = the_game.fov_recompute


    results = []

    wall = the_game.game_map.tiles[target_x][target_y].blocked
    if not wall:#there is a wall here
        msg = Message('There is no wall to break here', tcod.yellow)
        results.append({'acted': False, 'message':msg})
    elif wall:
        msg = Message('CRUNCH! A wall is broken', tcod.light_green)
        results.append({'acted': True, 'message': msg})
        game_map.tiles[target_x][target_y].destroy_wall()
        fov_map = set_tile_fov(target_x, target_y, game_map, fov_map)
        fov_recompute = True #do i need to do this here??

    return results

def move_wall(*args, **kwargs):
    results = []

    the_game = kwargs.get('the_game')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    new_target_x = kwargs.get('new_target_x')
    new_target_y = kwargs.get('new_target_y')

    wall_to_be_moved = the_game.game_map.tiles[target_x][target_y].blocked
    tile_to_move_wall = the_game.game_map.tiles[new_target_x][new_target_y].blocked

    if not wall_to_be_moved or new_target_x is None or tile_to_move_wall:
        msg = Message('There is no wall to break here', tcod.yellow)
        results.append({'acted': False, 'message':msg})
    elif wall_to_be_moved:
        break_wall(the_game=the_game, target_x=target_x, target_y=target_y)
        create_wall(the_game=the_game, target_x=new_target_x, target_y=new_target_y)
        results.append({'acted': True, 'message': Message('Success', tcod.cyan)})

    return results

#####################################################################################
#                    AIR SKILLS
#####################################################################################

def teleport(*args, **kwargs):
    the_game = kwargs.get('the_game')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    move = (target_x - the_game.player.x, target_y - the_game.player.y)
    move_result = move_action(the_game, move)
    if move_result.get('fail'):
        results.append({'message': Message('Cant move here!')})
    else:
        results.append({'message': Message('ZOOM, you teleported')})

    return results


