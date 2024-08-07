import sys
import copy
import time
import math
from typing import List, Union
import numpy as np
import random
import networkx as nx
from util import read_nxgraph
from util import obj_maxcut

# hyperparameters for tabu search
P_iter = 100
MaxIter = 10000
gamma = 65

def generate_random(graph):
    nodes = list(graph.nodes())
    binary_vector = [random.randint(0, 1) for _ in range(len(nodes))]
    return tabu_search(binary_vector, graph)

def generate_random_population(graph, pop_size):
    count = 1
    Pop = []
    best_binary_vector = []
    score_list = []
    best_score = 0
    while len(Pop) < pop_size:
        binary_vector, result = generate_random(graph)
        score = result

        if binary_vector not in Pop:
            score_list.append(score)
            Pop.append(binary_vector)
            print(count, "Score: " , score)
            count += 1
            if score > best_score:
                best_score = score
                best_binary_vector = binary_vector
    return Pop, best_binary_vector, best_score, score_list


def tenure(iteration, maxT):
    # define the sequence of values for the tenure function
    a = [maxT * bi for bi in [1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1]]
    # define the sequence of interval margins
    x = [1] + [x + 4 * maxT * bi for x, bi in zip([1] * 15, [1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1])]
    # find the interval to determine the tenure
    interval = next(i for i, xi in enumerate(x) if xi > iteration) - 1
    return a[interval]

def compute_move_gains(graph, vector, tabu_list):
    move_gains = []
    for i in range(len(vector)):
        delta_v = 0
        neighbor_nodes = list(graph.neighbors(i))
        for j in neighbor_nodes:
            if vector[i] == vector[j]:
                delta_v += graph[i][j]["weight"]
            else:
                delta_v -= graph[i][j]["weight"]
        move_gains.append(delta_v)

    return move_gains

def update_move_gains(node_flipped,move_gains,vector,graph):
    neighbors = list(graph.neighbors(node_flipped))
    for i in neighbors:
        if vector[i] == vector[node_flipped]:
            move_gains[i] += 2 * graph[i][node_flipped]["weight"]
        else:
            move_gains[i] -= 2 * graph[i][node_flipped]["weight"]
    move_gains[node_flipped] = -move_gains[node_flipped]
    return move_gains


def perturb(binary_vector):
    # randomly select gamma vertices to move
    vertices_to_move = random.sample(range(len(binary_vector)), gamma)
    
    # flip the subsets for the selected vertices
    for vertex in vertices_to_move:
        binary_vector[vertex] = 1 - binary_vector[vertex]
    
    return binary_vector

def tabu_search(initial_solution, graph):
    # initialize best solution and its score
    best_solution = initial_solution
    best_score = obj_maxcut(initial_solution, graph)
    curr_solution = copy.deepcopy(initial_solution)
    curr_score = best_score
    # initialize iteration counter
    Iter = 0
    pit = 0
    
    # initialize tabu list and tabu tenure
    tabu_list = [0] * len(curr_solution)
    maxT = 150
    
    # compute move gains
    move_gains = compute_move_gains(graph, curr_solution, tabu_list)
    while Iter < MaxIter:
        v = 0
        delta_v = -999999
        for i in range(0,len(move_gains)):
            if delta_v < move_gains[i] and tabu_list[i] <= Iter:
                delta_v = move_gains[i]
                v = i
        
        # move v from its original subset to the opposite set
        curr_solution[v] = 1 - curr_solution[v]
        curr_score += delta_v
        # print("Current ",curr_score)
        # print("Actual ",obj_maxcut(curr_solution,graph))
        # update tabu list and move gains for each vertex v ∈ V
        tabu_list[v] = maxT + Iter
        move_gains = update_move_gains(v, move_gains, curr_solution, graph)

        # update best solution if current solution is better
        if curr_score > best_score:
            best_solution = copy.deepcopy(curr_solution)
            best_score = curr_score
            pit = 0
            
        
        # increment iteration counter
        Iter += 1
        pit += 1
        # check if best solution hasn't improved after P_iter iterations
        if pit == P_iter and curr_score <= best_score:
            pit = 0
            curr_solution = perturb(curr_solution)
            curr_score = obj_maxcut(curr_solution, graph)
            tabu_list = [0] * len(curr_solution)
            move_gains = compute_move_gains(graph, curr_solution, tabu_list)
            
    
    return best_solution, best_score



# if __name__ == '__main__':
#     # read data
#     graph = read_nxgraph('./data/gset/gset_14.txt')
    # # vector = [1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1]
    # # print(obj_maxcut(vector,graph))
    # # generating random solutions
    # print("Tabuu Search")
    # population, best_binary_vector, best_score = generate_random_population(graph, 10)
    # print("Best Binary Vector:", best_binary_vector)
    # print("Best Score:", best_score)
    # total = 0
    # for i in population:
    #     total += obj_maxcut(i,graph)
    # total /= 10
    # print("Average of Population: ", total)

    # while True:
    #     population, new_binary_vector, new_score = generate_random_population(graph, 10)
    #     if new_score > best_score:
    #         best_binary_vector = copy.deepcopy(new_binary_vector)
    #         best_score = new_score
    #         print("Best Binary Vector:", best_binary_vector)
    #         print("Best Score:", best_score)

