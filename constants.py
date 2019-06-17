import tcod

def get_game_constants():

    cons = {
        'screen_width' : 80,
        'screen_height' : 50,
        'map_width' : 75,
        'map_height' : 45,
        'max_rooms' : 50,
        'room_min_size' : 6,
        'room_max_size' : 10,
        'cross_min_size' : 2,
        'cross_max_size' : 5,
        'fov_algorithm' : 0,
        'fov_light_walls' : True,
        'fov_radius' : 10
        
    
    }

    return cons

def get_colors():

    colors = {

        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150),
        'light_wall' : tcod.Color(130, 110, 50),
        'light_ground' : tcod.Color(200, 180, 50),
        'black' : tcod.Color(0, 0, 0),

    }

    return colors

#Actually this is in the wrong place, it should be somewhere u can toggle
#ergo it is no a constant, but for now we'll temporarily work like this
'''
def get_god_constants():

    cons = {
        'god_sight' : True

    }

    return cons
'''