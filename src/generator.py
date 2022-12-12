from vertex import Vertex
from point import Point
import random
import time
import networkx as nx

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

def find_clique(g):
      # g is a graph represented as a adjacency matrix
  n = len(g)  # number of vertices in the graph

  # Keep track of the largest clique found so far
  largest_clique = []

  # Iterate a fixed number of times
  for _ in range(1000):
    # Choose a random subset of the vertices
    vertex_subset = random.sample(range(n), n//2)

    # Check if the subset forms a clique
    is_clique = True
    for i in range(len(vertex_subset)):
      for j in range(i+1, len(vertex_subset)):
        if g[vertex_subset[i]][vertex_subset[j]] == 0:
          is_clique = False
          break
      if not is_clique:
        break

    # If the subset is a clique and it's larger than the previous largest clique,
    # update the largest clique
    if is_clique and len(vertex_subset) > len(largest_clique):
      largest_clique = vertex_subset

  return largest_clique

def random_subset(lst):
    subset = []
    for i in range(len(lst)):
        if random.random() < 0.5:
            subset.append(lst[i])
    return subset

# Returns True if the given subset of vertices forms a clique
# in the given graph, False otherwise
def is_clique(graph, subset):
    for i in range(len(subset)):
        for j in range(i + 1, len(subset)):
            if not graph[subset[i]][subset[j]]:
                return False
    return True

# Returns a clique in the given graph, or None if one does not exist
def find_clique_2(graph):
    # Keep generating random subsets until we find a clique
    while True:
        subset = random_subset(graph.vertices)
        if is_clique(graph, subset):
            return subset

    return None




# This function takes a graph represented as an adjacency matrix
# (in the form of a dictionary) and a positive integer k as
# inputs and returns True if the graph contains a k-clique,
# and False otherwise.
def k_clique(adj_matrix, k):
  # Initialize an empty set to store the vertices in the clique
  clique = set()

  # Get the number of vertices in the graph
  n = len(adj_matrix)
  
  # Initialize the number of vertices in the clique to 0
  clique_size = 0

  # Set the maximum number of vertices to consider before
  # stopping the search for a k-clique
  max_vertices = n

  # Initialize a counter for the number of vertices considered so far to 0
  vertices_considered = 0

  # Keep selecting random vertices until a k-clique is found
  # or the maximum number of vertices is reached
  while clique_size < k and vertices_considered < max_vertices:
    # Choose a random vertex in the graph
    v = random.randint(0, n-1)
    print(v)

    # Initialize the number of neighbors of v that are
    # already in the clique to 0
    neighbor_count = 0

    # Check each vertex in the graph to see if it is
    # adjacent to v and already in the clique
    for i in range(n):
      # If i is adjacent to v and is already in the clique,
      # increment the neighbor count
        print("i: ", i , " -- adj_matrizx[v] ", adj_matrix[v])
        if i in adj_matrix[v]:
            print("entrei aqui")
            neighbor_count += 1
            print("neighbor_count: ", neighbor_count)

        # If the number of neighbors of v that are already in the
        # clique is equal to k-1, then v can be added to the clique
        if neighbor_count == k-1:
            clique.add(v)
            clique_size += 1

        # Increment the counter for the number of vertices considered
        vertices_considered += 1

  # If the size of the clique is equal to k, then the
  # graph contains a k-clique, so return True
  if clique_size == k:
        return True

  # Otherwise, if the size of the clique is less than k,
  # then the graph does not contain a k-clique, so return False
  elif clique_size < k:
    return False




if __name__ == "__main__":
    #for i in range(5, 80):
        #for p in [12.5, 25, 50, 75]:
    v,e, adj_list = generate_graph(5, 75)
    #print(len(adj_list))
    graph = nx.Graph()
    for edge in e:
        graph.add_edge(edge[0],edge[1])
        
    print(adj_list)
    print(k_clique(adj_list, 3))
                
                