# The following is a transcription of Dr. Michael Huntington's code from his doctoral dissertation
# As a result, the following code is Copyright Jake Billings 2017 All Rights Reserved.
# Unless Dr. Michael Huntington, the original author of the MAGMA implementation claims it. In this case,
# the code is copyright Dr. Michael Huntington 2017.

import numpy
import networkx as nx
import graph


# Throughout the code it becomes necessary to make sure that the graphs we are working with do not have 3, 4 or
# 6-cycles. The following three programs do this by looking at various powers of the adjacency matrix.
# From Huntington's dissertation
#
# x A networkx graph
def c3free(x):
    m = nx.to_numpy_matrix(x)
    squared = numpy.dot(m, m)
    cubed = numpy.dot(squared, m)
    diagonal = numpy.diagonal(cubed)
    return numpy.sum(diagonal)


# Throughout the code it becomes necessary to make sure that the graphs we are working with do not have 3, 4 or
# 6-cycles. The following three programs do this by looking at various powers of the adjacency matrix.
# From Huntington's dissertation
#
# x A networkx graph
def c4free(x):
    m = nx.to_numpy_matrix(x)
    m1 = numpy.dot(m, m)

    for i in range(1, len(m1) - 1):
        for j in (i + 1, len(m1[i]) - 1):
            if m1[i, j] > 1:
                return m1[i, j]

    return 0


# Throughout the code it becomes necessary to make sure that the graphs we are working with do not have 3, 4 or
# 6-cycles. The following three programs do this by looking at various powers of the adjacency matrix.
# From Huntington's dissertation
#
# x A networkx graph
def c6free(x):
    m = nx.to_numpy_matrix(x)
    squared = numpy.dot(m, m)
    m1 = numpy.dot(squared, m)

    for i in range(1, len(m1) - 1):
        for j in (i + 1, len(m1[i]) - 1):
            if m1[i, j] > 1 and m[i, j] == 0:
                return m1[i, j]

    return 0


# This function calls the three previous functions and tests to see if any 3, 4 or 6-cycles are present, it returns true
# if none of these cycles are present and false otherwise.
# From Huntington's dissertation
#
# G A networkx graph
def check(G):
    s = c3free(G)
    t = c4free(G)
    u = c6free(G)

    if s+t+u == 0:
        return True
    else:
        return False


# Returns the size of the graph in the set of graphs L with the greatest number of edges
#
# "Given a list of graphs this next function returns the largest number of edges of the given
# graphs. Often in our search we would find suboptimal graphs and needed a way to discard these, this showed which
# graphs we should keep."
# From Huntington's dissertation
#
# L A list of networkx graphs
def maxedges(L):
    H = []
    for x in L:
        s = x.number_of_edges()
        exists_greater = False
        for y in H:
            if y > s:
                exists_greater = True
        if not exists_greater:
            H.append(s)
    return H[len(H)-1].number_of_edges()


# Returns a filtered version of the list of graphs L in which only a single version of each
# isomorphic graph remains.
#
# "Often given a list of graphs many would be isomorphic. This function shortens the list by keeping only one isomorphic
# copy of each graph."
# From Huntington's dissertation
#
# L A list of networkx graphs
def iso(L):
    H = []
    for x in L:
        found_iso = False
        for g in H:
            if nx.is_isomorphic(x, g):
                found_iso = True
        if not found_iso:
            H.append(x)
    return H


# Returns a filtered version of a list of graphs including only graphs of the specified size e
#
# "This next function takes a list of graphs and returns a new list of graphs of the given size."
# From Huntington's dissertation
#
# T A list of networkx graphs
# e A whole number representing the desired number of edges in the returned list L
def extgraph(T, e):
    L = []
    for x in T:
        if x.number_of_edges() == e:
            L.append(x)
    return L


if __name__ == "__main__":
    # Create a tree.
    G = graph.treex(3, 2)

    # This edge creates a 3-cycle. Commenting it out should cause this program to print True
    G.add_edge(2, 7)

    # Create a tree.
    G2 = graph.treex(4, 2)
    G3 = graph.treex(1, 4)

    L = [G, G2, G3]

    print G.number_of_edges()
    print G2.number_of_edges()
    print G3.number_of_edges()

    print maxedges(L)

    print extgraph(L, 13)

    # Should print False
    print check(G)
