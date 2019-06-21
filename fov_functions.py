import tcod

def initialize_fov(game_map):
    '''
        need to re-set properties when breaking walls
        actually need to rethink this whole function, because i need a fov map
        that is variable, depending on current tile status, not compute all at the start
        need to study more! 
    '''
    fov_map = tcod.map_new(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            tcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight,
                                    not game_map.tiles[x][y].blocked)

    return fov_map

def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    tcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)

def set_tile_fov(x, y, game_map, fov_map):

    tcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight,
                                    not game_map.tiles[x][y].blocked)
    return fov_map

def get_entities_in_fov(fov_map, entities):
    #**********************************************************************************
    #I have a duplicate function in render functions, delete this or that one!!!!!!!
    #**********************************************************************************
    results = []
    for entity in entities:
        if tcod.map_is_in_fov(fov_map, entity.x, entity.y):
            results.append(entity)

    return results
