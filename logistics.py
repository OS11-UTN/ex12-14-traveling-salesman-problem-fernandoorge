#   OS11 LOGISTICS
#   Author: Orge, Fernando Gabriel
#   logistics package

import numpy as np
import math
import random
import matplotlib
import matplotlib.pyplot as plt

def count_ones(NN):
    """Return number of ones in Node-Node Matrix."""
    # Input  : NN   Node-Node Matrix
    # Output : int  number of ones in NN Matrix
    (row, col) = NN.shape
    elem       = 0
    for i in range (0, row):
        for j in range (0, col):
            if (NN[i,j] == 1):
                elem = elem + 1
    return elem

def count_non_zeros(NN):
    """Return number of non-zero elements in Node-Node Matrix."""
    # Input  : NN   Node-Node Matrix
    # Output : int  number of ones in NN Matrix
    (row, col) = NN.shape
    elem       = 0
    for i in range (0, row):
        for j in range (0, col):
            if (NN[i,j] > 0):
                elem = elem + 1
    return elem

def nn2na(NN):
    """Return Node-Arcs matrix based on Node-Node Matrix."""
    # Input  : NN       Node-Node Matrix
    # Output : NA       Node-Arc  Matrix
    # Output : arcs     arcs      list of tuples
    (row, col) = NN.shape
    elem = count_ones(NN)
    NA   = np.zeros((row, elem))
    k    = 0
    arcs = []
    for i in range (0, row):
        for j in range (0, col):
            if (NN[i,j] == 1):
                NA[i,k] = +1
                NA[j,k] = -1
                k       = k + 1
                arcs.append((i, j))
    return NA, arcs

def convert_arc(arc, nodes):
    """Return an equivalent arc but with names instead of integer values."""
    # Input  : arc      Tuple of integer values
    # Input  : nodes    list of Nodes names as string values
    # Output : carc     Converted Arc => Tuple of strings
    #
    # NOTES  : This function is used just for printing results 
    #          and for debugging purposes
    return (nodes[arc[0]], nodes[arc[1]])

def convert_path(path, nodes):
    """Return an equivalent path but with names instead of integer values."""
    # Input  : path     path as list of nodes
    #                   Nodes are assumed to be integer values
    # Input  : nodes    list of all nodes names in the graph
    #                   Nodes are assumed to be string values
    # Output : cpath    Converted path => list of strings
    #
    # NOTES  : This function is used just for printing results 
    #          and for debugging purposes
    cpath = []
    for k in range(0,len(path)):
        cpath.append(nodes[path[k]])
    return cpath
    
def get_arcs_from_node(G, src):
    """Return a list of outcoming arcs from src node in G."""
    # Input  : G        Graph modeled as Node-Node Matrix
    # Input  : src      Source Node as INTEGER value
    # Output : arcs     List of arcs as LIST of TUPLES
    (row, col) = G.shape
    arcs = []
    for dst in range(0, col):
        if G[src, dst] > 0:
            arcs.append((src, dst))
    return arcs

def dijkstra_alg(NN, nodes):
    """DIJKSTRA Algorithm"""
    # Input  : NN       Node-Node Matrix
    # Input  : nodes    list of all nodes names in the graph
    #                   Nodes are assumed to be string values
    # NOTES  : This function prints all the results
    (row, col) = NN.shape                                   # get NN dimensions
    n          = len(nodes)                                 # n == row == col
    if (row != col):
        print("ERROR: NN must be a square matrix")
        return
    if (n != row):
        print("ERROR: n != row")
        return

    dist  = np.zeros(n)                                     # distance vector
    pred  = np.zeros(n)                                     # predecessor vector
    label = np.zeros(n)                                     # 0=unlabeled, 1=labeled
    
    for k in range (1, n):
        dist[k] = math.inf                                  # initialization of distance vector

    for k in range (0, n):
        dist_min = math.inf                                 # restore upper bound
        i        = 0                                        # restore index
        for k in range(0, n):
            if (dist[k] < dist_min) and (label[k] == 0):    # find min distance of non-labeled nodes
                dist_min = dist[k]                          # update min distance if found
                i        = k                                # update index if found
        label[i] = 1                                        # label node when min distance found
        for arc in get_arcs_from_node(NN, i):
            j = arc[1]
            if dist[j] > (dist[i] + NN[i,j]):
                dist[j] = dist[i] + NN[i,j]                 # update distance vector
                pred[j] = i                                 # update predecessor vector

    path      = []                                          # shortest path               
    cum_dist  = []                                          # cumulative distance
    curr_node = n-1                                         # start with the last node
    path.insert(0,nodes[curr_node])                         # insert last node to path
    cum_dist.insert(0,dist[curr_node])                      # insert cumulative distance (solution)
    while (curr_node != 0):                                 # iterate till first node is reached
        pred_node = int(pred[curr_node])                    # find predecessor of current node
        path.insert(0,nodes[pred_node])                     # insert predecessor into the path
        cum_dist.insert(0,dist[pred_node])                  # update cumulative distance vector
        curr_node = pred_node                               # predeccesor is now the current node
        
    print("\t Shortest path solution: %s" % path)
    print("\t Cumulative distance   : %s" % cum_dist)
    print("\t Minimum distance      : %d" % cum_dist[-1])
    print("")
    
def dfs(G, i, j):
    """Return a path from i to j in G if at least one path exists."""
    # Input  : G        Graph               as Node-Node Matrix
    # Input  : i        source node         as INTEGER value
    # Input  : j        destination node    as INTEGER value
    # Output : path     found path          as LIST of INTEGERS
    (row, col) = G.shape
    label = [ 0 for col in range(row)]
    pred  = [-1 for col in range(row)]
    path  = []
    s     = []
    s.insert(0,i)
    while (len(s) != 0):
        v = s.pop()
        if (label[v] == 0):
            label[v] = 1
            for arc in get_arcs_from_node(G, v):
                pred[arc[1]] = v
                s.insert(0,arc[1])
    if (label[j] != 0):
        path.insert(0, j)
        while (label[j] == 1 and pred[j] >= 0):
            j = pred[j]
            path.insert(0, j)
    return path
    
def max_flow_across_path(path, G):
    """Return the maximum flow across any given path in G"""
    # Input  : path     path                as LIST of INTEGERS
    # Input  : G        Graph               as Node-Node Matrix
    # Output : flow     maximum flow        as INTEGER value
    # Notes  : The maximum flow across a path is equal to the minimum cost of 
    #          all the arcs, since the arc with the minimun cost is the cut.
    c = []
    for k in range(0, len(path)-1):
        i = path[k]
        j = path[k+1]
        c.append(G[i,j])
    return min(c)
    
def ford_fulk(G, s, t):
    """Return max flow across s->t in G using Ford-Fulkerson Algorithm."""
    # Input  : G        Graph               as Node-Node Matrix
    # Input  : s        source node         as INTEGER value
    # Input  : t        destination node    as INTEGER value
    # Output : flow     maximum flow        as INTEGER value
    # Output : fbG      Feedback G          as Node-Node Matrix
    #                                       it can be used to reconstruct the 
    #                                       paths that determines the max flow
    resG = G
    fbG  = np.zeros(G.shape)
    path = dfs(G, s, t)
    flow = 0
    while (path != []):
        maxc = max_flow_across_path(path, resG)
        flow += maxc
        for k in range(0, len(path)-1):
            resG[path[k], path[k+1]] -= maxc
            fbG[path[k+1], path[k]]  -= maxc
        path = dfs(resG, s, t)
    return flow, fbG
    
def full_graph(dim):
    """Return the Node-Node Matrix of a full graph."""
    # Input  : dim      dimension           as integer value
    # Output : G        Node-Node Matrix    as {dim x dim} matrix of integers   
    G = np.zeros((dim, dim))
    for i in range(0, dim):
        for j in range(0, dim):
            if (i != j):
                G[i,j] = 1
    return G
    
def get_random_points(num):
    """Return a list of random points (x,y) in [0,1)X[0,1)."""
    # Input  : num      number of points    as integer value
    # Output : points   list of points      as list of tuples
    points = []
    for k in range(0, num):
        x = random.randint(0,100) / 100
        y = random.randint(0,100) / 100
        points.append((x,y))
    return points

def distance(p1, p2):
    """Return distance between p1 and p2."""
    # Input  : p1       point1 (x,y)    as tuple
    # Input  : p2       point2 (x,y)    as tuple
    # Output : distance dist(p1,p2)     as real
    return (math.sqrt( pow(p2[0]-p1[0],2) + pow(p2[1]-p1[1],2) ))
    
def first_value(iterable, value):
    """Return the index of the first appearance of value in iterable."""
    # Input  : iterable                 as any iterable
    # Input  : value                    as any element in the iterable
    # Output : idx          index       as integer value
    idx = -1
    for k in range(0, len(iterable)):
        if (iterable[k] == value):
            idx = k
            break
    return idx
            
def get_subtours(connections):
    """@TODO."""
    length   = len(connections)
    labeled  = [0 for col in range(length)]
    subtours = []
    while ( sum(labeled) < length ):
        path      = []
        init_node = first_value(labeled, 0)
        curr_node = init_node
        next_node = math.inf
        while (init_node != next_node):
            path.append(curr_node)
            labeled[curr_node] = 1
            next_node = connections[curr_node].index(1)
            curr_node = next_node
        subtours.append(path)
    return subtours
    
def plot_tour(points, tour):
    """@TODO."""
    x = [tup[0] for tup in points] 
    y = [tup[1] for tup in points]
    plt.plot(x, y, 'ro')
    for k in range(0, len(tour)):
        if (k == len(tour)-1):
            xseg = [x[tour[k]], x[tour[0]]]
            yseg = [y[tour[k]], y[tour[0]]]
            plt.plot(xseg, yseg, 'b-.')
        else:
            xseg = [x[tour[k]], x[tour[k+1]]]
            yseg = [y[tour[k]], y[tour[k+1]]]
            plt.plot(xseg, yseg, 'b-.')
            
def tour_distance(points, tour):
    dist = 0
    x = [tup[0] for tup in points] 
    y = [tup[1] for tup in points]
    for k in range(0, len(tour)):
        if (k == len(tour)-1):
            dist += math.sqrt(pow(x[tour[0]]  -x[tour[k]],2) + pow(y[tour[0]]  -y[tour[k]],2))
        else:
            dist += math.sqrt(pow(x[tour[k+1]]-x[tour[k]],2) + pow(y[tour[k+1]]-y[tour[k]],2))
    return dist
