

class Fact:
    '''
    Any piece of knowledge, describing untageable things
    '''
    def __init__(self, name, text, **kwargs):
        
        self.name = name
        self.text = text
        self.skill = kwargs.get('skill')