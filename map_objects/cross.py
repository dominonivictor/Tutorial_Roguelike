from random import randint
from constants import get_constants

const = get_constants()

class Cross():
    def __init__(self, typ):
        r = randint(const['cross_min_size'], const['cross_max_size'])
        x = randint(r, const['map_width'] - r - 1)
        y = randint(r, const['map_height'] - r - 1)

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

    def center(self):
        return (self.x, self.y)

    def intersect(self, other):
        '''
        Given another room, returns True if they intersect
        '''
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)        

    