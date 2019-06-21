import tcod


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