class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    has a destroy_wall meth. and in a near future implement transform_terrain
    """
    def __init__(self, blocked, block_sight=None, tile_element='earth', wind=None):
        self.blocked = blocked
        #This piece of code I'm not so sure if I agree with, analyse this further***
        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        
        self.block_sight = block_sight
        self.explored = False
        self.tile_element = tile_element
        #maybe implement as a string ex: wind = 'NE10' -> Northeast wind with spd 10,
        #catch data using regex? or if I do it like wind[0:2] for direction and wind[2:] for spd
        self.wind = wind

    def destroy_wall(self):
        self.blocked = False
        self.block_sight = False

'''
    def transform_terrain(self, new_element):
        self.tile_element = new_element
        pass
'''
    