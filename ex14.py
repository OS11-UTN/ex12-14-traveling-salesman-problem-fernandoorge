################################################################################
#   OS11 LOGISTICS
#
#   Author   : Orge, Fernando Gabriel
#   Exercise : EX14
################################################################################
import numpy     as np
import logistics as lg
import math
import random
import matplotlib
import matplotlib.pyplot as plt
from   scipy.optimize import  linprog

def adjust_plot(title):
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.grid()
    plt.xlabel('x coordinates (normalized)')
    plt.ylabel('y coordinates (normalized)')
    plt.title(title)

################################################################################
##                          MAIN SCRIPT
################################################################################
random.seed(5)
ncoor  = 15
G      = lg.full_graph(ncoor)
points = lg.get_random_points(ncoor)

plt.figure()
plt.plot( [tup[0] for tup in points] , [tup[1] for tup in points] , 'ro')
adjust_plot('TSP - CITIES')
plt.savefig("ex14_tsp_cities.png")

tour = [x for x in range(0,ncoor)]
plt.figure()
lg.plot_tour(points, tour)
adjust_plot('TSP - Initial Tour')
plt.savefig("ex14_tsp_initial.png")

tour_dist = lg.tour_distance(points, tour)
print('Initial tour distance = %0f' % tour_dist)

# initial values
list_tours = []
list_tours.append(tour)
list_dists = []
list_dists.append(tour_dist)
best_dists = []
best_dists.append(tour_dist)
curr_dist  = tour_dist

# GRASP METHOD
iterations = 2000
for k in range(iterations):
    node1 = 0
    node2 = 0
    while (node1 == node2):
        node1 = random.randint(0,ncoor-1)
        node2 = random.randint(0,ncoor-1)
    idx1 = tour.index(node1)
    idx2 = tour.index(node2)
    tour[idx1] = node2
    tour[idx2] = node1
    dist = lg.tour_distance(points, tour)
    list_dists.append(dist)
    if (dist > curr_dist): # restore path
        tour[idx1] = node1
        tour[idx2] = node2
    else:
        print('Swap node %d with node %d' % (node1, node2))
        print('New tour %s'    % tour)
        print('distance = %0f' % dist)
        best_dists.append(dist)
        curr_dist = dist 

plt.figure()
lg.plot_tour(points, tour)
adjust_plot('TSP - Best Tour Found')
plt.savefig("ex14_tsp_best.png")

plt.figure()
plt.plot(list_dists,'r.')
plt.ylim(0,10)
plt.xlim(0,iterations-1)
plt.grid()
plt.title('Distance reduction')
plt.savefig("ex14_tsp_distances.png")

plt.figure()
plt.plot(best_dists,'r.')
plt.ylim(0,10)
plt.xlim(0,len(best_dists)-1)
plt.grid()
plt.title('Distance reduction')
plt.savefig("ex14_tsp_best_dists.png")
