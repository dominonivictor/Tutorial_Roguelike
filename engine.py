import tcod


from entity import Entity
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all


def main():
    #Constantes
    screen_width = 80
    screen_height = 50
    map_width = 70
    map_height = 45
    
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    colors = {

        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150)
    
    }

    #Inicializando Entidades
    player = Entity(int(screen_width/2), int(screen_height/2), '@', tcod.white)
    npc = Entity(int(screen_width/2 - 5), int(screen_height/2), '@', tcod.yellow)
    entities = [npc, player]
    
    #Inicializando a Tela (o console), seu nome e o mapa
    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    tcod.console_init_root(screen_width, screen_height, 'tcod tutorial revised', False)

    con = tcod.console_new(screen_width, screen_height)
    
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_height, map_width, player)

    key = tcod.Key()
    mouse = tcod.Mouse()
     
    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
    
        render_all(con, entities, game_map, screen_width, screen_height, colors)
        
        tcod.console_flush()
        
        clear_all(con, entities)
        
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y +dy):
                player.move(dx, dy)

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())




if __name__ == '__main__':
    main()