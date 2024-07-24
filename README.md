## Algorithm Description
This is a multiparent genetic crossover algorithm to help find the best cut. A Tabu search is implemented to find optimum of with a pertebation after a certain number of non improving moves. This pertebation is a mutation of the current solution to hopefully escape local optimum and to increase the amount of solutions searched. Best moves are calculated in constant time with a move gains list of each node, updated per move for each node. Each element in the list corresponds to a node in the graph and respresents the change in cut score if set is changed on that node. 

## Solutions
Solutions to each graph is given in /data/results.txt file as a binary vector with a label of score and graph above.

## Results
Results for Gurobis QUBO solver and L2A were taken from provided results text documents Gurobis obj: ... and L2A best in line on the graph
| Graph  | Gurobis (1 hour) | L2A | Mine | Improvement % |
| ------------- | ------------- | ------------- | ------------- | ------------- | 
| powerlaw_100_ID_27 | 284 | 284 | 284 | 0.0% | 
| powerlaw_200_ID29 | 576 | 576 | 576 | 0.0% | 
| powerlaw_300_ID29 | 875 | 875 | 875 | 0.0% | 
| powerlaw_400_ID28 | 1174 | 1174 | 1174 | 0.0% | 
| powerlaw_400_ID29 | 1174 | 1172 | 1174 | 0.0% | 
| powerlaw_400_ID29 | 1174 | 1172 | 1174 | 0.0% | 
| powerlaw_400_ID29 | 1174 | 1172 | 1174 | 0.0% | 
| powerlaw_500_ID15 | 1467 | 1469 | 1471 | 0.27% | 
| powerlaw_500_ID18 | 1469 | 1475 | 1477 | 0.14% | 
| powerlaw_500_ID21 | 1468 | 1464 | 1481 | 0.88% | 
| powerlaw_500_ID22 | 1474 | 1474 | 1176 | 0.27% | 
| powerlaw_500_ID24 | 1469 | 1470 | 1473 | 0.17% | 
| powerlaw_500_ID26 | 1475 | 1467 | 1475 | 0.0% | 
| powerlaw_500_ID27 | 1462 | 1464 | 1465 | 0.07% | 
| powerlaw_500_ID28 | 1465 | 1463 | 1465 | 0.0% | 
| powerlaw_500_ID29 | 1464 | 1468 | 1473 | 0.34% | 
| Gset_14 | 3042 | 3064 | 3063 | -0.03% | 
| Gset_15 | 3033 | 3050 | 3050 | 0.0% | 
| Gset_29 | -- | -- | 3355 | -- | 

## References

1) Qinghua Wu and Jin-Kao Hao: A Memetic Approach for the Max-Cut Problem, LERIA, Universit´e d’Angers, 2 Boulevard Lavoisier, 49045 Angers Cedex 01, France
