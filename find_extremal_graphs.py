# This is a work-in-progress psuedocode file for the final extremal graph finding algorithm
from math import pow, sqrt, floor


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


# find_extremal_graph
#
# equivalent to s(n) from the dissertation (2.3) pg. 31
#
# finds an extremal graph for n vertices that follows the restrictions of this research:
#
# A graph follows the rules if it contains no c3, c4, or c6 cycles.
def find_extremal_graph(n):
    # FOR tree type in tree types
        # make tree with type
            # WHILE there's space in the tree,
                # add an edge
                # IF the graph now contains a cycle, remove the edge.
                # IF the graph has reached one of the following bounds, it is an extremal graph, so return.
                    # 1. E >= 1/2q(q+1)^2 (https://faculty.math.illinois.edu/~z-furedi/PUBS/furedi_C4from1988.pdf)
                    # 2. Bound from Huntington's research
    pass


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


# if anybody bothers to run this, run the test() function
if __name__ == '__main__':
    test()
