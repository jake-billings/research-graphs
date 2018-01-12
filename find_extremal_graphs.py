# This is a work-in-progress psuedocode file for the final extremal graph finding algorithm


# find_extremal_graph
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
