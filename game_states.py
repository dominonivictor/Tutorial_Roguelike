'''
    Learn this deeply, want to modify to fit a spd/turn system
    study how others do it and try to implement it :)
'''

from enum import Enum


class GameStates(Enum):
    PLAYERS_TURN = 1
    TARGETING_MODE = 2
    ENEMY_TURN = 3
    PLAYER_DEAD = 4