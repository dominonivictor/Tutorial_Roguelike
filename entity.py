

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        '''
        Move the entity by a given amount given the x and y variations 
        (final x (or y) - initial x (or y))
        '''
        self.x += dx
        self.y += dy 