import tcod
from functions.game_loop import initialize_flags, initialize_objs_vars, initialize_constants
from constants import get_game_constants
from game_states import GameStates
from god import God
from input_handlers import handle_keys
from entity import Entity, get_blocking_entity
from components.actor import Actor
from map_objects.game_map import GameMap
from functions.fov import initialize_fov, recompute_fov, set_tile_fov
from functions.death import kill_player, kill_creature 
from functions.render import RenderOrder

from functions.pc_actions import break_wall_action, move_action, remap_action, debug_action, god_toggle_action, fire_action
 

class TheGame:
    '''
    Need to be careful not to repeat myself too many times...
    I think having this obj is a nice way to access all the data on the game passing only one var
    but maybe this is inefficient, passing the whole obj only to access one or two vars/objs,
    and also maybe this will become spagetti code. using it in every single function will make
    code less readable... hummmmmmmmm, maybe this was not the best idea... need to ask for help
    On the other hand, it is nice to alter the game vars/objs in only one place...
    '''

    def __init__(self):
        self.screen_width, self.screen_height, self.map_width, self.map_height, self.fov_algorithm, self.fov_light_walls, self.fov_radius = initialize_constants()

        self.the_bug, self.fov_recompute = initialize_flags()

        self.player, self.entities, self.god, self.game_map, self.game_state, self.fov_map, self.key, self.mouse = initialize_objs_vars()

    def check_event(self):
        '''
        Is this if self.fov_recompute in the right place? I think it is a little lost in this func specifically
        maybe move it with the render func
        '''
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, self.key, self.mouse)
        if self.fov_recompute:
            recompute_fov(self.fov_map, self.player.x, self.player.y, 
                self.fov_radius, self.fov_light_walls, self.fov_algorithm)
        
    def player_action(self):
        '''
        This function gets the key from the player and does everything it needs to
        make the action execute
        Need to break this down even further, every action needs to be a separate func
        ''' 

        action = handle_keys(self.key)

        #PC COMMANDS
        move = action.get('move')
        break_wall = action.get('break_wall')
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
            break_wall_action(self)

        if fire:
            fire_action(self)


        if move and self.game_state == GameStates.PLAYERS_TURN:
            move_action(self, move)

        #MASTERMIND ACTIONS
        if god_toggle:
            god_toggle_action(self)

        if remap:
            remap_action(self)

        if debug:
            debug_action(self)


        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        
        if exit:
            return True


    def enemy_action(self):
        if self.game_state == GameStates.ENEMY_TURN:
            #Every other actionable entity will do stuff here
            for entity in self.entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(self.player, self.fov_map, self.game_map, self.entities)

                    for enemy_result in enemy_turn_results:
                        message = enemy_result.get('message')
                        dead_entity = enemy_result.get('dead')

                        if message:
                            print(message)

                        if dead_entity:
                            if dead_entity == self.player:
                                message, self.game_state = kill_player(dead_entity)
                            else:
                                message = kill_creature(dead_entity)

                            print(message)

                            if self.game_state == GameStates.PLAYER_DEAD:
                                break

                    if self.game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                self.game_state = GameStates.PLAYERS_TURN


    def update(self):
        exit = self.player_action()
        self.enemy_action()

        return exit