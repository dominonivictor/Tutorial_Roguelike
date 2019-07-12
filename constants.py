import tcod

def get_game_constants():

    const = {
        #SCREEN
        'screen_width' : 110,
        'screen_height' : 65,
        #MAP
        'map_width' : 95,
        'map_height' : 58,
        #FOV
        'fov_algorithm' : 0,
        'fov_light_walls' : True,
        'fov_radius' : 10,
        #PANEL
        'bar_width': 20,
        'panel_height': 7,

    }
    const['map_x_offset'] = 0
    const['map_y_offset'] = const['panel_height']
    const['panel_y'] = const['screen_height'] - const['panel_height']
    #MESSAGES
    const['message_x'] = const['bar_width'] + 2
    const['message_width'] = const['screen_width'] - const['bar_width'] - 2
    const['message_height'] = const['panel_height'] - 1

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