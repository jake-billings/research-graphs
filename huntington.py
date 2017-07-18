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
def c3free(x):
    m = nx.to_numpy_matrix(x)
    squared = numpy.dot(m, m)
    cubed = numpy.dot(squared, m)
    diagonal = numpy.diagonal(cubed)
    return numpy.sum(diagonal)


# From Huntington's dissertation
def c4free(x):
    m = nx.to_numpy_matrix(x)
    m1 = numpy.dot(m, m)

    for i in range(1, len(m1) - 1):
        for j in (i + 1, len(m1[i]) - 1):
            if m1[i, j] > 1:
                return m1[i, j]

    return 0


# From Huntington's dissertation
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
def check(G):
    s = c3free(G)
    t = c4free(G)
    u = c6free(G)

    if s+t+u == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    # Create a tree.
    G = graph.treex(3, 2)

    # This edge creates a 3-cycle. Commenting it out should cause this program to print True
    G.add_edge(2, 7)

    # Should print False
    print check(G)
