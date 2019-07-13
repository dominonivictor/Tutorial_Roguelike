import tcod
from game_states import GameStates
from input_handlers import handle_keys
from entity import get_blocking_entity
from map_objects.game_map import GameMap
from functions.fov import initialize_fov, set_tile_fov, get_entities_in_fov
from functions.death import kill_player, kill_creature 
from interface.game_messages import Message
from functions.render import get_entities_under_mouse, get_mouse_xy
'''
################################################################################################################################

                            REGULAR PLAYER ACTIONS: BREAK WALL, MOVE(AND ATTACK)
IN A NEAR FUTURE: FIRE PROJECTILE TO A  SINGLE ENEMY, CREATE WALL (WITH OPTIONAL MULTIPLE TILES), OTHER EARTH RELATED STUFFS
################################################################################################################################
'''
def process_player_turn_results(the_game, player_turn_results):
    for player_result in player_turn_results:
        message = player_result.get('message')
        dead_entity = player_result.get('dead')
        item_added = player_result.get('item_added')
        item_consumed = player_result.get('consumed')
        item_dropped = player_result.get('item_dropped')


        targeting = player_result.get('targeting')
        targeting_cancelled = player_result.get('targeting_cancelled')

        targeting_skill = player_result.get('targeting_skill')

        acted = player_result.get('acted')

        if message:
            the_game.msg_log.add_msg(message)

        if dead_entity:
            if dead_entity == the_game.player:
                message, the_game.game_state = kill_player(dead_entity)
            else:
                message = kill_creature(dead_entity)

            the_game.msg_log.add_msg(message)

        if item_added:
            the_game.entities.remove(item_added)

            the_game.game_state = GameStates.ENEMY_TURN

        if item_consumed:
            the_game.game_state = GameStates.ENEMY_TURN


        if item_dropped:
            the_game.entities.append(item_dropped)

            the_game.game_state = GameStates.ENEMY_TURN

        if targeting:
            the_game.prev_game_state = GameStates.PLAYERS_TURN
            the_game.game_state = GameStates.TARGETING_MODE

            the_game.targeting_item = targeting

            the_game.msg_log.add_msg(the_game.targeting_item.item.targeting_message)

        if targeting_skill:
            the_game.prev_game_state = GameStates.PLAYERS_TURN
            the_game.game_state = GameStates.TARGETING_MODE

            the_game.targeting_skill = targeting_skill

            the_game.msg_log.add_msg(the_game.targeting_skill.skill.targeting_message)

        if targeting_cancelled:
            the_game.game_state = the_game.prev_game_state

            the_game.msg_log.add_msg(Message('Targeting cancelled'))

        if acted:
            the_game.game_state = GameStates.ENEMY_TURN

'''
################################################################################################################################
                        ELEMENTAL TECHNIQUES
################################################################################################################################
'''
def create_wall_action(the_game):
    player_turn_results = []
    the_game.game_state = GameStates.TARGETING_MODE
    '''
    ############## NOTE ##############
    THIS WHILE LOOP WILL GENERATE PROBLEMS IN THE FUTURE, specifically with rendering animations(if i so wish to implement it)
    Need to find a better solution, maybe do targeting function first, and then after u get the direction u activate break_wall()
    '''
    while the_game.game_state == GameStates.TARGETING_MODE:

        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, the_game.key, the_game.mouse)
        x, y = handle_keys(the_game.key, the_game.game_state).get('move', (None, None))
        if x is not None:
            the_game.game_state = GameStates.ENEMY_TURN
        if handle_keys(the_game.key, the_game.game_state).get('exit'):
            the_game.game_state = GameStates.PLAYERS_TURN
            return False

    dx, dy = the_game.player.x + x, the_game.player.y + y
    if get_blocking_entity(the_game.entities, dx, dy):
        msg = {'message': Message("It's too heavy for you to create a wall here, there is someone there!", tcod.orange)}
        player_turn_results.append(msg)
        process_player_turn_results(the_game, player_turn_results)
        return None

    the_game.game_map.tiles[dx][dy].create_wall()
    the_game.fov_map = set_tile_fov(dx, dy, the_game.game_map, the_game.fov_map)
    the_game.fov_recompute = True


def break_wall_action(the_game):
    #THIS IS BROKEN FOR NOW
    player_turn_results = []
    the_game.game_state = GameStates.TARGETING_MODE
    '''
    ############## NOTE ##############33
    THIS WHILE LOOP WILL GENERATE PROBLEMS IN THE FUTURE, specifically with rendering animations(if i so wish to implement it)
    Need to find a better solution, maybe do targeting function first, and then after u get the direction u activate break_wall()
    '''
    while the_game.game_state == GameStates.TARGETING_MODE:

        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, the_game.key, the_game.mouse)
        x, y = handle_keys(the_game.key, the_game.game_state).get('move', (None, None))
        if x is not None:
            the_game.game_state = GameStates.ENEMY_TURN
        if handle_keys(the_game.key, the_game.game_state).get('exit'):
            the_game.game_state = GameStates.PLAYERS_TURN
            return False

    dx, dy = the_game.player.x + x, the_game.player.y + y
    the_game.game_map.tiles[dx][dy].destroy_wall()
    the_game.fov_map = set_tile_fov(dx, dy, the_game.game_map, the_game.fov_map)
    the_game.fov_recompute = True

    #break_results = the_game.player.actor.break_wall()



def teleport_action(the_game):
    #working partially, he attacks as if meelee if a target is in the desired space
    the_game.game_state = GameStates.TARGETING_MODE
    while the_game.game_state == GameStates.TARGETING_MODE:

        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, the_game.key, the_game.mouse)
        entities_under_mouse = get_entities_under_mouse(the_game.god, the_game.mouse, the_game.entities, the_game.fov_map)

        exit = handle_keys(the_game.key, the_game.game_state).get('exit')
        pos_x, pos_y = get_mouse_xy(the_game.mouse, offset=True)

        if the_game.mouse.lbutton_pressed or exit: 
            if exit:
                the_game.game_state = GameStates.PLAYERS_TURN
                return False 
            else:
                move = (pos_x - the_game.player.x, pos_y - the_game.player.y)
                move_action(the_game, move)


def fire_action(the_game):
    '''
    This is repeating code, create a better attack func that covers both move and fire actions
    Maybe create a range_attack for it to be used on entity.actor??
    '''
    player_turn_results = []
    entities_in_fov = get_entities_in_fov(the_game.fov_map, the_game.entities)
    if entities_in_fov:
        
        #GOD MODE FIRING ALL TARGETS ON SIGHT
        if the_game.god.tog:
            for target in entities_in_fov:
                attack_results = the_game.player.actor.attack_target(target)
                player_turn_results.extend(attack_results)
            process_player_turn_results(the_game, player_turn_results)

        #NORMAL MODE FIRING 1 TARGET W/ MOUSE CLICK
        else:
            the_game.game_state = GameStates.TARGETING_MODE
            while the_game.game_state == GameStates.TARGETING_MODE:

                tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, the_game.key, the_game.mouse)
                entities_under_mouse = get_entities_under_mouse(the_game.god, the_game.mouse, the_game.entities, the_game.fov_map)

                exit = handle_keys(the_game.key, the_game.game_state).get('exit')
                if the_game.mouse.lbutton_pressed or exit: 
                    if exit:
                        the_game.game_state = GameStates.PLAYERS_TURN
                        return False 
                    else:
                        the_game.game_state = GameStates.ENEMY_TURN
                        for entity in entities_under_mouse:
                            if entity.actor:
                                target = entity
                                attack_results = the_game.player.actor.attack_target(target)
                                player_turn_results.extend(attack_results)
                            
            process_player_turn_results(the_game, player_turn_results)
              
    else:
        message = Message("There are no targets in range", tcod.red)
        the_game.msg_log.add_msg(message)

    the_game.game_state = GameStates.ENEMY_TURN

'''
################################################################################################################################
                        REGULAR ACTIONS
################################################################################################################################
'''

def wait_action(the_game):
    the_game.game_state = GameStates.ENEMY_TURN 


'''
################################################################################################################################
                        TUTORIAL MADE ACTIONS
################################################################################################################################
'''

def move_action(the_game, move):
    '''
    This func needs the absolute distance it will move in (x, y) parameters
    '''
    player_turn_results = []
    dx, dy = move
    goto_x = the_game.player.x + dx
    goto_y = the_game.player.y + dy

    #Check if tile is blocked, atk if able to, walk if not
    try:
        if not the_game.game_map.is_blocked(goto_x, goto_y):
            target = get_blocking_entity(the_game.entities, goto_x, goto_y)
            if target:
                attack_results = the_game.player.actor.attack_target(target)
                player_turn_results.extend(attack_results)
            else:
                the_game.player.move(dx, dy)
                the_game.fov_recompute = True

            the_game.game_state = GameStates.ENEMY_TURN
        else:
            return {'fail': True}
    except IndexError:
        msg = {'message': Message('You cannot move there, it is forbbiden', tcod.orange)}
        player_turn_results.append(msg)
    #This basically processes all msgs
    process_player_turn_results(the_game, player_turn_results)

    return {}

def pickup_action(the_game):
    player_turn_results = []
    for entity in the_game.entities:
        if entity.item and entity.x == the_game.player.x and entity.y == the_game.player.y:
            pickup_results = the_game.player.inventory.add_item(entity)
            player_turn_results.extend(pickup_results)

            break
    else:
        the_game.msg_log.add_msg(Message('There is nothing here to pickup.', tcod.yellow))

    process_player_turn_results(the_game, player_turn_results)

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
    the_game.the_bug = not the_game.the_bug   
    print('Key.vk: ' + str(int(tcod.KEY_3))) 

def god_toggle_action(the_game):
    the_game.god.toggle()
    the_game.fov_recompute = True



'''
def player_actions(the_game):
'''
#For now this func is not being utilized... but probably will in the future...
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
'''