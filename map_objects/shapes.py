'''
    Primitive shape class where all shapes inherit from
    Putting all here for one line imports and stuff, lets see

'''
from random import randint, seed

from constants import get_room_constants


const = get_room_constants()


class Shape:

    def __init__(self, typ):
        w = randint(const[typ+'_min_size'], const[typ+'_max_size'])
        h = randint(const[typ+'_min_size'], const[typ+'_max_size'])
        r = randint(const[typ+'_min_size'], const[typ+'_max_size'])
        self.x = None
        self.y = None

    def center(self):
        return (self.x, self.y)

    def intersect(self, other):
        for tile in self.tiles:
            if tile in other.tiles:
                return True  
        else: 
            return False

'''
*******************************************************************
        RECTANGLE   RECTANGLE   RECTANGLE
*******************************************************************
'''

class Rect(Shape):
    '''
    Class that makes any kind of Rectangle in game, makes random size rooms
    text boxes?, Area of effect spells?, random scenery?
    '''


    def __init__(self, typ='rect', debug=False):  
        #random width and height depending on type
        w = randint(const[typ+'_min_size'], const[typ+'_max_size'])
        h = randint(const[typ+'_min_size'], const[typ+'_max_size'])
        #random position w/out going out of bounds, FOR ROOMS
        x0 = randint(0, const['map_width'] - w - 1)
        y0 = randint(0, const['map_height'] - h - 1)

        if debug:
            x0 = const[typ+'_min_size']
            y0 = const[typ+'_min_size']
            w = const['map_width'] - 2*const[typ+'_min_size']
            h = const['map_height'] - 2*const[typ+'_min_size']
        
        self.x1 = x0
        self.y1 = y0
        self.x2 = x0 + w
        self.y2 = y0 + h
        
        #CLEAN THIS UP,
        self.x = int((self.x1 + self.x2)/2)
        self.y = int((self.y1 + self.y2)/2)

        self.size = w * h
        self.typ = typ
        self.tiles = self.tiles_xy()

    def tiles_xy(self):
        '''
        Calculates all x, y coordinates from this Rectangle'
        '''
        tiles = []
        for x in range(self.x1 + 1, self.x2):
            for y in range(self.y1 + 1, self.y2):
                tiles.append((x, y))

        return tiles

    #make noise method, basicaly repopulate the blank rect with stuff (removing tiles)

'''
*******************************************************************
        CROSS   CROSS   CROSS   CROSS
*******************************************************************
'''

class Cross(Shape):

    def __init__(self, typ='cross'):
        
        r = randint(const[typ+'_min_size'], const[typ+'_max_size'])
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

'''
*******************************************************************
        ELLIPSE     ELLIPSE     ELLIPSE     ELLIPSE     ELLIPSE     
*******************************************************************
'''

class Ellipse(Shape):

    def __init__(self, typ='ellipse'):
        w = randint(const[typ+'_min_size'], const[typ+'_max_size'])
        h = randint(const[typ+'_min_size'], const[typ+'_max_size'])
        x = randint(w+1, const['map_width'] - w - 2)
        y = randint(h+1, const['map_height'] - h - 2)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.tiles = self.tiles_xy()

    def tiles_xy(self):
        tiles = []
        w = self.w
        h = self.h
        for y in range(-h, h+1):
            for x in range(-w, w+1):
                if(x**2*h**2 + y**2*w**2 <= h**2*w**2):
                    tiles.append((self.x+x, self.y+y))

        return tiles