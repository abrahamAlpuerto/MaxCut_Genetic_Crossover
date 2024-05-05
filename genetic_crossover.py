import sys
import copy
import time
import math
from typing import List, Union
import numpy as np
import random
import networkx as nx

from tabu_Search import generate_random_population
from tabu_Search import tabu_search
from util import read_nxgraph
from util import obj_maxcut

def cross_over(population):
    selected_parents = random.sample(population, num_parents)

    child = []
    for node in range(0,len(selected_parents[0])):
        node_in_same_set = all(parent[node] == selected_parents[0][node] for parent in selected_parents)

        if node_in_same_set:
            child.append(selected_parents[0][node])
        else:
            child.append(random.randint(0,1))
    child, child_score = tabu_search(child,graph)
    return child

def algorithm_run():
    population, best_binary_vector, best_score, population_scores = generate_random_population(graph, 10)
    c_iter = 0
    print("Start Genetic Crossover")
    while c_iter < c_itMax:
        child = cross_over(population)
        if(child not in population):
            child_score = obj_maxcut(child,graph)

            print(c_iter + 1," Childs Score: ", child_score)
    
            # Finding the min score in the list and replacing it with the child if smaller than child cut
            min_score_index = np.argmin(population_scores)
            if(population_scores[min_score_index] < child_score):
                population_scores[min_score_index] = child_score
                population[min_score_index] = child
            c_iter += 1
        

    max_score_index = np.argmax(population_scores)
    max_score_vector = population[max_score_index]
    print("Binary Vector: ", max_score_vector)
    print("Score of Cut: ", population_scores[max_score_index])
    print("Genetic Search Complete")


    
if __name__ == '__main__':
    # Constants
    num_parents = 5
    c_itMax = 5
    # read data
    graph = read_nxgraph('./data/syn/powerlaw_500_ID15.txt')
    print("Genetic Search Start")
    algorithm_run()

    # Cut checker
    # vector = [1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1]
    # print(obj_maxcut(vector,graph))
