
class Actor:
    '''
        For now a pretty straight forward class, in a near future this shall have also specific skills (prob. separated in a specific file)
    '''
    def __init__(self, mental, physical, spiritual):
        '''
        Each contributes to 1 or 2 basic atributes and lower another
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

    def attack_target(self, target):
        results = []

        dmg = self.atk_stat - target.actor.def_stat

        if dmg > 0:
            results.append({'message': '{} attacks {} for {} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(dmg))})
            results.extend(target.actor.take_dmg(dmg))
        else:
            results.append({'message': '{} attacks {} but deals no damage.'.format(
                self.owner.name.capitalize(), target.name )})

        return results