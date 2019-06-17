import tcod


def render_all(god, con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
    ''' 
    Draw all the tiles and entities in the game map, taking the console, all entities, game_map, screen vars and colors as input
    '''
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = tcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        tcod.console_set_char_background(con, x, y, colors.get('light_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, colors.get('light_ground'), tcod.BKGND_SET)
                
                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored or god.sight:
                    if wall:
                        tcod.console_set_char_background(con, x, y, colors.get('dark_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, colors.get('dark_ground'), tcod.BKGND_SET)

                else:# if god mode is turned off, it will make all non explored stuff turn black again
                    tcod.console_set_char_background(con, x, y, colors.get('black'), tcod.BKGND_SET)
            
    for entity in entities:
        draw_entity(god, con, entity, fov_map)

    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(god, con, entity, fov_map):
    if entity_in_fov(god, entity, fov_map):
        tcod.console_set_default_foreground(con, entity.color)
        tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)


def entity_in_fov(god, entity, fov_map):
    if god.sight:
        return True
    elif tcod.map_is_in_fov(fov_map, entity.x, entity.y):
        return True
    else:
        return False

def clear_entity(con, entity):
    # erase the character that represents this object
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)