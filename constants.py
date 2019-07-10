import tcod

def get_game_constants():

    const = {
        #SCREEN
        'screen_width' : 80,
        'screen_height' : 50,
        #MAP
        'map_width' : 80,
        'map_height' : 43,
        #FOV
        'fov_algorithm' : 0,
        'fov_light_walls' : True,
        'fov_radius' : 10,
        #PANEL
        'bar_width': 20,
        'panel_height': 7,

    }
    const['panel_y'] = const['screen_height'] - const['panel_height']
    #MESSAGES
    const['message_x'] = const['bar_width'] + 2
    const['message_width'] = const['screen_width'] - const['bar_width'] - 2
    const['message_height'] = const['panel_height'] - 1

    return const

def get_room_constants():

    const = {
        'max_rooms' : 30, 
        'max_monsters_per_room' : 4,  
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

        'map_width' : 80,
        'map_height' : 43,
    }

    return const

def get_colors():

    colors = {

        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150),
        'light_wall' : tcod.Color(130, 110, 50),
        'light_ground' : tcod.Color(200, 180, 50),
        'black' : tcod.Color(0, 0, 0),

        #CREAtURES
        'orc' : tcod.desaturated_green,
        'troll' : tcod.darker_green,
        'fox' : tcod.orange,

    }

    return colors

def get_actors_stats():

    stats = {
        'player':{'spiritual':10, 'mental': 10, 'physical': 10}

    }

    return stats