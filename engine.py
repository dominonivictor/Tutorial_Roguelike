import tcod
import logging as log

from entity import Entity
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all
from fov_functions import initialize_fov, recompute_fov
from constants import get_game_constants, get_colors
from god import God
'''
log.basicConfig =(
    filename = 'log.txt',
    level=log.DEBUG 
    )
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

    colors = get_colors()

    #Inicializando Entidades
    player = Entity(int(screen_width/2), int(screen_height/2), '@', tcod.white)
    npc = Entity(int(screen_width/2 - 5), int(screen_height/2), '@', tcod.yellow)
    entities = [npc, player]
    god = God()

    #Inicializando a Tela (o console), seu nome e o mapa
    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    tcod.console_init_root(screen_width, screen_height, 'Project Tesla', False)

    con = tcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(player)

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    key = tcod.Key()
    mouse = tcod.Mouse()
     
    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(god, con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        
        fov_recompute = False

        tcod.console_flush()
        
        clear_all(con, entities)
        
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        debug = action.get('debug')
        remap = action.get('remap')
        god_toggle = action.get('god_toggle')

        if god_toggle:
            god.toggle()

        if remap:
            game_map = GameMap(map_width, map_height)
            game_map.make_map(player)
            fov_recompute = True
            fov_map = initialize_fov(game_map)
            remap = False

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y +dy):
                player.move(dx, dy)

                fov_recompute = True

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        if debug:
            #do debug things
            print('Bizz, bizz, bizzzz')
            #log.debug('msg goes here')



if __name__ == '__main__':
    main()