from random import randint
from constants import get_game_constants

const = get_game_constants()

class Cross():
    def __init__(self, typ):
        r = randint(const['cross_min_size'], const['cross_max_size'])
        x = randint(r+1, const['map_width'] - r - 2)
        y = randint(r+1, const['map_height'] - r - 2)

        self.x = x
        self.y = y
        self.r = r

        #thinking like a rect
        self.x1 = x - r
        self.y1 = y - r
        self.x2 = x + r
        self.y2 = y + r

        self.size = 1 + 4*r
        self.typ = typ
        self.tiles = self.tiles_xy()

    def center(self):
        return (self.x, self.y)

    def intersect(self, other):
        '''
        Given another room, returns True if they intersect
        '''
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)        

    def tiles_xy(self):
        tiles = []
        for x in range(self.x1 , self.x2 + 1):
                for y in range(self.y1 , self.y2 + 1):
                    rel_x = x - self.x
                    rel_y = y - self.y
                    xysum = abs(rel_x) + abs(rel_y)
                    if (xysum <= self.r ):    
                        tiles.append((x, y))

        return tiles