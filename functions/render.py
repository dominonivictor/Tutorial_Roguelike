import tcod
from enum import Enum
from constants import get_game_constants, get_colors
from game_states import GameStates
from interface.menus import inventory_menu, skills_menu
from datetime import time, datetime
import textwrap

'''
if you somehow adjust the gui you might need to adjust that single function with new offset
but just there
you need a small function to convert mouse_x,mouse_y to map_x,map_y and use it for targeting, spells, wheree


You subtract the mouse position by the offset.  This gets you the position on the map.

This type of conversion is already being done by libtcod to get the screen tile from the mouse pixel.  You just need to add your own layer to get the map tile from the screen tile.
If your map needs to scroll then you'd add the camera position as well, even if the offset was still 0,0.


Layer is more of a programming term.  "SDL (layer)" -> "screen pixel" -> "libtcod (layer)" -> "screen tile" -> "your code (layer)" -> "map tile".
'''
const = get_game_constants()
colors = get_colors()

class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

def get_mouse_xy(mouse, offset=True):
    if offset:
        return (mouse.cx - const['map_x_offset'] , mouse.cy - const['map_y_offset'])
    else:
        return (mouse.cx, mouse.cy)
        
def get_entities_under_mouse(god, mouse, entities, fov_map):
    (x, y) = (get_mouse_xy(mouse))

    entities_under_mouse = [entity for entity in entities
                            if entity.x == x and entity.y == y and (tcod.map_is_in_fov(fov_map, x, y) or god.sight)]
    return entities_under_mouse 

def get_tile_under_mouse(god, mouse, game_map, fov_map):
    (x, y) = get_mouse_xy(mouse)

    tile = game_map.tiles[x][y]

    return tile

def get_names_under_mouse(god, mouse, entities, fov_map):
    names = [entity.name for entity in get_entities_under_mouse(god, mouse, entities, fov_map)]

    names = ', '.join(names)

    return names.capitalize()


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value)/maximum*total_width)

    tcod.console_set_default_background(panel, back_color)
    tcod.console_rect(panel, x, y, total_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        tcod.console_rect(panel, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_foreground(panel, tcod.white)
    tcod.console_print_ex(panel, int(x + total_width/2), y, tcod.BKGND_NONE, tcod.CENTER, 
                        f'{name}: {value}/{maximum}')

def render_all(god, con, panel, sidebar, entities, player, game_map, fov_map, fov_recompute, msg_log, mouse, game_state):
    ''' 
    Draw all the tiles and entities in the game map, taking the console, all entities, game_map, screen vars and colors as input
    Starting to draw stats on the screen! Think carefully about this and change stuff acordingly, probably move the UI part into another file
    '''
    zeit = datetime.now()
    if game_state == GameStates.TARGETING_MODE:
        blink=True
    else:
        blink=False
    if fov_recompute:
        for y in range(const['map_height']):
            for x in range(const['map_width']):
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
                        tcod.console_set_char_background(con, x, y, colors['dark_wall'], tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, colors['dark_ground'], tcod.BKGND_SET)

                else:# if god mode is turned off, it will make all non explored stuff turn black again
                    tcod.console_set_char_background(con, x, y, colors['black'], tcod.BKGND_SET)
    
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(god, con, entity, fov_map)

    '''
    ############## BLINKING SHENANIGANS WHEN TARGETING
    '''

    mouse_x, mouse_y = get_mouse_xy(mouse)
    if blink and round(zeit.microsecond/900000): #this just gets it every half secondish
        tcod.console_set_char_background(con, mouse_x, mouse_y, colors.get('blink'), tcod.BKGND_SET)
                    
    ############# Bliting the Main Console

    tcod.console_blit(con, 0, 0, const['screen_width'], const['screen_height'], 0, 0, const['panel_height'])


    ######################## PANEL  ############################3

    tcod.console_set_default_background(panel, tcod.black)
    tcod.console_clear(panel)

    #print the game msgs, one line at a time, at the apropriate x, and y (message_x and y)
    y = 1
    for msg in msg_log.msgs:
        tcod.console_set_default_foreground(panel, msg.color)
        tcod.console_print_ex(panel, msg_log.x, y, tcod.BKGND_NONE, tcod.LEFT, msg.text)
        y+=1

    #renders hp bar
    render_bar(panel, 1, 1, const['bar_width'], 'HP', player.actor.hp, player.actor.max_hp, 
                tcod.light_red, tcod.darker_red)  

    #prints names under mouse
    tcod.console_set_default_foreground(panel, tcod.light_gray)
    tcod.console_print_ex(panel, 1, 0, tcod.BKGND_NONE, tcod.LEFT,
                            get_names_under_mouse(god, mouse, entities, fov_map))
    
    #Prints info on the player
    player = entities[0]
    '''
    tcod.console_print_ex(panel, 1, 3, tcod.BKGND_NONE, tcod.LEFT,
                            f'SPI = {player.actor.spiritual} DEF = {player.actor.def_stat}')
    tcod.console_print_ex(panel, 1, 4, tcod.BKGND_NONE, tcod.LEFT,
                            f'PHY = {player.actor.physical} SPD = {player.actor.spd_stat}')
    tcod.console_print_ex(panel, 1, 5, tcod.BKGND_NONE, tcod.LEFT,
                            f'MEN = {player.actor.mental} ATK = {player.actor.atk_stat}')
    '''
    
    tcod.console_blit(panel, 0, 0, const['screen_width'], const['panel_height'], 0, 0, 0)

    ############################## SIDEBAR ##################################3

    tcod.console_set_default_background(sidebar, tcod.grey)
    tcod.console_clear(sidebar)

    y = 1    
    tcod.console_set_default_foreground(sidebar, tcod.yellow)
    for skill in player.knowledge.skill_forest.skills:
        tcod.console_print_ex(sidebar, 0, y, tcod.BKGND_NONE, tcod.LEFT, skill.name)
        y += 2

    tcod.console_blit(sidebar, 0, 0, const['sidebar_width'], const['sidebar_height'], 0, const['sidebar_x'], const['sidebar_y'])




    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        elif game_state == GameStates.DROP_INVENTORY:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'
        inventory_menu(con, inventory_title, player.inventory, 50)



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
    #I have another similar func in fov_functions, they are a little different, unite them both into 1 func??
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
'''
def draw_text():
    tcod.console_print_ex(con, 5 , const['map_height']- 8, tcod.BKGND_NONE, tcod.LEFT,
                            'HP: {0:02}/{1:02}\nName: {2}\nMen: {3}, Phy: {4}, Spi: {5}\nAtk: {6}, Def: {7}, Spd: {8}'.format(
                            player.actor.hp, player.actor.max_hp, player.name, player.actor.mental, player.actor.physical, player.actor.spiritual,
                            player.actor.atk_stat, player.actor.def_stat, player.actor.spd_stat
'''
