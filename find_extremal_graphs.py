# This is a work-in-progress psuedocode file for the final extremal graph finding algorithm
from math import pow, sqrt, floor
from OptimizedGraph import OptimizedGraph


# upper_bound()
#
# equivalent to f(n) from the dissertation (2.3) pg. 31
# see 2.1.2 on pg 25 of the dissertation
#
# equivalent
def upper_bound(n):
    return floor(((n / 12.0) * (pow(((108.0 * n) - 188.0 + (12.0 * sqrt(3.0)) * sqrt(83.0 - (94.0 * n) + (27.0 * n * n))), 1.0/3.0))) \
     - ((n / 12.0) * (pow(((-108.0 * n) + 188.0 + (12.0 * sqrt(3.0)) * sqrt(83.0 - (94.0 * n) + (27.0 * n * n))), 1.0/3.0))) \
     + (n / 3.0))


# find_extremal_graph_size()
#
# equivalent to s(n) from the dissertation (2.3) pg. 31
#
# finds the size of an extremal graph on n vertices that follows the restrictions of this research:
#
# A graph follows the rules if it contains no c3, c4, or c6 cycles.
def find_extremal_graph_size(n):
    # FOR tree type in tree types
        # make tree with type
            # WHILE there's space in the tree,
                # add an edge
                # IF the graph now contains a cycle, remove the edge.
                # IF the graph has reached one of the following bounds, it is an extremal graph, so return.
                    # 1. E >= 1/2q(q+1)^2 (https://faculty.math.illinois.edu/~z-furedi/PUBS/furedi_C4from1988.pdf)
                    # 2. Bound from Huntington's research
    # Init an empty graph data structure of size n
    graph = OptimizedGraph(n)

    # calculate the upper bound edge count for a graph of this size that follows the rules
    upper_bound_n = upper_bound(n)

    # Naively try to add all the edges
    for i in range(0, n):
        for j in range(0, n):
            if i != j:
                # Add an edge
                graph.add_edge(i, j)

                # check if the graph follows the rules
                #  if not, remove the edge
                if not graph.does_follow_rules():
                    graph.remove_edge(i, j)

                # if we reached the bound, we are one of the extremal graphs
                if graph.size >= upper_bound_n:
                    return graph.size

    return graph.size


# test():
#
# test our functions using known values from the dissertation (2.3) pg. 31
def test():
    print 'Testing upper_bound()'
    assert upper_bound(6) == 6
    assert upper_bound(7) == 7
    assert upper_bound(8) == 9
    assert upper_bound(9) == 11
    assert upper_bound(10) == 12
    assert upper_bound(11) == 14
    assert upper_bound(12) == 16
    assert upper_bound(13) == 18
    assert upper_bound(14) == 20
    assert upper_bound(14) == 20
    assert upper_bound(15) == 22
    assert upper_bound(16) == 24
    print 'Passed.'

    print 'Testing find_extremal_graph_size()'
    assert find_extremal_graph_size(6) == 6
    assert find_extremal_graph_size(7) == 7
    print find_extremal_graph_size(8), 'should be', 9
    print find_extremal_graph_size(9), 'should be', 10
    print find_extremal_graph_size(10), 'should be', 12
    print find_extremal_graph_size(11), 'should be', 13
    # assert find_extremal_graph_size(8) == 9
    # assert find_extremal_graph_size(9) == 10
    # assert find_extremal_graph_size(10) == 12
    # assert find_extremal_graph_size(11) == 13
    # assert find_extremal_graph_size(12) == 15
    # assert find_extremal_graph_size(13) == 17
    # assert find_extremal_graph_size(14) == 18
    # assert find_extremal_graph_size(15) == 20
    # assert find_extremal_graph_size(16) == 22


# if anybody bothers to run this, run the test() function
if __name__ == '__main__':
    test()
