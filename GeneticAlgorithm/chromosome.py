import copy
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from directional_antenna import DirectionalAntenna


def merge_sort(array, start, end):
    if start >= end:
        return
    mid = (start + end) // 2
    merge_sort(array, start, mid)
    merge_sort(array, mid + 1, end)
    copy_array = []
    i = start
    j = mid + 1
    while i <= mid and j <= end:
        if array[i].compare(array[j]):
            copy_array.append(array[i])
            i += 1
        else:
            copy_array.append(array[j])
            j += 1
    while i <= mid:
        copy_array.append(array[i])
        i += 1
    while j <= end:
        copy_array.append(array[j])
        j += 1
    for i in range(0, end - start + 1):
        array[i + start] = copy_array[i]


def binary_search(array, target):
    end = len(array) - 1
    if end == -1 or target.compare(array[0]):
        return 0
    elif array[end].compare(target):
        return end + 1
    start = 0
    mid = (start + end) // 2
    while start <= end:
        if array[mid].compare(target) and target.compare(array[mid + 1]):
            return mid + 1
        elif target.compare(array[mid]):
            end = mid - 1
        else:
            start = mid + 1
        mid = (start + end) // 2


def calculate_angle(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0:
        if dy >= 0:
            angle = math.pi / 2
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
    return angle


class Chromosome:
    def __init__(self, pool, radius, detect_angle):
        self.pool = pool
        self.radius = radius
        self.detect_angle = detect_angle
        self.list = [[], [], []]
        self.antennas = []
        self.uncovered_point = None
        self.coverage = None
        self.fitness = None
        self.intersection = None
        self.utilization = None

    def copy(self):
        another = Chromosome(self.pool, self.radius, self.detect_angle)
        another.list = copy.deepcopy(self.list)
        another.antennas = copy.deepcopy(self.antennas)
        another.uncovered_point = self.uncovered_point
        another.coverage = self.coverage
        another.fitness = self.fitness
        another.intersection = self.intersection
        return another

    def random_generate(self, num):
        area_list = self.pool.get_area_of_different_part()
        area_sum = np.sum(area_list)
        for i in range(0, num):
            target = np.random.uniform(0, area_sum)
            accumulate = 0
            for area_index in range(0, 3):
                accumulate += area_list[area_index]
                if accumulate >= target:
                    break
            x_min, x_max, y_min, y_max = self.pool.get_quarter_range(area_index)
            x = np.random.uniform(x_min, x_max)
            y = np.random.uniform(y_min, y_max)
            angle_1, angle_2 = self.get_angle_range(area_index, x, y)
            direction = np.random.uniform(angle_1, angle_2)
            antenna = DirectionalAntenna(x, y, self.radius, self.detect_angle, direction)
            self.list[area_index].append(antenna)

    def generate_antennas(self):
        self.antennas = []
        for i in range(0, 3):
            for antenna in self.list[i]:
                antenna.covered_num = 0
                antenna.intersected_num = 0
                self.antennas.append(antenna)
                antenna_1 = DirectionalAntenna(self.pool.width - antenna.x, antenna.y, self.radius,
                                               self.detect_angle, math.pi - antenna.direction)
                antenna_2 = DirectionalAntenna(antenna.x, self.pool.length - antenna.y, self.radius,
                                               self.detect_angle, 2 * math.pi - antenna.direction)
                antenna_3 = DirectionalAntenna(self.pool.width - antenna.x, self.pool.length - antenna.y,
                                               self.radius,
                                               self.detect_angle, math.pi + antenna.direction)
                self.antennas.append(antenna_1)
                self.antennas.append(antenna_2)
                self.antennas.append(antenna_3)

    def clear(self):
        for antenna in self.antennas:
            antenna.covered_num = 0
            antenna.intersected_num = 0
        self.fitness = None
        self.coverage = None
        self.intersection = None
        self.uncovered_point = None
        self.utilization = None

    def get_fitness(self, num):
        if len(self.antennas) == 0:
            self.generate_antennas()
        if self.fitness is not None:
            return self.fitness
        else:
            x_min, x_max, y_min, y_max = self.pool.get_pool_range()
            x_list = np.random.uniform(x_min, x_max, num)
            y_list = np.random.uniform(y_min, y_max, num)
            covered_num = 0
            intersect_num = 0
            for x, y in zip(x_list, y_list):
                flag = False
                added = False
                first_antenna = None
                for antenna in self.antennas:
                    if antenna.in_range(x, y):
                        if not flag:
                            covered_num += 1
                            flag = True
                            first_antenna = antenna
                            antenna.covered_num += 1
                        else:
                            if not added:
                                intersect_num += 1
                                added = True
                                first_antenna.intersected_num += 1
                            antenna.covered_num += 1
                            antenna.intersected_num += 1
                if not flag:
                    if self.uncovered_point is None:
                        self.uncovered_point = [x, y]
                    elif self.pool.distance_to_edge(self.uncovered_point[0],
                                                    self.uncovered_point[1]) < self.pool.distance_to_edge(x, y):
                        self.uncovered_point = [x, y]

            self.coverage = covered_num / num
            self.intersection = intersect_num / num
            area_of_pool = self.pool.pool_length * self.pool.pool_width
            area_of_antenna = self.radius * self.radius * self.detect_angle / 2 * len(self.antennas)
            if area_of_antenna != 0:
                self.utilization = area_of_pool / area_of_antenna
            else:
                self.utilization = 0
            if self.coverage < 1:
                self.fitness = 1 - self.intersection + 16 * self.coverage * self.coverage
            else:
                self.fitness = 16 * self.utilization * self.utilization + 20
            return self.fitness

    def cross_over(self, another):
        child = Chromosome(self.pool, self.radius, self.detect_angle)
        for idx in range(0, 3):
            i = 0
            j = 0
            antenna_list = []
            while i < len(self.list[idx]) and j < len(another.list[idx]):
                if self.list[idx][i].compare(another.list[idx][j]):
                    antenna_list.append(self.list[idx][i])
                    i += 1
                else:
                    antenna_list.append(another.list[idx][j])
                    j += 1
            while i < len(self.list[idx]):
                antenna_list.append(self.list[idx][i])
                i += 1
            while j < len(another.list[idx]):
                antenna_list.append(another.list[idx][j])
                j += 1
            for antenna in antenna_list:
                possibility = np.random.uniform(0, 1)
                if possibility >= 0.5:
                    child.list[idx].append(antenna.copy())
        child.generate_antennas()
        return child

    def mutate(self, mutate_flag):
        if self.fitness is None:
            self.antennas = []
            self.generate_antennas()
            self.get_fitness(10000)

        # add or delete gene from chromosome
        if mutate_flag:
            if self.coverage < 1:
                target_x, target_y = self.pool.point_in_first_range(self.uncovered_point[0], self.uncovered_point[1])
                area_index, antenna = self.generate_antenna()
                while not antenna.in_range(target_x, target_y):
                    area_index, antenna = self.generate_antenna()
                i = binary_search(self.list[area_index], antenna)
                self.list[area_index].append(antenna)
                if i < len(self.list[area_index]) - 1:
                    j = len(self.list[area_index]) - 1
                    while j > i:
                        self.list[area_index][j] = self.list[area_index][j - 1]
                        j -= 1
                    self.list[area_index][i] = antenna
            else:
                remove_list = []
                for antennas in self.list:
                    for antenna in antennas:
                        if antenna.covered_num == antenna.intersected_num or antenna.covered_num == 0:
                            remove_list.append(antenna)
                if len(remove_list) == 0:
                    return
                idx = np.random.randint(0, len(remove_list))
                remove_one = remove_list[idx]
                for antennas in self.list:
                    if antennas.__contains__(remove_one):
                        antennas.remove(remove_one)

        # mutate gene
        else:
            idx = np.random.randint(0, 3)
            while len(self.list[idx]) == 0:
                idx = np.random.randint(0, 3)
            x_min, x_max, y_min, y_max = self.pool.get_quarter_range(idx)
            x = np.random.uniform(x_min, x_max)
            y = np.random.uniform(y_min, y_max)
            angle_1, angle_2 = self.get_angle_range(idx, x, y)
            direction = np.random.uniform(angle_1, angle_2)
            antenna = DirectionalAntenna(x, y, self.radius, self.detect_angle, direction)
            i = binary_search(self.list[idx], antenna)
            if i == len(self.list[idx]):
                i = i - 1
            self.list[idx][i] = antenna

        self.clear()
        self.generate_antennas()

    def compare(self, another):
        if self.fitness is None:
            self.get_fitness(100000)
        if another.fitness is None:
            another.get_fitness(100000)
        if self.fitness > another.fitness:
            return True
        elif self.fitness == another.fitness:
            return self.intersection < another.intersection
        return False

    def get_angle_range(self, idx, x, y):
        x_min, x_max, y_min, y_max = self.pool.get_pool_range()
        if idx == 0:
            angle_1 = calculate_angle(x, y, x_max, y_min)
            angle_2 = calculate_angle(x, y, x_min, y_max)
            angle_3 = math.asin((y_min - y) / self.radius)
            angle_4 = math.acos((x_min - x) / self.radius)
            if angle_3 > angle_1:
                angle_1 = angle_3
            if angle_4 < angle_2:
                angle_2 = angle_4
        elif idx == 1:
            angle_1 = calculate_angle(x, y, x_max, y_min)
            angle_2 = calculate_angle(x, y, x_min, y_min)
            angle_3 = math.asin((y_min - y) / self.radius)
            angle_4 = math.pi - angle_3
            if angle_3 > angle_1:
                angle_1 = angle_3
            if angle_4 < angle_2:
                angle_2 = angle_4
        elif idx == 2:
            angle_1 = calculate_angle(x, y, x_min, y_min)
            angle_2 = calculate_angle(x, y, x_min, y_max)
            angle_3 = -math.acos((x_min - x) / self.radius)
            angle_4 = -angle_3
            if angle_1 == math.pi / 2:
                angle_1 == 3 * math.pi / 2
            angle_1 = angle_1 - 2 * math.pi
            if angle_3 > angle_1:
                angle_1 = angle_3
            if angle_4 < angle_2:
                angle_2 = angle_4
        angle_1 = angle_1 + self.detect_angle / 2
        angle_2 = angle_2 - self.detect_angle / 2
        if angle_1 > angle_2:
            return angle_2, angle_1
        return angle_1, angle_2

    def generate_antenna(self):
        area_list = self.pool.get_area_of_different_part()
        area_sum = np.sum(area_list)
        target = np.random.uniform(0, area_sum)
        accumulate = 0
        for area_index in range(0, 3):
            accumulate += area_list[area_index]
            if accumulate >= target:
                break
        x_min, x_max, y_min, y_max = self.pool.get_quarter_range(area_index)
        x = np.random.uniform(x_min, x_max)
        y = np.random.uniform(y_min, y_max)
        angle_1, angle_2 = self.get_angle_range(area_index, x, y)
        direction = np.random.uniform(angle_1, angle_2)
        antenna = DirectionalAntenna(x, y, self.radius, self.detect_angle, direction)
        return area_index, antenna

    def to_image(self, path):
        fig, ax = plt.subplots()
        rectangle = patches.Rectangle((0, 0), self.pool.width, self.pool.length, linewidth=1, edgecolor='blue',
                                      facecolor='none')
        x, _, y, _ = self.pool.get_pool_range()
        pool_rectangle = patches.Rectangle((x, y), self.pool.pool_width, self.pool.pool_length, linewidth=1,
                                           edgecolor='blue', facecolor='none')

        for antenna in self.antennas:
            start_angle = antenna.direction - antenna.detect_angle / 2
            end_angle = antenna.direction + antenna.detect_angle / 2
            start_angle = math.degrees(start_angle)
            end_angle = math.degrees(end_angle)
            ax.pie([1], radius=antenna.radius, startangle=start_angle, colors=['yellow'],
                   wedgeprops={'theta1': start_angle, 'theta2': end_angle}, center=(antenna.x, antenna.y))

        for antenna in self.antennas:
            ax.plot(antenna.x, antenna.y, 'ro')
        ax.add_patch(rectangle)
        ax.add_patch(pool_rectangle)

        ax.set_xlim(-10, 100)
        ax.set_ylim(-10, 100)
        # plt.show()
        plt.savefig(path)
        plt.close(fig)

    def to_text(self, path):
        with open(path, 'w') as f:
            for antennas in self.list:
                for antenna in antennas:
                    f.write('x:' + str(antenna.x) + ' y:' + str(antenna.y) + ' direction:' + str(antenna.direction) + '\n')
