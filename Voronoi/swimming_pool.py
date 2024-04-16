import numpy as np
from installing_point import InstallingPoint
from scipy.spatial import Voronoi
import math


def distance(point1, point2):
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    res = dx * dx + dy * dy
    res = math.pow(res, 1 / 2)
    return res


class SwimmingPool:
    def __init__(self, width, length, radius):
        self.width = width
        self.length = length
        self.radius = radius
        self.points = []
        self.point_list = []
        self.vertice_list = []
        self.voronoi = None

    def generate_voronoi(self):
        self.point_list = []
        self.vertice_list = []
        for point in self.points:
            self.point_list.append(point.to_list())
        points = np.array(self.point_list)
        self.voronoi = Voronoi(points)

        for point_idx, region_index in enumerate(self.voronoi.point_region):
            region = self.voronoi.regions[region_index]
            vertices = []
            for idx in region:
                if idx != - 1:
                    vertices.append(idx)
            self.vertice_list.append(vertices)

    def add_points(self, x, y):
        point = InstallingPoint(x, y, self.width, self.length)
        insert_index = 0
        end = len(self.points) - 1
        if end == -1:
            self.points.append(point)
            return
        elif self.points[end].compare(point):
            insert_index = len(self.points)
        elif point.compare(self.points[0]):
            insert_index = 0
        else:
            start = 0
            mid = (end + start) // 2
            while start <= end:
                if self.points[mid].compare(point) and point.compare(self.points[mid + 1]):
                    insert_index = mid + 1
                    break
                elif point.compare(self.points[mid]):
                    end = mid - 1
                else:
                    start = mid + 1
                mid = (end + start) // 2
        self.points.append(point)
        for i in range(1, len(self.points) - insert_index):
            index = len(self.points) - i
            self.points[index] = self.points[index - 1]
        self.points[insert_index] = point

    def is_covered(self):
        max_dis = 0
        farthest = []
        for idx in range(0, len(self.point_list)):
            for v_idx in self.vertice_list[idx]:

                vertice = self.voronoi.vertices[v_idx]
                if 0 <= vertice[0] <= self.width and 0 <= vertice[1] <= self.length:
                    dis = distance(self.point_list[idx], vertice)
                    if dis > max_dis:
                        max_dis = dis
                        farthest = self.voronoi.vertices[v_idx]

        max_dis_1 = pow(self.width * self.width + self.length * self.length, 1 / 2)
        max_dis_2 = max_dis_1
        max_dis_3 = max_dis_1
        max_dis_4 = max_dis_1
        for idx in range(0, len(self.points)):
            dis_1 = distance(self.point_list[idx], [0, 0])
            dis_2 = distance(self.point_list[idx], [self.width, 0])
            dis_3 = distance(self.point_list[idx], [0, self.length])
            dis_4 = distance(self.point_list[idx], [self.width, self.length])
            if dis_1 < max_dis_1:
                max_dis_1 = dis_1
            if dis_2 < max_dis_2:
                max_dis_2 = dis_2
            if dis_3 < max_dis_3:
                max_dis_3 = dis_3
            if dis_4 < max_dis_4:
                max_dis_4 = dis_4

        if max_dis_1 > max_dis:
            max_dis = max_dis_1
            farthest = [0, 0]
        if max_dis_2 > max_dis:
            max_dis = max_dis_2
            farthest = [self.width, 0]
        if max_dis_3 > max_dis:
            max_dis = max_dis_3
            farthest = [0, self.length]
        if max_dis_4 > max_dis:
            max_dis = max_dis_4
            farthest = [self.width, self.length]

        for idx in range(0, len(self.points) - 1):
            intersects = self.points[idx].intersect_point(self.points[idx + 1])
            for intersect in intersects:
                point = InstallingPoint(intersect[0], intersect[1], self.width, self.length)
                dis_to_origin = point.distance_to_origin()
                dis_to_origin_1 = self.points[idx].distance_to_origin()
                dis_to_origin_2 = self.points[idx + 1].distance_to_origin()
                if dis_to_origin_1 <= dis_to_origin <= dis_to_origin_2:
                    dis = distance(self.point_list[idx], intersect)
                    if dis > max_dis:
                        max_dis = dis
                        farthest = intersect
        if len(self.points) > 1:
            intersects = self.points[len(self.points) - 1].intersect_point(self.points[0])
            for intersect in intersects:
                point = InstallingPoint(intersect[0], intersect[1], self.width, self.length)
                dis_to_origin = point.distance_to_origin()
                dis_to_origin_1 = self.points[len(self.points) - 1].distance_to_origin()
                if dis_to_origin_1 <= dis_to_origin:
                    dis = distance(self.point_list[0], intersect)
                    if dis > max_dis:
                        max_dis = dis
                        farthest = intersect

        return max_dis > self.radius, farthest
