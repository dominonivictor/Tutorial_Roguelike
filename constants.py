import tcod

def get_game_constants():

    cons = {
        'screen_width' : 80,
        'screen_height' : 50,
        'map_width' : 75,
        'map_height' : 45,
        'fov_algorithm' : 0,
        'fov_light_walls' : True,
        'fov_radius' : 10,
            
    }

    return cons

def get_room_constants():

    cons = {
        'max_rooms' : 30, 
        'max_monsters_per_room' : 4,  
        'rect_min_size' : 2,
        'rect_max_size' : 6,
        'cross_min_size' : 2,
        'cross_max_size' : 6,
        'ellipse_min_size' : 2,
        'ellipse_max_size' : 8,

        #****************************************************
        #A little repetitive, but I'll work something better
        #DONT FORGET THIS SHIT, OR LEARN TO JOIN DICTS
        #****************************************************

        'map_width' : 75,
        'map_height' : 45,
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

def get_creatures_stats():

    stats = {
        'fox':{'hp':20},

    }

    return stats