import random

# This function takes a graph represented as an adjacency matrix
# and a positive integer k as inputs and returns True if the
# graph contains a k-clique, and False otherwise.
def k_clique(adj_matrix, k):
  # Initialize an empty set to store the vertices in the clique
  clique = set()

  # Get the number of vertices in the graph
  n = len(adj_matrix)

  # Initialize the number of vertices in the clique to 0
  clique_size = 0

  # Keep selecting random vertices until a k-clique is found
  while clique_size < k:
    # Choose a random vertex in the graph
    v = random.randint(0, n-1)

    # Initialize the number of neighbors of v that are
    # already in the clique to 0
    neighbor_count = 0

    # Check each vertex in the graph to see if it is
    # adjacent to v and already in the clique
    for i in range(n):
      # If i is adjacent to v and is already in the clique,
      # increment the neighbor count
      if adj_matrix[v][i] and i in clique:
        neighbor_count += 1

    # If the number of neighbors of v that are already in the
    # clique is equal to k-1, then v can be added to the clique
    if neighbor_count == k-1:
      clique.add(v)
      clique_size += 1

  # If the size of the clique is equal to k, then the
  # graph contains a k-clique, so return True
  if clique_size == k:
    return True

  # Otherwise, the graph does not contain a k-clique,
  # so return False
  return False


import random

# This function takes a graph represented as an adjacency matrix
# (in the form of a dictionary) and a positive integer k as
# inputs and returns True if the graph contains a k-clique,
# and False otherwise.
def k_clique_dict_matrix(adj_matrix, k):
  # Initialize an empty set to store the vertices in the clique
  clique = set()

  # Get the number of vertices in the graph
  n = len(adj_matrix)

  # Initialize the number of vertices in the clique to 0
  clique_size = 0

  # Keep selecting random vertices until a k-clique is found
  while clique_size < k:
    # Choose a random vertex in the graph
    v = random.randint(0, n-1)

    # Initialize the number of neighbors of v that are
    # already in the clique to 0
    neighbor_count = 0

    # Check each vertex in the graph to see if it is
    # adjacent to v and already in the clique
    for i in range(n):
      # If i is adjacent to v and is already in the clique,
      # increment the neighbor count
      if i in adj_matrix[v] and i in clique:
        neighbor_count += 1

    # If the number of neighbors of v that are already in the
    # clique is equal to k-1, then v can be added to the clique
    if neighbor_count == k-1:
      clique.add(v)
      clique_size += 1

  # If the size of the clique is equal to k, then the
  # graph contains a k-clique, so return True
  if clique_size == k:
    return True

  # Otherwise, the graph does not contain a k-clique,
  # so return False
  return False


