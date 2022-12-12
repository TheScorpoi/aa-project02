import random
import networkx as nx

# Returns a random subset of the given list
# Returns a random subset of the given list
def random_subset(lst):
    subset = []
    for i in range(len(lst)):
        if random.random() < 0.5:
            subset.append(lst[i]["name"])
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
def find_clique(graph):
    # Keep generating random subsets until we find a clique
    while True:
        subset = random_subset(graph.nodes)
        if is_clique(graph, subset):
            return subset

    return None


# Generate a random graph using the Erdos-Renyi model
G = nx.erdos_renyi_graph(10, 0.5)

# Use the find_clique function to find a clique in the graph
clique = find_clique(G)

# Print the clique
print(clique)
