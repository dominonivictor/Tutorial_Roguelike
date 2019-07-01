import tcod
from game_states import GameStates
from input_handlers import handle_keys
from entity import get_blocking_entity
from map_objects.game_map import GameMap
from functions.fov import initialize_fov, set_tile_fov, get_entities_in_fov
from functions.death import kill_player, kill_creature 

'''
################################################################################################################################

                            REGULAR PLAYER ACTIONS: BREAK WALL, MOVE(AND ATTACK)
IN A NEAR FUTURE: FIRE PROJECTILE TO A  SINGLE ENEMY, CREATE WALL (WITH OPTIONAL MULTIPLE TILES), OTHER EARTH RELATED STUFFS
################################################################################################################################
'''

def break_wall_action(the_game):
    
    #SUCCESS. just need to implement directions
    the_game.game_state = GameStates.TARGETING_MODE
    '''
    ############## NOTE ##############33
    THIS WHILE LOOP WILL GENERATE PROBLEMS IN THE FUTURE, specifically with rendering animations(if i so wish to implement it)
    Need to find a better solution, maybe do targeting function first, and then after u get the direction u activate break_wall()
    '''
    while the_game.game_state == GameStates.TARGETING_MODE:

        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, the_game.key, the_game.mouse)
        x, y = handle_keys(the_game.key).get('move', (None, None))
        if x is not None:
            the_game.game_state = GameStates.ENEMY_TURN
    dx, dy = the_game.player.x + x, the_game.player.y + y
    the_game.game_map.tiles[dx][dy].destroy_wall()
    the_game.fov_map = set_tile_fov(dx, dy, the_game.game_map, the_game.fov_map)
    the_game.fov_recompute = True


def move_action(the_game, move):
    '''
    This func needs the absolute distance it will move in (x, y) parameters
    '''
    player_turn_results = []
    dx, dy = move
    goto_x = the_game.player.x + dx
    goto_y = the_game.player.y + dy

    if not the_game.game_map.is_blocked(goto_x, goto_y):
        target = get_blocking_entity(the_game.entities, goto_x, goto_y)
        if target:
            attack_results = the_game.player.actor.attack_target(target)
            player_turn_results.extend(attack_results)
        else:
            the_game.player.move(dx, dy)
            the_game.fov_recompute = True

        the_game.game_state = GameStates.ENEMY_TURN

    for player_result in player_turn_results:
        message = player_result.get('message')
        dead_entity = player_result.get('dead')

        if message:
            print(message)

        if dead_entity:
            if dead_entity == the_game.player:
                message, the_game.game_state = kill_player(dead_entity)
            else:
                message = kill_creature(dead_entity)

            print(message)

def fire_action(the_game):
    '''
    This is repeating code, create a better attack func that covers both move and fire actions
    '''
    player_turn_results = []
    entities_in_fov = get_entities_in_fov(the_game.fov_map, the_game.entities)
    if entities_in_fov:
        the_game.game_state = GameStates.ENEMY_TURN
        for target in entities_in_fov:
            attack_results = the_game.player.actor.attack_target(target)
            player_turn_results.extend(attack_results)
        for result in player_turn_results:
            message = result.get('message')
            dead_entity = result.get('dead')

            if message:
                print(message)

            if dead_entity:
                if dead_entity == the_game.player:
                    message, the_game.game_state = kill_player(dead_entity)
                else:
                    message = kill_creature(dead_entity)

                print(message)
    else:
        message = "There are no targets in range"
        print(message)

'''################################################################################################################################

                        GODLIKE ACTIONS: REMAP, DEBUG, GOD_SIGHT
IN A NEAR FUTURE: ADD GOD_INVUNERABILITY FOR NOT TAKING DMG AND DEBUG STUFF ON CONSOLE THAT WILL BE INTRODUCED IN THE NEXT PART
'''################################################################################################################################

def remap_action(the_game):
    the_game.entities = [the_game.player]
    the_game.game_map = GameMap(the_game.map_width, the_game.map_height)
    the_game.game_map.make_map(the_game.player, the_game.entities, debug_map=the_game.the_bug)
    the_game.fov_recompute = True
    the_game.fov_map = initialize_fov(the_game.game_map)


def debug_action(the_game):
    self.the_bug = False if self.the_bug else True
    print("X: ", self.player.x, "Y: ", self.player.y )      

def god_toggle_action(the_game):
    the_game.god.toggle()
    the_game.fov_recompute = True

def player_actions(the_game):
    '''
    For now this func is not being utilized... but probably will in the future...
    '''


    action = handle_keys(the_game.key)

    #PC COMMANDS
    move = action.get('move')
    break_wall = action.get('break')
    direction = action.get('direction')
    fire = action.get('fire')
    player_turn_results = []

    #MASTERMIND COMMANDS
    god_toggle = action.get('god_toggle')
    remap = action.get('remap')
    debug = action.get('debug')
    fullscreen = action.get('fullscreen')
    exit = action.get('exit')

################################################################################################################################################
    
    #PLAYER ACTIONS
    if break_wall:
        break_wall(the_game)
        
        
    if fire:
        for target in get_entities_in_fov(the_game.fov_map, the_game.entities):
            the_game.player.actor.attack_target(target) 

    if move and the_game.game_state == GameStates.PLAYERS_TURN:
        move_action(the_game, move)

    #MASTERMIND ACTIONS
    if god_toggle:
        the_game.god.toggle()
        fov_recompute = True

    if remap:
        remap_action()

    if debug:
        the_game.the_bug = False if the_game.the_bug else True
        print("X: ", the_game.player.x, "Y: ", the_game.player.y )

    if fullscreen:
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

    
    if exit:
        return True
