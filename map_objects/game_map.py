from random import randint, seed, choice
from map_objects.tile import Tile
from map_objects.shapes import Rect, Cross, Ellipse
from constants import get_room_constants, get_colors
from entity import Entity


const = get_room_constants()
colors = get_colors()

class GameMap:
    '''
    Class that draws a map for the game to be played, Places each entity (monsters, items) on the map
    as it's generated... 
    Future Plans:
    - Different generators for different regions
        - including map layout
        - items/monsters/scenery spawn
        - include more data? 
    '''
    def __init__(self, width, height, region='desert'):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.region = region

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        
        return tiles

    def make_map(self, player, entities, debug_map=False):
        '''
        Creates the whole map, first placing rooms, then connecting them
        '''
        #seed(0)
        if debug_map:
            new_room=Rect(debug=True)
            self.create_room(new_room)

        else:
            rooms = []
            num_rooms = 0
            intersecc = False

            for r in range(const.get('max_rooms')):
                #"Rect" class makes it easier to work with
                num = randint(0,6)
                if(num==0):
                    new_room = Rect()
                elif num == 1:
                    new_room = Cross()
                else:
                    new_room = Ellipse()
                #run through the other rooms, and see if they intersect
                for other_room in rooms:
                    if new_room.intersect(other_room):
                        if (randint(0,1)==1 and intersecc):#50/50 for joining intersecting rooms
                            continue
                        else:
                            break
                else:
                    #This means no intersections, so we are free to make the room
                    #First "paint" it to the map's tiles
                    self.create_room(new_room)
                    (new_x, new_y) = new_room.center()
                    if num_rooms == 0:
                        #This is our first room
                        player.x = new_x
                        player.y = new_y
                    else:
                    #all rooms after the first, connect it to the previous room using a tunnel
                        #center coonates from previous room
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        #choice 0 or 1
                        if randint(0, 1) == 1:
                            #first move horizontally then vertically
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)

                    self.place_entities(new_room, entities)

                    #Finally, append new room to the list
                    rooms.append(new_room)
                    num_rooms += 1

    def create_room(self, room):
        '''
        Takes the room parameter and digs out the space for the room
        '''
        for x, y in room.tiles:        
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False



    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities):
        '''
            Takes a room and the list of entities and puts monsters inside the room
            where there isn't any other entity at that square. Since it is here were
            the monster gen is, i'll either build upon the stuff here or migrate elsewher
            to make it more sofisticated, making specific "mobs" for diferent regions
            and different items placed depending on stuff
        '''
        num_monsters = randint(0, const['max_monsters_per_room'])

        for i in range(num_monsters):
            #random location in room
            choicez = choice(room.tiles)
            x = choicez[0]
            y = choicez[1]

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    monster = Entity(x, y, 'o', colors['orc'], 'Orc', blocks=True)
                else:
                    monster = Entity(x, y, 'T', colors['troll'], 'Troll', blocks=True)

                entities.append(monster)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
            
        return False