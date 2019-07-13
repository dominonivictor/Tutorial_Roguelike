import tcod

from interface.game_messages import Message

def get_game_constants():

    screen_width = 110
    screen_height = 65
    #MAP
    map_width = 95
    map_height = 58
    #FOV
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    #PANEL
    bar_width= 20
    panel_height= 7
    panel_y = screen_height - panel_height
    #SIDEBAR
    sidebar_width = screen_width - map_width
    sidebar_height = screen_height - panel_height
    sidebar_x = map_width + 1
    sidebar_y = panel_height + 1

    #MESSAGES
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    #Offset for getting mouse input
    map_x_offset = 0
    map_y_offset = panel_height

    const = {
        #SCREEN
        'screen_width': screen_width,
        'screen_height': screen_height,
        #MAP
        'map_width': map_width,
        'map_height': map_height,
        'map_x_offset': map_x_offset,
        'map_y_offset': map_y_offset,
        #FOV
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        #PANEL
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        #SIDEBAR
        'sidebar_width': sidebar_width,
        'sidebar_height': sidebar_height,
        'sidebar_x': sidebar_x,
        'sidebar_y': sidebar_y,
        #MESSAGES
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
    }

    return const

gconst = get_game_constants()

def get_room_constants():

    const = {
        'max_rooms' : 30, 
        'max_monsters_per_room' : 4,
        'max_items_per_room': 5,  
        'rect_min_size' : 2,
        'rect_max_size' : 4,
        'cross_min_size' : 2,
        'cross_max_size' : 5,
        'ellipse_min_size' : 2,
        'ellipse_max_size' : 6,

        #****************************************************
        #A little repetitive, but I'll work something better
        #DONT FORGET THIS SHIT, OR LEARN TO JOIN DICTS
        #****************************************************

        'map_width' : gconst['map_width'],
        'map_height' : gconst['map_height'],
    }

    return const

def get_colors():

    colors = {

        'blink': tcod.Color(255, 71, 243),

        'dark_wall': tcod.Color(66, 47, 32),
        'dark_ground': tcod.Color(110, 78, 54),
        'light_wall' : tcod.Color(156, 97, 26), #darker orange
        'light_ground' : tcod.Color(245, 164, 66), #light orange
        'black' : tcod.Color(0, 0, 0),

        #CREAtURES
        'player': tcod.Color(28, 43, 140),
        'bandit' : tcod.Color(66, 139, 255),
        'troll' : tcod.darker_green,
        'fox' : tcod.orange,

    }

    return colors

def get_actors_stats():

    stats = {
        'player':{'spiritual': 10, 'mental': 5, 'physical': 5}

    }

    return stats

def get_item_parameters():

    parameters = {

    'heal': {'amount': 4},
    'lightning': {'damage': 20, 'maximum_range': 5},
    'fireball': {'targeting': True, 'damage': 12, 'radius': 3,
                'targeting_message': Message('Left-click a tile to cast a 3x3 fireball, or right-click to cancel', tcod.cyan)},
    'confusion': {'targeting': True, 
                'targeting_message':Message('Left-click a Creature to cast Confusion, or right-click to cancel', tcod.cyan)},
    }

    return parameters