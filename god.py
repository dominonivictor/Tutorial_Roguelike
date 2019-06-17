
class God:
    
    def __init__(self):
        default = False
        self.tog = default
        self.sight = self.tog


    def toggle(self):
        if self.tog:
            self.sight = False
            self.tog = False

        else:
            self.sight = True
            self.tog = True
