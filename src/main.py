import random
import networkx as nx
from vertex import Vertex
from point import Point
import matplotlib.pyplot as plt
import time
from prettytable import PrettyTable
import psutil
import collections


random.seed(98491)

def generate_graph(vertexs_number: int, percentage: int):
    
    points = [(Point(random.randint(1, 20), random.randint(1, 20))) for i in range(vertexs_number)]
    vertexs = [(Vertex(i, points[i])) for i in range(vertexs_number)]
    vertex_label = [vertex.id for vertex in vertexs]

    edges_number = round(((vertexs_number*(vertexs_number-1))/2)*(percentage/100))
    edges = list()
    visited = list()
    adj_list = dict()
    unvisited = vertex_label
    
    for i in range(edges_number):
        if len(edges) == 0:  # initial case: pick 2 random unvisited vertexes to form the first edge
            two_random_vertexs = random.sample(unvisited, 2)
            edges.append(tuple(sorted(two_random_vertexs)))
            unvisited = list(set(unvisited) - set(two_random_vertexs))
            visited = list(set(visited).union(two_random_vertexs))
        elif len(unvisited) != 0:  # general case:
            vertex_1 = random.choice(unvisited)
            vertex_2 = random.choice(visited)
            edges.append(tuple(sorted([vertex_1, vertex_2])))
            unvisited.remove(vertex_1)
        else:
            edges.append(tuple(sorted(random.sample(vertex_label[:vertexs_number], 2))))
            
    # generate adjacency list
    for node1, node2 in sorted(edges):
        if node1 in adj_list:
            adj_list[node1].append(node2)
        else:
            adj_list[node1] = [node2]
        if node2 in adj_list:
            adj_list[node2].append(node1)
        else:
            adj_list[node2] = [node1]

    return vertexs, edges, adj_list

def random_subset(vertices, k):
    #Ensure that the subset is unique and no solution is testes more than once
    tested_subsets = []
    
    subset = random.sample(vertices, k)
    if subset not in tested_subsets:
        tested_subsets.append(subset)
        return subset
    else:
        return random_subset(vertices, k)

# Returns True if the given subset of vertices forms a clique in the given graph, False otherwise
def is_clique(vertices, edges):
    edges_set = set(edges)
    # Check if each pair of vertices is connected by an edge
    for i, v1 in enumerate(vertices):
        for v2 in vertices[i+1:]:
            if (v1, v2) not in edges_set and (v2, v1) not in edges_set:
                return False
    return True

# Returns a clique in the given graph, or None if one does not exist
def find_clique_2(graph, edges, k):
    vertices = list(graph.keys())
    A = time.time()
    
    counter = 0
    
    while time.time() - A < 5: #The algorithm will run for 20 seconds 
        counter += 1
        subset = random_subset(vertices, k)
        if is_clique(subset, edges):
            return True, counter
        else:
            continue
    return False, counter

def plot_graph(e):
    G = nx.Graph()
    for edge in e:
        G.add_edge(edge[0], edge[1])
    nx.draw(G, node_size=700, with_labels=True)
    plt.show()
    
def pick_random(s):
    if s:
        elem = s.pop()
        s.add(elem)
        return elem

def bron_kerbosch(clique, candidates, excluded, NEIGHBORS):
    global cliques_list
    if not candidates and not excluded:
        if len(clique) >= 1:
            cliques_list.append(clique)
        return
 
    pivot = pick_random(candidates) or pick_random(excluded)
    for v in list(candidates.difference(NEIGHBORS[pivot])):
        new_candidates = candidates.intersection(NEIGHBORS[v])
        new_excluded = excluded.intersection(NEIGHBORS[v])
        bron_kerbosch(clique + [v], new_candidates, new_excluded, NEIGHBORS)
        candidates.remove(v)
        excluded.add(v)

def get_adj_list_in_a_set(graph):
    neighbors = collections.defaultdict(set)
    for vertice, adajacent_vertices in graph.items():
        for a_d in adajacent_vertices:
            if a_d != vertice:
                neighbors[a_d].add(vertice)
                neighbors[vertice].add(a_d)
    return neighbors

def internet_graphs():
    global cliques_list
    graph = nx.Graph()

    adj_list = dict()

    with open('../SW_ALGUNS_GRAFOS/SWlargeG.txt', 'r') as f:
        for line in f:
            graph.add_edge(line.split()[0],line.split()[1])

    for node1, node2 in sorted(graph.edges):
            if node1 in adj_list:
                adj_list[node1].append(node2)
            else:
                adj_list[node1] = [node2]
            if node2 in adj_list:
                adj_list[node2].append(node1)
            else:
                adj_list[node2] = [node1]
    #250
    #1273
    
    k = int(100000*12.5 / 100)
    
    neighbors = get_adj_list_in_a_set(adj_list)
    
    cliques_list = []
    bron_kerbosch([], set(graph.nodes()), set(), neighbors)
    result = False
    for cliq in cliques_list:
        if len(cliq) == k or k==1:
            result = True
            break
    print(result)

#l = []
#for i in nx.find_cliques(graph):
#    if len(i) not in l:
#        l.append(len(i))
#print(l)
#plot_graph(e)
#A = time.time()
#print(find_clique_2(adj_list, e, 6))
#print("time: ", time.time() - A)

def write_results():
    with open('../results/results_2.txt', 'w') as f:
        f.write("Nodes,Percentagem,Edges,Perc_k,k,Result,Basic_Operations,Time,Memory\n")
        for i in range(10, 80):
            for p in [12.5, 25, 50, 75]:
                v,e, adj_list = generate_graph(i, p)
                graph = nx.Graph()
                for edge in e:
                    graph.add_edge(edge[0],edge[1])
                for j in [12.5, 25, 50, 75]:
                    A = time.time()
                    mem1 = psutil.virtual_memory().used # total physical memory in Bytes
                    k = int(i * j / 100)
                    result, counter = find_clique_2(adj_list, e, k)
                    mem2 = psutil.virtual_memory().used  # total physical memory in Bytes
                    f.write(str(i) + "," + str(p) + "," + str(len(e)) + "," + str(j) + "," + str(k) + "," + str(result) + "," + str(counter) + "," + str(time.time() - A) + "," + str((abs(mem2 - mem1))/2**(20)) + "\n")
                
                
                
if __name__ == "__main__":
    internet_graphs()    