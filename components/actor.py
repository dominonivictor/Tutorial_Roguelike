import tcod
from interface.game_messages import Message


class Actor:
    '''
        For now a pretty straight forward class, in a near future this shall have also specific skills (prob. separated in a specific file)
    '''
    def __init__(self, mental, physical, spiritual):
        '''
        Each parameter/aspect contributes to 1 or 2 basic stat and lowers another
        '''
        hp = int(mental*0.5) + int(physical*1.2) + int(spiritual*0.9)
        self.max_hp = int(mental*0.5) + int(physical*1.2) + int(spiritual*0.9)
        self.hp = hp
        self.mental = mental
        self.physical = physical
        self.spiritual = spiritual
        self.atk_stat = int(mental*1) + int(physical*1) - int(spiritual*0.5)
        self.def_stat = int(mental*1) - int(physical*0.5) + int(spiritual*1)
        self.spd_stat = - int(mental*0.5) + int(physical*1) + int(spiritual*1)

    def take_dmg(self, value):
        results = []

        self.hp -= value

        if self.hp <= 0:
            results.append({'dead': self.owner})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack_target(self, target):
        results = []

        dmg = self.atk_stat - target.actor.def_stat

        name = self.owner.name.capitalize()

        if dmg > 0:
            results.append({'message': Message(f'{name} attacks {target.name} for {str(dmg)} hit points.', tcod.white)})
            results.extend(target.actor.take_dmg(dmg))
        else:
            results.append({'message': Message(f'{name} attacks {target.name} but deals no damage.', tcod.white)})

        return results