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

def generate_random(graph):
    nodes = list(graph.nodes())
    binary_vector = [random.randint(0, 1) for _ in range(len(nodes))]
    return tabu_search(binary_vector, graph)

def generate_random_population(graph, pop_size):
    count = 1
    Pop = []
    best_binary_vector = []
    best_score = 0
    while len(Pop) < pop_size:
        result = generate_random(graph)
        binary_vector, score = result
        if binary_vector not in Pop:
            Pop.append(binary_vector)
            print(count, "Score: " , score)
            count += 1
            if score > best_score:
                best_score = score
                best_binary_vector = binary_vector
    return Pop, best_binary_vector, best_score


def tenure(iteration, maxT):
    # Define the sequence of values for the tenure function
    a = [maxT * bi for bi in [1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1]]
    # Define the sequence of interval margins
    x = [1] + [x + 4 * maxT * bi for x, bi in zip([1] * 15, [1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1])]
    # Find the interval to determine the tenure
    interval = next(i for i, xi in enumerate(x) if xi > iteration) - 1
    return a[interval]

def compute_move_gains(graph, vector, tabu_list):
    move_gains = []
    for i in range(len(vector)):
        delta_v = 0
        neighbor_nodes = list(graph.neighbors(i))
        for j in neighbor_nodes:
            if vector[i] == vector[j]:
                delta_v += 1
            else:
                delta_v -= 1
        move_gains.append(delta_v)

    return move_gains

def update_move_gains(node_flipped,move_gains,vector,graph):
    neighbors = list(graph.neighbors(node_flipped))
    for i in neighbors:
        if vector[i] == vector[node_flipped]:
            move_gains[i] += 2
        else:
            move_gains[i] -= 2
    move_gains[node_flipped] = -move_gains[node_flipped]
    return move_gains


def perturb(binary_vector):
    # Randomly select gamma vertices to move
    vertices_to_move = random.sample(range(len(binary_vector)), gamma)
    
    # Flip the subsets for the selected vertices
    for vertex in vertices_to_move:
        binary_vector[vertex] = 1 - binary_vector[vertex]
    
    return binary_vector

def tabu_search(initial_solution, graph):
    # Initialize best solution and its score
    best_solution = initial_solution
    best_score = obj_maxcut(initial_solution, graph)
    curr_solution = copy.deepcopy(initial_solution)
    curr_score = best_score
    # Initialize iteration counter
    Iter = 0
    pit = 0
    
    # Initialize tabu list and tabu tenure
    tabu_list = [0] * len(curr_solution)
    maxT = 20  
    
    # Compute move gains
    move_gains = compute_move_gains(graph, curr_solution, tabu_list)
    while Iter < MaxIter:
        v = 0
        delta_v = -999999
        for i in range(0,len(move_gains)):
            if delta_v < move_gains[i] and tabu_list[i] <= Iter:
                delta_v = move_gains[i]
                v = i
        
        # Move v from its original subset to the opposite set
        curr_solution[v] = 1 - curr_solution[v]
        curr_score += delta_v
        # print("Current ",curr_score)
        # print("Actual ",obj_maxcut(curr_solution,graph))
        # Update tabu list and move gains for each vertex v ∈ V
        tabu_list[v] = maxT + Iter
        move_gains = update_move_gains(v, move_gains, curr_solution, graph)

        # Update best solution if current solution is better
        if curr_score > best_score:
            best_solution = copy.deepcopy(curr_solution)
            best_score = curr_score
            pit = 0
            
        
        # Increment iteration counter
        Iter += 1
        pit += 1
        # Check if best solution hasn't improved after P_iter iterations
        if pit == P_iter and curr_score <= best_score:
            pit = 0
            curr_solution = perturb(curr_solution)
            curr_score = obj_maxcut(curr_solution, graph)
            tabu_list = [0] * len(curr_solution)
            move_gains = compute_move_gains(graph, curr_solution, tabu_list)
            
    
    return best_solution, best_score



def memetic_algorithm(graph):
    return

if __name__ == '__main__':
    # read data
    graph = read_nxgraph('./data/gset/gset_14.txt')
    P_iter = 200
    MaxIter = 1000000
    gamma = 75
    # vector = [1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1]
    # print(obj_maxcut(vector,graph))
    # generating random solutions
    print("Tabuu Search")
    population, best_binary_vector, best_score = generate_random_population(graph, 10)
    print("Best Binary Vector:", best_binary_vector)
    print("Best Score:", best_score)
    total = 0
    for i in population:
        total += obj_maxcut(i,graph)
    total /= 10
    print("Average of Population: ", total)

    while True:
        population, new_binary_vector, new_score = generate_random_population(graph, 10)
        if new_score > best_score:
            best_binary_vector = copy.deepcopy(new_binary_vector)
            best_score = new_score
            print("Best Binary Vector:", best_binary_vector)
            print("Best Score:", best_score)

