import tcod

from fact import Fact
from components.skill import Skill
from interface.game_messages import Message
from functions.skill import create_wall, break_wall, move_wall, teleport


class SkillForest:
    def __init__(self):
        create_wall_comp = Skill(use_function=create_wall, targeting_skill=True, targeting_type='single',
            targeting_message=Message('Select tile to make wall',tcod.cyan))
        create_wall_fact = Fact('Create Wall', 'Self explanatory', skill=create_wall_comp)

        break_wall_comp = Skill(use_function=break_wall, targeting_skill=True, targeting_type='single', 
            targeting_message=Message('Select tile to destoy wall',tcod.cyan))
        break_wall_fact = Fact('Break Wall', 'Self explanatory', skill=break_wall_comp)

        move_wall_comp = Skill(use_function=move_wall, targeting_skill=True, targeting_type='multi' ,
            targeting_message=Message('Select tile to move wall',tcod.cyan))
        move_wall_fact = Fact('Move Wall', 'Self explanatory', skill=move_wall_comp)

        teleport_comp = Skill(use_function=teleport, targeting_skill=True, targeting_type='single' ,
            targeting_message=Message('Select tile to teleport',tcod.cyan))
        teleport_fact = Fact('Teleport', 'Self explanatory', skill=teleport_comp)


        self.skills = [create_wall_fact, break_wall_fact, move_wall_fact, teleport_fact]

    def learn_skill(self, skill):
        results =[]

        if skill in self.skills:
            #I think I don't need this skill_learned part
            results.append({
                    'skill_learned': False,
                    'message': Message('You have already learned this skill.', tcod.yellow)
                    })
        else:
            results.append({
                    'skill_learned': True,
                    'message': Message(f'You have learned {skill.name}')
                })
            self.skills.append(skill)

        return results

    def use_skill(self, skill_fact, **kwargs):
        results = []

        skill_comp = skill_fact.skill

        if skill_comp.use_function is None:
            results.append({'message': Message(f'You cant use this skill', tcod.yellow)})

        else:
            if skill_comp.targeting_skill and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting_skill': skill_fact})
            else:
                kwargs = {**skill_comp.function_kwargs, **kwargs}
                skill_use_results = skill_comp.use_function(**kwargs)

                #In inventory there is an extra step that is consuming the item
                #Not really needed here, but maybe it would be nice to check if 
                #player has enough stamina/energy to do so...

                results.extend(skill_use_results)

        return results

