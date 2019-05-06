from map_objects.tile import Tile


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]
        
        tiles[30][22].blocked = True
        tiles[30][22].block_sight = True
        tiles[31][22].blocked = True
        tiles[31][22].block_sight = True
        tiles[32][22].blocked = True
        tiles[32][22].block_sight = True
        
        for x in range(30, 36):
            tiles[x][x].blocked = True
            tiles[x][x].block_sight = True
        for x in range(35, 41):
            tiles[x][(70-x)].blocked = True
            tiles[x][(70-x)].block_sight = True    
            
        tiles[30+5][22].blocked = True
        tiles[30+5][22].block_sight = True
        tiles[31+5][22].blocked = True
        tiles[31+5][22].block_sight = True
        tiles[32+5][22].blocked = True
        tiles[32+5][22].block_sight = True
        
        return tiles
        
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
            
        return False