import math


class DirectionalAntenna:
    def __init__(self, x, y, radius, detect_angle, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.detect_angle = detect_angle
        if direction < 0:
            direction = 2 * math.pi + direction
        self.direction = direction
        self.covered_num = 0
        self.intersected_num = 0

    def in_range(self, x, y):
        dx = x - self.x
        dy = y - self.y
        distance = dx * dx + dy * dy
        distance = math.pow(distance, 1 / 2)
        if distance > self.radius:
            return False
        if dx == 0:
            if dy > 0:
                angle = math.pi / 2
            elif dy == 0:
                angle = self.direction
            else:
                angle = 3 * math.pi / 2
        elif dy == 0:
            if dx > 0:
                angle = 0
            else:
                angle = math.pi
        else:
            angle = math.atan(dy / dx)
            if angle < 0 and dy < 0:
                angle = angle + 2 * math.pi
            elif angle < 0 < dy:
                angle = angle + math.pi
            elif angle > 0 > dx:
                angle = angle + math.pi

        d_angle = angle - self.direction
        if d_angle < -math.pi:
            d_angle += 2 * math.pi
        elif d_angle > math.pi:
            d_angle -= 2 * math.pi

        return -self.detect_angle / 2 <= d_angle <= self.detect_angle / 2

    def compare(self, another):
        if self.x < another.x:
            return True
        elif self.x == another.x:
            return self.y < another.y
        return False

    def copy(self):
        res = DirectionalAntenna(self.x, self.y, self.radius, self.detect_angle, self.direction)
        return res
