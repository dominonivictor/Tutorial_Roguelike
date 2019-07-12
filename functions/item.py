import tcod

from interface.game_messages import Message
from components.ai import ConfusedMonster

def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.actor.hp == entity.actor.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health', tcod.yellow)})
    else:
        entity.actor.heal(amount)
        results.append({'consumed': True, 'message': Message('Your wounds are healing.', tcod.green)})

    return results

def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results =[]

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.actor and entity != caster and tcod.map_is_in_fov(fov_map, entity.x,entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                clostest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target, 'message':Message(f'Pikachu use THUNDERBOLT! Deals {damage} to {target.name}', tcod.blue)})
        results.extend(target.actor.take_dmg(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('No enemies in range.', tcod.red)})

    return results

def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('Out of range!', tcod.yellow)})
        return results

    results.append({'consumed': True, 'message': Message(f'BOOM, burns a {radius}x{radius} area.', tcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.actor:
            results.append({'message': Message(f'The {entity.name} is burned for {damage} hitpoints', tcod.red)})
            results.extend(entity.actor.take_dmg(damage))

    return results

def cast_confuse(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('Out of range!', tcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 5)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message(f'{entity.name} is confused', tcod.light_green)})

            break

    else:
        results.append({'consumed': False, 'message': Message('There is no targetable creature in this tile', tcod.yellow)})

    return results