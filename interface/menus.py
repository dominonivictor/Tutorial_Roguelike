import tcod
from constants import get_game_constants

const = get_game_constants()

def menu(con, header, options, width, max_capacity=3):
    if len(options) > max_capacity: raise ValueError('No more than 3.')

    #Calculate total height for header
    header_height = tcod.console_get_height_rect(con, 0, 0, width, const['screen_height'], header)
    height = len(options) + header_height

    #create an offscreen console that represents the menu's window
    window = tcod.console_new(width, height)

    #print header, with autowrap
    tcod.console_set_default_foreground(window, tcod.white)
    tcod.console_print_rect_ex(window, 0, 0, width, height, tcod.BKGND_NONE, tcod.LEFT, header)

    #print all options
    y = header_height
    num_index = 1
    for option_text in options:
        text = '('+str(num_index)+')' + option_text
        tcod.console_print_ex(window, 0, y, tcod.BKGND_NONE, tcod.LEFT, text)
        y += 1
        num_index += 1

    #blit the contents of 'window' to the root console
    x = int(const['screen_width']/2 - width/2)
    y = int(const['screen_height']/2 - height/2)
    tcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

def inventory_menu(con, header, inventory, inventory_width):
    #show a menu with each item of the inventory as an option
    if len(inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in inventory.items]

    menu(con, header, options, inventory_width)