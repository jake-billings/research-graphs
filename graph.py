import numpy
import networkx as nx
import gui

# Count the triangles in an adjacency matrix
# See: https://en.wikipedia.org/wiki/Adjacency_matrix#Matrix_powers
def count_triangles(matrix):
    print "matrix"
    print matrix
    squared = numpy.dot(matrix, matrix)
    cubed = numpy.dot(squared, matrix)
    print "cubed"
    print cubed
    diagonal = numpy.diagonal(cubed)
    print "diagonal"
    print diagonal
    diagonal_sum = numpy.sum(diagonal)
    print "diagonal sum", diagonal_sum
    return diagonal_sum/6

# Count the edges in an adjacency matrix
# Source: Lesson in Math class
def count_edges(matrix):
    print "matrix"
    print matrix
    squared = numpy.dot(matrix, matrix)
    print "squared"
    print squared
    diagonal = numpy.diagonal(squared)
    print "diagonal"
    print diagonal
    diagonal_sum = numpy.sum(diagonal)
    print "diagonal sum", diagonal_sum
    return diagonal_sum/2


# Recursively generate edges for a tree graph
# width describes the number of branches to create at each node. width is n where the desired tree is an n tree
# depth the number of recursions to perform. Depth levels of tree will be generated from the first node.
def tree(width, depth, root=1, node_index=1):
    layer = []
    if depth is 0:
        return []
    for i in range(root, root+width):
        node_index+=1
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
    # Generate a tree of width 3 with a depth of 1
    G = treex(4,2)

    # Count the triangles and print the edges (there should be 0 triangles)
    print count_triangles(nx.to_numpy_matrix(G)), "triangles in a basic tree graph:"
    print G.edges()

    # Add an edge connecting two branches. This creates a triangle.
    G.add_edge(2,3)

    # Count the triangles and print the edges of the new tree (there should be 1 triangle)
    print count_triangles(nx.to_numpy_matrix(G)), "triangles in a tree graph where two branches have been connected:"
    print G.edges()

    # Draw the graph containing the tree with two connected branches
    gui.draw_network(G)