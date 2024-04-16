import math
import numpy as np

from chromosome import Chromosome
from genetic_algorithm import GeneticAlgorithm
from pool import Pool
from directional_antenna import DirectionalAntenna

if __name__ == "__main__":
    ga = GeneticAlgorithm(40, 60, 30, 50, 18, 1 / 3 * math.pi, 10, 1 / 2, 0.2, 0.2, 10000)
    ga.random_construct()
    ga.show_info()
    ga.to_text('../Txt/1.txt')


