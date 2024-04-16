import math
import os
import shutil

from GeneticAlgorithm.genetic_algorithm import GeneticAlgorithm

if __name__ == '__main__':
    ga = GeneticAlgorithm(40, 60, 30, 50, 18, 1 / 3 * math.pi, 1600, 1 / 2, 0.2, 0.2, 10000)
    ga.random_construct()
    if os.path.exists('Image'):
        shutil.rmtree('Image')
    os.makedirs('Image', exist_ok=True)
    if os.path.exists('Txt'):
        shutil.rmtree('Txt')
    os.makedirs('Txt', exist_ok=True)
    for i in range(0, 100):
        print("Gen:{}".format(i))
        ga.reproduce()
        ga.show_info()
        ga.save_to_img('Image/gen' + str(i) + '.png')
        ga.to_text('Txt/gen' + str(i) + '.txt')


