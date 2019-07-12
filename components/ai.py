import tcod
from random import randint
from interface.game_messages import Message

class BasicCreature:
    '''
    ok big plans for this class, acording to Caves of Qud creators, the thing is to make
    a bunch of "purpose" components that makes the creatures do things according to their characteristics
    For my project I believe that inside these components there will be even further restrictions according 
    to character allignments, background, personality, etc
    '''
    def take_turn(self, target, fov_map, game_map, entities):
        results = []
        creature = self.owner

        if tcod.map_is_in_fov(fov_map, creature.x, creature.y):
            if creature.distance_to(target) >= 2:
                creature.move_astar(target, entities, game_map)

            elif target.actor.hp > 0:
                attack_results = creature.actor.attack_target(target)
                results.extend(attack_results)

        return results

class ConfusedMonster:
    def __init__(self, prev_ai, turns_left=3):
        self.prev_ai = prev_ai
        self.turns_left = turns_left

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        if self.turns_left >0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.turns_left -=1

        else:
            self.owner.ai = self.prev_ai
            results.append({'message': Message(f'The {self.owner.name} is no longer confused', tcod.red)})

        return results

