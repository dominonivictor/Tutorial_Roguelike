import tcod

from interface.game_messages import Message
from game_states import GameStates
from functions.render import RenderOrder

def kill_player(player):
    player.char = '%'
    player.color = tcod.dark_red

    return Message('You died!', tcod.red), GameStates.PLAYER_DEAD

def kill_creature(creature):
    death_message = Message(f'{creature.name.capitalize()} is dead!', tcod.orange)

    creature.char = '%'
    creature.color = tcod.dark_red
    creature.blocks = False

    creature.actor = None
    creature.ai = None
    creature.name = 'remains of ' + creature.name
    creature.render_order = RenderOrder.CORPSE

    return death_message