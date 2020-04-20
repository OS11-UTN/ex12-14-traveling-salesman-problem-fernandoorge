################################################################################
#   OS11 LOGISTICS
#
#   Author   : Orge, Fernando Gabriel
#   Exercise : EX12 - Traveling Salesman Problem - LP with subtours
################################################################################
import numpy     as np
import logistics as lg
import math
import random
import matplotlib
import matplotlib.pyplot as plt
from   scipy.optimize import  linprog

random.seed(5)
ncoor  = 15
G      = lg.full_graph(ncoor)
points = lg.get_random_points(ncoor)

costs  = []
for i in range(0, ncoor):
    for j in range(0, ncoor):
        if (i != j):
            costs.append( lg.distance(points[j], points[i]) )
            
NA  , arcs = lg.nn2na(G)
Aeq1, arcs = lg.nn2na(G)
Aeq2, arcs = lg.nn2na(G)

(row, col) = NA.shape
for i in range(0, row):
    for j in range(0, col):
        if Aeq1[i,j] < 0:
            Aeq1[i,j] = 0
        if Aeq2[i,j] > 0:
            Aeq2[i,j] = 0
        if Aeq2[i,j] < 0:
            Aeq2[i,j] = 1

Aeq = np.concatenate((Aeq1, Aeq2))
beq = np.ones(2*ncoor)
bounds = tuple([(0, 1) for arcs in range(0, len(arcs))])

print('\n SOLVING PROBLEM WITH SIMPLEX')
res = linprog(c=costs, A_eq=Aeq, b_eq=beq, bounds=bounds, method='simplex')
print('\t Solution to the problem:')
print('\t     The minimum distance will be    : %0.2f ' % res.fun)

# Now take the res.x vector an insert an extra node for each node
# this extra node will represent the conection between the node with itself
# this is only used to facilitate the plot of the paths
connections = []
for k in range(0, ncoor):
    partial = list(res.x[(ncoor-1)*k:(ncoor-1)*(k+1)])
    partial.insert(k, 0.0)
    connections.append(partial)
    print('\t    Node %2d conection : %s' % (k, partial))
    
plt.figure()
plt.plot( [tup[0] for tup in points] , [tup[1] for tup in points] , 'ro')
plt.xlim(0,1)
plt.ylim(0,1)
plt.title('TSP - CITIES')
plt.xlabel('x coordinates (normalized)')
plt.ylabel('y coordinates (normalized)')
plt.grid()
plt.savefig("ex12_tsp_cities.png")
for i in range(0, ncoor):
    for j in range(0, ncoor):
        if connections[i][j] == 1:
            x = [points[i][0], points[j][0]]
            y = [points[i][1], points[j][1]]
            plt.plot(x, y, 'b--')
plt.xlim(0,1)
plt.ylim(0,1)
plt.title('TSP - SUBTOURS')
plt.savefig("ex12_tsp_subtours.png")

# get the list of subtours
subtours = lg.get_subtours(connections)
for st in subtours:
    print('\t    Subtour found: %s' % st)

################################################################################
################################################################################
