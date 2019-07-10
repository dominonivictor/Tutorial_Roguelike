import tcod

from constants import get_game_constants, get_actor_stats
from game_states import GameStates
from god import God
from input_handlers import handle_keys
from entity import Entity, get_blocking_entity
from components.actor import Actor
from map_objects.game_map import GameMap
from functions.fov import initialize_fov, recompute_fov, set_tile_fov, get_entities_in_fov
from functions.death import kill_player, kill_creature 
from functions.render import RenderOrder
from interface.game_messages import MessageLog


const = get_game_constants()
pstats = get_actor_stats()['player']
'''
    make a game object to handle the stuff?? use to save important data?
'''

def initialize_constants():
    screen_width = const.get('screen_width')
    screen_height = const.get('screen_height')
    
    map_width = const.get('map_width')  
    map_height = const.get('map_height')

    fov_algorithm = const.get('fov_algorithm')
    fov_light_walls = const.get('fov_light_walls')
    fov_radius = const.get('fov_radius')

    return screen_width, screen_height, map_width, map_height, fov_algorithm, fov_light_walls, fov_radius

def initialize_flags():
    the_bug = False
    fov_recompute = True

    return the_bug, fov_recompute

def initialize_objs_vars():
    '''
    Initializing all game objects (and some important vars) at the start of the run, namely:
    Objects: Player, entities, god, game_map,
    Important VARS: game_state, fov_map, key, mouse
    '''
    # OBJECTS
    actor_comp = Actor(mental=pstats['mental'], physical=pstats['physical'], spiritual=pstats['spiritual'])
    player = Entity(0, 0, '@', tcod.white, 'Hero', blocks=True, render_order=RenderOrder.ACTOR, actor=actor_comp)
    entities = [player]
    god = God()
    game_map = GameMap(const.get('map_width'), const.get('map_height'))
    game_map.make_map(player, entities)

    #Important vars
    game_state = GameStates.PLAYERS_TURN
    fov_map = initialize_fov(game_map)
    key = tcod.Key()
    mouse = tcod.Mouse()

    #Message related stuff, in a near future, separate into combat, qests, chat, etc
    msg_log = MessageLog(const['message_x'], const['message_width'], const['message_height'])

    return player, entities, god, game_map, game_state, fov_map, msg_log, key, mouse
