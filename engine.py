import tcod
#import logging as log
from random import randint

from entity import Entity, get_blocking_entity
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import RenderOrder, clear_all, render_all
from fov_functions import initialize_fov, recompute_fov, set_tile_fov, get_entities_in_fov
from constants import get_game_constants
from game_states import GameStates
from god import God
from components.actor import Actor
from death_functions import kill_player, kill_creature

'''
I Want to decluter stuff here
I believe that at the end of the tut they clean this baby up, so i'm not too worried
but what i could do is create an update function and move the bulk of stuff there
separe even further by combat, god_actions and such
'''
def main():
    const = get_game_constants()
    #Constantes

    screen_width = const.get('screen_width')
    screen_height = const.get('screen_height')
    map_width = const.get('map_width')  
    map_height = const.get('map_height')

    fov_algorithm = const.get('fov_algorithm')
    fov_light_walls = const.get('fov_light_walls')
    fov_radius = const.get('fov_radius')

    #Inicializando Entidades
    actor_comp = Actor(mental=10, physical=5, spiritual=7)
    player = Entity(0, 0, '@', tcod.white, 'Hero', blocks=True, render_order=RenderOrder.ACTOR, actor=actor_comp)
    #npc = Entity(int(screen_width/2 - 5), int(screen_height/2), '@', tcod.yellow)
    entities = [player]
    god = God()

    the_bug = False

    #Inicializando a Tela (o console), seu nome e o mapa
    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    tcod.console_init_root(screen_width, screen_height, 'Project Tesla', False)

    con = tcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(player, entities, debug_map=the_bug)

    game_state = GameStates.PLAYERS_TURN

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    key = tcod.Key()
    mouse = tcod.Mouse()
     
    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(god, con, entities, player, game_map, fov_map, fov_recompute)
        
        fov_recompute = False

        tcod.console_flush()
        
        clear_all(con, entities)
        
        action = handle_keys(key)

        #PC COMMANDS
        move = action.get('move')
        break_wall = action.get('break')
        direction = action.get('direction')
        fire = action.get('fire')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        #MASTERMIND COMMANDS
        debug = action.get('debug')
        remap = action.get('remap')
        god_toggle = action.get('god_toggle')

        player_turn_results = []


        if god_toggle:
            god.toggle()
            fov_recompute = True

        if remap:
            entities = [player]
            game_map = GameMap(map_width, map_height)
            game_map.make_map(player, entities, debug_map=the_bug)
            fov_recompute = True
            fov_map = initialize_fov(game_map)
            remap = False

        if break_wall:
            #SUCCESS. just need to implement directions
            x = player.x+1
            y = player.y
            game_map.tiles[x][y].destroy_wall()
            fov_map = set_tile_fov(x, y, game_map, fov_map)
            fov_recompute = True
            
        if fire:
            for target in get_entities_in_fov(fov_map, entities):
                player.actor.attack_target(target) 

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            goto_x = player.x + dx
            goto_y = player.y + dy

            if not game_map.is_blocked(goto_x, goto_y):
                target = get_blocking_entity(entities, goto_x, goto_y)
                if target:
                    attack_results = player.actor.attack_target(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        if debug:
            #do debug things
            the_bug = False if the_bug else True
            print("X: ", player.x, "Y: ", player.y )
            #log.debug('msg goes here')

        for player_result in player_turn_results:
            message = player_result.get('message')
            dead_entity = player_result.get('dead')

            if message:
                print(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_creature(dead_entity)

                print(message)

        if game_state == GameStates.ENEMY_TURN:
            #Every other actionable entity will do stuff here
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_result in enemy_turn_results:
                        message = enemy_result.get('message')
                        dead_entity = enemy_result.get('dead')

                        if message:
                            print(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_creature(dead_entity)

                            print(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()