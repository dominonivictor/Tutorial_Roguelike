
class God:
    
    def __init__(self):
        default = False
        self.tog = default
        self.sight = self.tog


    def toggle(self):
        self.tog = not self.tog
        self.sight = self.tog
        self.invunerability = self.tog
