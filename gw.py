#goeman & williams max cut algorithm

import sys
import copy
import time
import math
import numpy as np
import random
import networkx as nx
import cvxpy as cp
from scipy.linalg import sqrtm

from util import read_nxgraph
from util import obj_maxcut

def gw(graph):
    """
    Solve the relaxation (P) to obtain optimal vectors Ui.
    Input: graph - NetworkX graph
    Output: optimal_vectors - list of optimal vectors Ui
    """
    # Edges list
    edges = graph.edges()

    # Number of vertices
    n = graph.number_of_nodes()
    
    # Define variables (Gram matrix X)
    X = cp.Variable((n, n), symmetric=True)
    
    constraints = [X >> 0]
    constraints += [    
        X[i,i] == 1 for i in range(n)]

    objective = sum (0.5*(1-X[i,j]) for (i,j) in edges)


    # Formulate and solve the semidefinite program
    prob = cp.Problem(cp.Maximize(objective),constraints)
    prob.solve()
    
    x = sqrtm(X.value)
    u = np.random.randn(n)

    x = np.sign(x @ u)
    print(x)

    return x

def calculate_cut_value(graph, x):
    """
    Calculate the weight of the cut based on the partition defined by vector x.
    Input: graph - NetworkX graph
           x - vector obtained from the Goemans-Williamson algorithm
    Output: cut_value - weight of the cut
    """
    # Get the edges of the graph
    edges = graph.edges()
    
    # Initialize cut value
    cut_value = 0
    
    # Partition the vertices based on the sign of x
    partition = [1 if val > 0 else 0 for val in x]
    
    # Calculate the weight of the cut
    cut_value = obj_maxcut(partition,graph)
    
    return cut_value


if __name__ == '__main__':
    graph = read_nxgraph('./data/syn/powerlaw_500_ID29.txt')
    x = gw(graph)
    cut_value = calculate_cut_value(graph, x)
    print("Cut Value:", cut_value)

