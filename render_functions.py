import tcod
from enum import Enum
from constants import get_game_constants, get_colors

const = get_game_constants()
colors = get_colors()

class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

def render_all(god, con, entities, player, game_map, fov_map, fov_recompute):
    ''' 
    Draw all the tiles and entities in the game map, taking the console, all entities, game_map, screen vars and colors as input
    Starting to draw stats on the screen! Think carefully about this and change stuff acordingly, probably move the UI part into another file
    '''
    if fov_recompute:
        for y in range(const.get('map_height')):
            for x in range(const.get('map_width')):
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
    
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(god, con, entity, fov_map)

    tcod.console_set_default_foreground(con, tcod.white)
    '''
    This is the way that was taught by the Tutorial:
    tcod.console_print_ex(con, 1, const.get('screen_height') - 2, tcod.BKGND_NONE, tcod.LEFT,
                            'HP: {0:02}/{1:02}'.format(player.actor.hp, player.actor.max_hp))

    WoA, printing on screen is so very satisfiying, and such an important part of the whole game, need to study this carefully and diligently
    '''
    tcod.console_print_ex(con, 5 , 2, tcod.BKGND_NONE, tcod.LEFT,
                            'HP: {0:02}/{1:02}\nName: {2}\nMen: {3}, Phy: {4}, Spi: {5}\nAtk: {6}, Def: {7}, Spd: {8}'.format(
                            player.actor.hp, player.actor.max_hp, player.name, player.actor.mental, player.actor.physical, player.actor.spiritual,
                            player.actor.atk_stat, player.actor.def_stat, player.actor.spd_stat))


    tcod.console_blit(con, 0, 0, const.get('screen_width'), const.get('screen_height'), 0, 0, 0)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(god, con, entity, fov_map):
    if entity_in_fov(god, entity, fov_map):
        tcod.console_set_default_foreground(con, entity.color)
        tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

#change this to fov_functions ??
def entity_in_fov(god, entity, fov_map):
    #**********************************************************************************
    #I have another similar func in fov_functions, they are a little different, unite them both into 1 func
    #**********************************************************************************
    if god.sight:
        return True
    elif tcod.map_is_in_fov(fov_map, entity.x, entity.y):
        return True
    else:
        return False

def clear_entity(con, entity):
    # erase the character that represents this object
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)