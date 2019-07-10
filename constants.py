import tcod

def get_game_constants():

    cons = {
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
    cons['panel_y'] = cons['screen_height'] - cons['panel_height']
    #MESSAGES
    cons['message_x'] = cons['bar_width'] + 2
    cons['message_width'] = cons['screen_width'] - cons['bar_width'] - 2
    cons['message_height'] = cons['panel_height'] - 1

    return cons

def get_room_constants():

    cons = {
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

    return cons

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
        'player':{'spiritual':5, 'mental': 5, 'physical': 5}

    }

    return stats