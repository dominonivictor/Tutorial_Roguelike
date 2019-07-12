import tcod
from functions.game_loop import initialize_flags, initialize_objs_vars, initialize_constants
from constants import get_game_constants
from game_states import GameStates
from god import God
from input_handlers import handle_keys, handle_mouse
from entity import Entity, get_blocking_entity
from components.actor import Actor
from map_objects.game_map import GameMap
from functions.fov import initialize_fov, recompute_fov, set_tile_fov
from functions.death import kill_player, kill_creature 
from functions.render import RenderOrder

from functions.pc_actions import (move_action, pickup_action, remap_action, debug_action, god_toggle_action,
                                fire_action, wait_action, teleport_action, break_wall_action, create_wall_action,
                                process_player_turn_results)
from functions.interface_actions import show_inventory_action, inventory_index_action, drop_inventory_action

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

        self.player, self.entities, self.god, self.game_map, self.game_state, self.prev_game_state, self.fov_map, self.msg_log, self.key, self.mouse, self.targeting_item = initialize_objs_vars()

    def check_event(self):
        '''
        Is this if self.fov_recompute in the right place? I think it is a little lost in this func specifically
        maybe move it with the render func
        '''
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, self.key, self.mouse)
        if self.fov_recompute:
            recompute_fov(self.fov_map, self.player.x, self.player.y, 
                self.fov_radius, self.fov_light_walls, self.fov_algorithm)
        
    def player_action(self):
        '''
        This function gets the key from the player and does everything it needs to
        make the action execute
        Need to break this down even further, every action needs to be a separate func
        ''' 
        action = handle_keys(self.key, self.game_state)
        mouse_action = handle_mouse(self.mouse)
        #PC COMMANDS
        move = action.get('move')
        pickup = action.get('pickup')        
        #MENUS STUFF
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')

        #MOUSE
        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        ########My personal actions""""""""""
        wait = action.get('wait')
        teleport = action.get('teleport')
        break_wall = action.get('break_wall')
        create_wall = action.get('create_wall')
        fire = action.get('fire')
        player_turn_results = []
        #MASTERMIND COMMANDS
        god_toggle = action.get('god_toggle')
        remap = action.get('remap')
        debug = action.get('debug')
        ############33    """"""""""""""""""""""""""""""""""""
        fullscreen = action.get('fullscreen')
        exit = action.get('exit')

    ################################################################################################################################################
        



        #PLAYER ACTIONS 1st from TUT then from Me
        if move and self.game_state == GameStates.PLAYERS_TURN:
            move_action(self, move)

        if pickup and self.game_state == GameStates.PLAYERS_TURN:
            pickup_action(self)
        
        if show_inventory:
            show_inventory_action(self)

        if drop_inventory:
            drop_inventory_action(self)

        if inventory_index is not None and self.prev_game_state != GameStates.PLAYER_DEAD and inventory_index < len(self.player.inventory.items):
            inventory_index_action(self, inventory_index)

        if self.game_state == GameStates.TARGETING_MODE:
            if left_click:
                target_x, target_y = left_click

                item_use_results = self.player.inventory.use(self.targeting_item, entities=self.entities, fov_map=self.fov_map,
                                                    target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)

            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

            process_player_turn_results(self, player_turn_results)

        ## CUSTOM MADE ACTIONS
        if break_wall:
            break_wall_action(self)

        if create_wall:
            create_wall_action(self)

        if fire:
            fire_action(self)

        if teleport:
            teleport_action(self)

        
        if wait:
            wait_action(self)

        #MASTERMIND ACTIONS
        if god_toggle:
            god_toggle_action(self)

        if remap:
            remap_action(self)

        if debug:
            debug_action(self)


        #OUT OF GAME STUFF
        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        
        if exit:
            if self.game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                self.game_state = self.prev_game_state
            elif self.game_state == GameStates.TARGETING_MODE:
                player_turn_results.append({'targeting_cancelled': True})
            else:
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
                            self.msg_log.add_msg(message)

                        if dead_entity:
                            if dead_entity == self.player:
                                message, self.game_state = kill_player(dead_entity)
                            else:
                                message = kill_creature(dead_entity)

                            self.msg_log.add_msg(message)

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