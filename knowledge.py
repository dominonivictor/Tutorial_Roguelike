from components.skill_forest import SkillForest


class Knowledge:
    '''
    A generic object to represent knowledge of skills, events, maps, etc
    '''
    def __init__(self, **kwargs):
        self.skill_forest = SkillForest()