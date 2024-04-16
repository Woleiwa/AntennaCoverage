import os
import random

import numpy as np
from pool import Pool
from chromosome import Chromosome, merge_sort


class GeneticAlgorithm:
    def __init__(self, width, length, pool_width, pool_length, radius, detect_angle, num,
                 ratio, mutate_possibility, increase_possibility, monte_carlo_num):
        self.pool = Pool(width, length, pool_width, pool_length)
        self.radius = radius
        self.detect_angle = detect_angle
        self.num = num
        self.mutate_possibility = mutate_possibility
        self.increase_possibility = increase_possibility
        self.ratio = ratio
        self.population = []
        self.monte_carlo_num = monte_carlo_num

    def random_construct(self):
        for i in range(0, self.num):
            antenna_num = (self.pool.pool_width * self.pool.pool_length /
                           (self.radius * self.radius * self.detect_angle * 2))
            chromosome = Chromosome(self.pool, self.radius, self.detect_angle)
            chromosome.random_generate(np.random.randint(int(antenna_num) + 1, int(4 * antenna_num)))
            chromosome.generate_antennas()
            chromosome.mutate(True)
            chromosome.get_fitness(self.monte_carlo_num)
            self.population.append(chromosome)
        selected_idx = random.sample(range(0, self.num), self.num // 10)
        for i in selected_idx:
            print("Selected index:{}".format(i))
            # idx = 0
            # os.makedirs('../Test/' + str(i), exist_ok=True)
            while self.population[i].coverage < 1:
                self.population[i].mutate(True)
                self.population[i].get_fitness(self.monte_carlo_num)
                print("Fitness:{}".format(self.population[i].fitness))
                # self.population[i].to_image('../Test/' + str(i) + '/' + str(idx))
                # idx += 1
        merge_sort(self.population, 0, len(self.population) - 1)

    def select_parents(self):
        fitness_sum = 0
        fitness_list = []
        parent_list = []
        for pop in self.population:
            fitness_sum += pop.get_fitness(self.monte_carlo_num)
            fitness_list.append(pop.get_fitness(self.monte_carlo_num))

        selected_num = int(self.num * self.ratio)
        for idx in range(0, selected_num):
            target = np.random.uniform(0, fitness_sum)
            culminate_fitness = 0
            for i in range(self.num):
                culminate_fitness += fitness_list[i]
                if culminate_fitness >= target:
                    father = i
                    break
            target = np.random.uniform(0, fitness_sum)
            culminate_fitness = 0
            for i in range(self.num):
                culminate_fitness += fitness_list[i]
                if culminate_fitness >= target:
                    mother = i
                    break
            parent_list.append([father, mother])
        return parent_list

    def reproduce(self):
        parent_list = self.select_parents()
        children_list = []
        for parent in parent_list:
            father = parent[0]
            mother = parent[1]
            child = self.population[father].cross_over(self.population[mother])
            children_list.append(child)
            child.get_fitness(self.monte_carlo_num)
        merge_sort(children_list, 0, len(children_list) - 1)
        merge_population = []
        i = 0
        j = 0
        while i < len(self.population) and j < len(children_list):
            if self.population[i].compare(children_list[j]):
                merge_population.append(self.population[i])
                i += 1
            else:
                merge_population.append(children_list[j])
                j += 1
            if len(merge_population) == self.num:
                break

        while i < len(self.population):
            if len(merge_population) == self.num:
                break
            merge_population.append(self.population[i])
            i += 1

        while j < len(children_list):
            if len(merge_population) == self.num:
                break
            merge_population.append(children_list[j])
            j += 1

        self.population = merge_population

        mutate_idx = random.sample(range(0, self.num), int(self.num * self.mutate_possibility))
        increase_idx = random.sample(range(0, self.num), int(self.num * self.mutate_possibility))
        mutate_list = []
        increase_list = []
        print('length of mutate list:{}'.format(len(mutate_idx)))
        print('length of increase list:{}'.format(len(mutate_idx)))
        for i in mutate_idx:
            mutate_list.append(self.population[i].copy())
        for i in increase_idx:
            increase_list.append(self.population[i].copy())
        for chromo in mutate_list:
            chromo.mutate(False)
        for chromo in increase_list:
            chromo.mutate(True)
        mutate_list.extend(increase_list)

        merge_population = []
        i = 0
        j = 0
        while i < len(self.population) and j < len(mutate_list):
            if self.population[i].compare(mutate_list[j]):
                merge_population.append(self.population[i])
                i += 1
            else:
                merge_population.append(mutate_list[j])
                j += 1
            if len(merge_population) == self.num:
                break

        while i < len(self.population):
            if len(merge_population) == self.num:
                break
            merge_population.append(self.population[i])
            i += 1

        while j < len(mutate_list):
            if len(merge_population) == self.num:
                break
            merge_population.append(mutate_list)
            j += 1
        self.population = merge_population

        print('Length of the population:{}'.format(len(self.population)))
        for i in range(0, self.num):
            if self.population[i].coverage == 1:
                copied_chromo = self.population[i].copy()
                copied_chromo.mutate(True)
                copied_chromo.get_fitness(self.monte_carlo_num)
                if copied_chromo.fitness > self.population[i].fitness:
                    self.population[i] = copied_chromo
            else:
                break
        merge_sort(self.population,0, i - 1)
        print('The num of fully-covered graph: {}'.format(i + 1))

    def show_info(self):
        print("Fitness score{}".format(self.population[0].fitness))
        print("Coverage score{}".format(self.population[0].coverage))
        print("Intersection score{}".format(self.population[0].intersection))
        print("Utilization score{}".format(self.population[0].utilization))

    def save_to_img(self, path):
        self.population[0].to_image(path)

    def to_text(self, path):
        self.population[0].to_text(path)