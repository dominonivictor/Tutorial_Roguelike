class Cross():
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.size = 1 + 4*r

    for x in range(-r, r + 1):
        for y in range(-r, r + 1):
            xysum = x+y
            if (xysum <= r):
                return False