


class Skill:
    def __init__(self, use_function=None, targeting_skill=None, targeting_message=None, targeting_type=None, original_x=None, original_y=None,
                **kwargs):
        self.use_function = use_function
        self.targeting_skill = targeting_skill
        self.targeting_message = targeting_message
        self.targeting_type = targeting_type
        self.original_x = original_x
        self.original_y = original_y
        self.function_kwargs = kwargs