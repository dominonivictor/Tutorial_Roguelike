

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, dx, dy):
        '''
        Move the entity by a given amount given the x and y variations 
        (final x (or y) - initial x (or y))
        '''
        self.x += dx
        self.y += dy 

def get_blocking_entity(entities, coord_x, coord_y):
    '''
    Given the entities array, and a tile (x, y coordinates), returns a blocking entity
    at that location, else it returns None
    '''
    for entity in entities:
        if entity.blocks and entity.x == coord_x and entity.y == coord_y:
            return entity

    return None