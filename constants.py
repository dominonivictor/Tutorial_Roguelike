import tcod

def get_constants():

    cons = {
        'screen_width' : 80,
        'screen_height' : 50,
        'map_width' : 75,
        'map_height' : 45,
        'max_rooms' : 30,
        'room_min_size' : 6,
        'room_max_size' : 10,
        'cross_min_size' : 2,
        'cross_max_size' : 5,
    }

    return cons

def get_colors():

    colors = {

        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150)

    }

    return colors