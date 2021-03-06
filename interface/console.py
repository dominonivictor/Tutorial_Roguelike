import tcod
from functions.render import render_all, clear_all
from constants import get_game_constants

const = get_game_constants()

'''
    maybe make a class to handle this? I think its nice...
'''
class Console:
    def __init__(self):
        self.console = self.console_init()
    
    def console_init(self):
        tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

        tcod.console_init_root(const['screen_width'], const['screen_height'], 'Project Tesla', False)

        con = tcod.console_new(const['screen_width'], const['screen_height'])

        return con

def render_console(con, panel, sidebar, god, player, entities, game_map, fov_map, fov_recompute, msg_log, mouse, game_state):
    render_all(god, con, panel, sidebar, entities, player, game_map, fov_map, fov_recompute, msg_log, mouse, game_state)

    tcod.console_flush()

    clear_all(con, entities)

class Panel:
    def __init__(self):
        self.panel = self.panel_init()

    def panel_init(self):
        panel = tcod.console_new(const['screen_width'], const['panel_height'])
        
        return panel

class Sidebar:
    def __init__(self):
        self.sidebar = self.sidebar_init()

    def sidebar_init(self):
        sidebar = tcod.console_new(const['sidebar_width'], const['sidebar_height'])
        
        return sidebar