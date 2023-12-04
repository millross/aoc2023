class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_adjacent(self, other):
        x_diff = abs(self.x - other.x)
        y_diff = abs(self.y - other.y)
        return x_diff < 2 and y_diff < 2 and (not(x_diff == 0) and (y_diff ==0))
    
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    
    def __repr__(self):
        return str(self)
