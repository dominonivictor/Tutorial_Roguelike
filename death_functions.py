import tcod

from game_states import GameStates
from render_functions import RenderOrder

def kill_player(player):
    player.char = '%'
    player.color = tcod.dark_red

    return 'You died!', GameStates.PLAYER_DEAD

def kill_creature(creature):
    death_message = '{} is dead!'.format(creature.name.capitalize())

    creature.char = '%'
    creature.color = tcod.dark_red
    creature.blocks = False

    creature.actor = None
    creature.ai = None
    creature.name = 'remains of ' + creature.name
    creature.render_order = RenderOrder.CORPSE

    return death_message