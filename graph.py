import numpy
import networkx as nx
import gui


# Count the edges in an adjacency matrix
#
# matrix An adjacency matrix in the form of a 2D array that represents a networkx (or any other) graph
# see nx.to_numpy_matrix() to convert networkx graphs to adjacency matrices.
#
# Source: Lesson in Math class
def count_edges(matrix):
    squared = numpy.dot(matrix, matrix)
    diagonal = numpy.diagonal(squared)
    diagonal_sum = numpy.sum(diagonal)
    return diagonal_sum/2


# Count the triangles in an adjacency matrix
#
# matrix An adjacency matrix in the form of a 2D array that represents a networkx (or any other) graph
# see nx.to_numpy_matrix() to convert networkx graphs to adjacency matrices.
#
# See: https://en.wikipedia.org/wiki/Adjacency_matrix#Matrix_powers
def count_triangles(matrix):
    squared = numpy.dot(matrix, matrix)
    cubed = numpy.dot(squared, matrix)
    diagonal = numpy.diagonal(cubed)
    diagonal_sum = numpy.sum(diagonal)
    return diagonal_sum/6


# Test for triangles in an adjacency matrix
#
# matrix An adjacency matrix in the form of a 2D array that represents a networkx (or any other) graph
# see nx.to_numpy_matrix() to convert networkx graphs to adjacency matrices.
#
# see c3free() in Huntington's dissertation
def test_triangles(matrix):
    return count_triangles(matrix) > 0


# Test for quads in an adjacency matrix
#
# matrix An adjacency matrix in the form of a 2D array that represents a networkx (or any other) graph
# see nx.to_numpy_matrix() to convert networkx graphs to adjacency matrices.
#
# see c4free() in Huntington's dissertation
def test_quads(matrix):
    squared = numpy.dot(matrix, matrix)

    for i in range(1,len(squared)-1):
        for j in (i+1,len(squared[i])-1):
            if squared[i, j] > 1:
                return True

    return False


# Test for hexes in an adjacency matrix
#
# matrix An adjacency matrix in the form of a 2D array that represents a networkx (or any other) graph
# see nx.to_numpy_matrix() to convert networkx graphs to adjacency matrices.
#
# see c6free() in Huntington's dissertation
def test_hexes(matrix):
    squared = numpy.dot(matrix, matrix)
    cubed = numpy.dot(squared, matrix)

    for i in range(1, len(cubed)-1):
        for j in (i+1, len(cubed[i])-1):
            if cubed[i, j] > 1 and matrix[i, j] == 0:
                return True

    return False


# A graph follows the rules if it contains no c3, c4, or c6 cycles.
#
# matrix An adjacency matrix in the form of a 2D array that represents a networkx (or any other) graph
# see nx.to_numpy_matrix() to convert networkx graphs to adjacency matrices.
#
# see check() in Huntington's dissertation
# see does_follow_rules_optimized for a more efficient implementation
def does_follow_rules(matrix):
    # If contains 3 return false
    if test_triangles(matrix):
        print "Found trie"
        return False
    # If contains 4 return false
    if test_quads(matrix):
        print "Found quads"
        return False
    # If contains 6 return false
    if test_hexes(matrix):
        print "Found hexes"
        return False
    return True


# A graph follows the rules if it contains no c3, c4, or c6 cycles.
# This function is far less reader-friendly; however it is equivalent to
# does_follow_rules() and should run more quickly due to linearly decreased
# number of loops and matrix operations.
#
# matrix An adjacency matrix in the form of a 2D array that represents a networkx (or any other) graph
# see nx.to_numpy_matrix() to convert networkx graphs to adjacency matrices.
#
# see check() in Huntington's dissertation
# see does_follow_rules() for a more-readable but less efficient version
def does_follow_rules_optimized(matrix):
    # Square and cube the matrix
    squared = numpy.dot(matrix, matrix)
    cubed = numpy.dot(squared, matrix)

    # Test for tries and return false if they exist
    cubed_diagonal_sum = numpy.sum(numpy.diagonal(cubed))
    if cubed_diagonal_sum > 0:
        return False

    # Test for quads and return false if they exist
    for i in range(1,len(squared)-1):
        for j in (i+1,len(squared[i])-1):
            if squared[i, j] > 1:
                return False
            if cubed[i, j] > 1 and matrix[i, j] == 0:
                return False

    return True


# Recursively generate edges for a tree graph
# width describes the number of branches to create at each node. width is n where the desired tree is an n tree
# depth the number of recursions to perform. Depth levels of tree will be generated from the first node.
def tree(width, depth, root=1, node_index=1):
    layer = []
    if depth is 0:
        return []
    for i in range(root, root+width):
        node_index += 1
        node = node_index

        layer.append((root, node, 1))
        sub_layer = tree(width, depth-1,root=node,node_index=node)
        layer += sub_layer
        node_index += len(sub_layer)

    return layer


# Wrap the result of tree() in a networkx Graph
def treex(width, depth, node_index=1):
    G=nx.Graph()
    G.add_weighted_edges_from(tree(width,depth,node_index))
    return G


# Returns the size of the graph in the set of graphs with the greatest number of edges
#
# "Given a list of graphs this next function returns the largest number of edges of the given
# graphs. Often in our search we would find suboptimal graphs and needed a way to discard these, this showed which
# graphs we should keep."
# From Huntington's dissertation
#
# graphs A list of networkx graphs
# See maxedges() from Huntington's dissertation
def max_edges(graphs):
    highest_known_edge_count = 0
    for graph in graphs:
        edge_count = graph.number_of_edges()
        if edge_count > highest_known_edge_count:
            highest_known_edge_count = edge_count
    return highest_known_edge_count


# Returns a filtered version of the list of graphs L in which only a single version of each
# isomorphic graph remains.
#
# graphs An array of networkx graphs
#
# See iso() from Huntington's dissertation
def filter_by_isomorphic(graphs):
    # Initialize an array to hold the filtered graphs
    filtered_graphs = []

    # Iterate over the graphs passed to the function
    for graph in graphs:

        # Check if the graph is isomorphically unique compared to all other isomorphicallly
        # unique graphs we intend to return
        found_isomorphically_identical_graph = False
        for existing_isomorphically_unique_graph in filtered_graphs:
            if nx.is_isomorphic(graph, existing_isomorphically_unique_graph):
                found_isomorphically_identical_graph = True

        # If the graph is isomorphically unique, add it to the list of isomorphically uniuqe graphs
        if not found_isomorphically_identical_graph:
            filtered_graphs.append(graph)

    # Return the list of known isomorphically unique graphs
    return filtered_graphs


# Returns a filtered version of a list of graphs including only graphs of the specified size e
#
# "This next function takes a list of graphs and returns a new list of graphs of the given size."
# From Huntington's dissertation
#
# graph A list of networkx graphs
# edge_count A whole number representing the desired number of edges in the returned list L
#
# See extgraph() from Huntington's dissertation
def filter_by_edge_count(graphs, edge_count):
    filtered_graphs = []

    for graph in graphs:
        if graph.number_of_edges() == edge_count:
            filtered_graphs.append(graph)
    return filtered_graphs


if __name__ == "__main__":
    G = treex(3, 2)

    G.add_edge(2, 7)

    print "Follows rules: ", does_follow_rules_optimized(nx.to_numpy_matrix(G))
    print nx.to_numpy_matrix(G)
    print G.edges()

    # Draw the graph containing the tree with two connected branches
    gui.draw_network(G)