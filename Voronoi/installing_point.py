class InstallingPoint:
    def __init__(self, x, y, width, length):
        self.width = width
        self.length = length
        self.x = x
        self.y = y

    def distance_to_origin(self):
        if self.y == 0:
            return self.x
        elif self.y == self.length:
            return 2 * self.width - self.x + self.length
        elif self.x == 0:
            return 2 * self.width + 2 * self.length - self.y
        else:
            return self.width + self.y

    def compare(self, another):
        return self.distance_to_origin() < another.distance_to_origin()

    def to_list(self):
        return [self.x, self.y]

    def intersect_point(self, another):
        x = (self.x + another.x) / 2
        y = (self.y + another.y) / 2
        if x == 0 or x == self.width:
            return [[0, y], [self.width, y]]
        elif y == 0 or y == self.length:
            return [[x, 0], [x, self.length]]

        grad = (self.x - another.x) / (another.y - self.y)
        intersect = y - grad * x

        res = []
        if self.length >= intersect >= 0 :
            res.append([0, intersect])
        y = grad * self.width + intersect
        if self.length >= y >= 0 :
            res.append([self.width, y])
        x_1 = -intersect / grad
        if self.width >= x_1 >= 0:
            res.append([x_1, 0])
        x_2 = (self.length-intersect) / grad
        if self.width >= x_2 >= 0:
            res.append([x_2, 0])
        return res

