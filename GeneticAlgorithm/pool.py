import numpy as np


class Pool:
    def __init__(self, width, length, pool_width, pool_length):
        self.width = width
        self.length = length
        self.pool_width = pool_width
        self.pool_length = pool_length

    def get_range(self, idx):
        half_d_width = (self.width - self.pool_width) / 2
        half_d_length = (self.length - self.pool_length) / 2
        if idx == 0:
            return 0, half_d_width, 0, half_d_length
        elif idx == 1:
            return half_d_width, half_d_width + self.pool_width, 0, half_d_length
        elif idx == 2:
            return half_d_width + self.pool_width, self.width, 0, half_d_length
        elif idx == 3:
            return half_d_width + self.pool_width, self.width, half_d_length, half_d_length + self.pool_length
        elif idx == 4:
            return half_d_width + self.pool_width, self.width, half_d_length + self.pool_length, self.length
        elif idx == 5:
            return half_d_width, half_d_width + self.pool_width, half_d_length + self.pool_length, self.length
        elif idx == 6:
            return 0, half_d_width, half_d_length + self.pool_length, self.length
        elif idx == 7:
            return 0, half_d_width, half_d_length, half_d_length + self.pool_length
        else:
            raise Exception("Idx should be an integer between 0 and 7")

    def get_pool_range(self):
        half_d_width = (self.width - self.pool_width) / 2
        half_d_length = (self.length - self.pool_length) / 2
        return half_d_width, half_d_width + self.pool_width, half_d_length, half_d_length + self.pool_length

    def get_area_of_different_part(self):
        half_d_width = (self.width - self.pool_width) / 2
        half_d_length = (self.length - self.pool_length) / 2
        area_0 = half_d_length * half_d_length
        area_1 = half_d_length * self.pool_width / 2
        area_2 = half_d_width * self.pool_length / 2
        return [area_0, area_1, area_2]

    def get_quarter_range(self, idx):
        half_d_width = (self.width - self.pool_width) / 2
        half_d_length = (self.length - self.pool_length) / 2
        if idx == 0:
            return 0, half_d_width, 0, half_d_length
        elif idx == 1:
            return half_d_width, half_d_width + self.pool_width / 2, 0, half_d_length
        elif idx == 2:
            return 0, half_d_width, half_d_length, half_d_length + self.pool_length / 2
        else:
            raise Exception("Idx should be an integer between 0 and 2!")

    def distance_to_edge(self, x, y):
        half_d_width = (self.width - self.pool_width) / 2
        half_d_length = (self.length - self.pool_length) / 2
        d1 = x - half_d_width
        d2 = half_d_width + self.pool_width - x
        d3 = y - half_d_length
        d4 = half_d_length + self.pool_length - y
        res = np.max([d1, d2, d3, d4])
        return res

    def point_in_first_range(self, x, y):
        half_d_width = (self.width - self.pool_width) / 2
        half_d_length = (self.length - self.pool_length) / 2
        if half_d_width + self.pool_width / 2 < x:
            x = self.width - x
        if half_d_length + self.pool_length / 2 < y:
            y = self.length - y
        return x, y