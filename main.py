from Voronoi.swimming_pool import SwimmingPool
import matplotlib.pyplot as plt
from scipy.spatial import voronoi_plot_2d

import random
if __name__ == '__main__':
    pool = SwimmingPool(25, 50, 13)

    """for i in range(0, 40):
        x = random.random() * 25
        y = random.random() * 50
        p = random.randint(0,3)
        if p == 0:
            x = 0
        elif p == 1:
            y = 0
        elif p == 2:
            x = 25
        else:
            y = 50
        pool.add_points(x, y)"""
    pool.add_points(0, 25)
    pool.add_points(25, 25)
    pool.add_points(12.5, 0)
    pool.add_points(12.5, 50)
    pool.generate_voronoi()
    voronoi_plot_2d(pool.voronoi)
    plt.show()

    judge, point = pool.is_covered()
    while judge:
        print(judge)
        print(point)
        dis_1 = point[0]
        dis_2 = point[1]
        dis_3 = 25 - point[0]
        dis_4 = 50 - point[1]
        dis_list = [dis_1, dis_2, dis_3, dis_4]
        min = dis_1
        min_index = 0
        for i in range(1, 4):
            if dis_list[i] < min:
                min = dis_list[i]
                min_index = i
        if min_index == 0:
            x = 0
            y= point[1]
        elif min_index == 1:
            x = point[0]
            y = 0
        elif min_index == 2:
            x = 25
            y = point[1]
        else:
            x = point[0]
            y = 50
        pool.add_points(x, y)
        pool.generate_voronoi()
        judge, point = pool.is_covered()
    fig, ax = plt.subplots()
    rectangle = plt.Rectangle((0, 0), 25, 50, edgecolor='red', facecolor='none')
    ax.add_patch(rectangle)
    voronoi_plot_2d(pool.voronoi, ax)
    ax.set_xlim(-10, 60)
    ax.set_ylim(-10, 60)
    plt.show()
