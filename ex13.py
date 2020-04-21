################################################################################
#   OS11 LOGISTICS
#
#   Author   : Orge, Fernando Gabriel
#   Exercise : EX13 - 
################################################################################
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
import operator
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
plt.savefig("images/ex13_tsp_cities.png")

# HYPER PARAMETERS
POP_SIZE   = 1000
ELITE_SIZE = 100
MUT_RATE   = 0.05

chromosome = [x for x in range(0,ncoor)]
population = lg.get_population(chromosome, POP_SIZE)
results    = lg.rank_routes(population, points)

no_imp    = 0
limit     = 100
list_tour = []
list_dist = []
best_dist = math.inf
while (no_imp < limit):
    parents    = lg.perform_selection(results, ELITE_SIZE)
    population = lg.get_next_generation(parents, MUT_RATE, points)
    population.sort(key = operator.itemgetter(1))
    curr_tour  = population[0][0]
    curr_dist  = population[0][1]
    if curr_dist < best_dist:
        best_dist = curr_dist
        list_tour.append(curr_tour)
        list_dist.append(curr_dist)
    else:
        no_imp = no_imp+1
        
print('Final results')
print('Best tour: %s ' % list_tour[-1])
print('Best dist: %0f' % list_dist[-1])
for d in list_dist:
    print(d)

for k in range(len(list_tour)):
    plt.figure(k)
    lg.plot_tour(points, list_tour[k])
    adjust_plot('TSP - Tour Found # %d' % k)
    plt.savefig("images/ex13_tsp_best_"+str(k)+".png")

    
