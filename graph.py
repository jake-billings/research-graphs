import numpy
import networkx as nx
import gui


# Count the edges in an adjacency matrix
# Source: Lesson in Math class
def count_edges(matrix):
    squared = numpy.dot(matrix, matrix)
    diagonal = numpy.diagonal(squared)
    diagonal_sum = numpy.sum(diagonal)
    return diagonal_sum/2


# Count the triangles in an adjacency matrix
# See: https://en.wikipedia.org/wiki/Adjacency_matrix#Matrix_powers
def count_triangles(matrix):
    squared = numpy.dot(matrix, matrix)
    cubed = numpy.dot(squared, matrix)
    diagonal = numpy.diagonal(cubed)
    diagonal_sum = numpy.sum(diagonal)
    return diagonal_sum/6


# Test for triangles in an adjacency matrix
def test_triangles(matrix):
    return count_triangles(matrix) > 0


# Test for triangles in an adjacency matrix
def test_quads(matrix):
    squared = numpy.dot(matrix, matrix)

    for i in range(1,len(squared)-1):
        for j in (i+1,len(squared[i])-1):
            if squared[i, j] > 1:
                return True

    return False


# Test for hexes in an adjacency matrix
def test_hexes(matrix):
    squared = numpy.dot(matrix, matrix)
    cubed = numpy.dot(squared, matrix)

    for i in range(1, len(cubed)-1):
        for j in (i+1, len(cubed[i])-1):
            if cubed[i, j] > 1 and matrix[i, j] == 0:
                return True

    return False


# A graph follows the rules if it contains no c3, c4, or c6 cycles.
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
        sub_layer=tree(width, depth-1,root=node,node_index=node)
        layer += sub_layer
        node_index += len(sub_layer)

    return layer


# Wrap the result of tree() in a networkx Graph
def treex(width, depth, node_index=1):
    G=nx.Graph()
    G.add_weighted_edges_from(tree(width,depth,node_index))
    return G


if __name__ == "__main__":
    G = treex(3, 2)

    print "Follows rules: ", does_follow_rules(nx.to_numpy_matrix(G))
    print G.edges()

    # Draw the graph containing the tree with two connected branches
    gui.draw_network(G)