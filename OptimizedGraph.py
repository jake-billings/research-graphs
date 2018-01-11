from time import time
import numpy # todo remove and move into test() once we don't need numpy in the class (after we update to the new checking)

# OptimizedGraph
#
# Undirected graph
#
# A data structure for storing graphs that is optimized for the specific cycle-checking algorithm
#  required for the research in this repository.
#
# More specifically, the brute-force graph search algorithm approaches the problem via an "add an edge and check"
#  method. The original code from Huntington's thesis computes far more matrix operations than necessary. The goal
#  of this algorithm is to minimize the calculation required to check if a cycle was added when a new edge is added.
#
# This structure is not recommended for any other application as it does not store the information effeciently for this
#  purpose.
#
# Additionally, I attempt to make abstractions that make it practical and convenient to convert this class to use a
#  simpler data structure such as node/edge arrays.
#
# Additionally, memory was a concern in the original algorithm, so an attempt is made to minimize memory consumption
#  by reducing the redundant information in the adjacency structure.
#
# Since we are working with simple undirected graphs, we can assume no node has an edge linking with itself and that
#  the adj matrix is symmetric over the diagonal. Thus, we can reduce the information stored to only the lower left.
#  The matrix values can also be stored as booleans instead of integers.
#
# Typical Adj Matrix: [[a, b, c],
#                      [d, e, f],
#                      [g, h, i]]
#
# We know a, e, and i are false. We know b=d, c=g, h=f. Thus we need only store the following:
#
# self.adjacency_structure: [[d],
#                           [g, h]]
#
# Since we're optimizing for cycle checking we will need to use the squared adjacency matrix. However, since we're
#  only adding/removing one edge at a time, we can reduce computational overhead by caching the square matrix and
#  updating only affected rows when edges are added and removed. Unfortunately, the diagonal cannot be compressed
#  in the square matrix, so it must be stored. However, the square matrix is still symmetrical, so the upper right
#  can still be discarded. Additionally, the square_adjacency_structure must be stored as numeric/integer values
#  instead of booleans.
#
# self.square_adjacency_structure: [[p],
#                                   [q, w],
#                                   [x, y, z]]
#
# This matrix is updated upon calls to write_adjacency_matrix.
class OptimizedGraph:
    # __init__()
    #
    # constructor
    #
    # performs initialization of graph structure
    def __init__(self, size):
        # Store size and define an array to hold adjacency structures
        self.size = size
        self.adjacency_structure = []
        self.square_adjacency_structure = []

        # Generate an empty adjacency structure for the given size
        #  See class docs for details on adjacency structure
        for row in range(0, size - 1):
            self.adjacency_structure.append([])
            for column in range(0, row + 1):
                self.adjacency_structure[row].append(False)

        # Generate an empty square structure for the given size
        #  See class docs for details on square adjacency structure
        #  square needs to include a diagonal that adjacency_structure does not
        for row in range(0, size):
            self.square_adjacency_structure.append([])
            for column in range(0, row + 1):
                self.square_adjacency_structure[row].append(0)

    # read_adjacency_matrix_bool()
    #
    # Returns BOOLEAN because boolean is the underlying data type
    #
    # Accesses the theoretical adjacency matrix of this graph; we only store a much smaller adjacencyStructure
    #  since the graph is assumed to be simple and undirected. See class docs for more.
    def read_adjacency_matrix_bool(self, row, col):
        # Since we assume a simple graph, no node connects to itself. Thus, if row=col, the answer is false.
        if row == col:
            return False

        # If the column is greater than the row, we're reading from the upper right of the adj. mat.
        #  We deleted this area in order to compress the adj. structure. However, it's a mirror image
        #  over the diagonal of the lower left. Thus, swap the row and column to read from the lower left
        #  which we did store.
        # Row access is shifted down one due to the location of the stored region (col variable is used but
        #  row access is shifted down)
        if col > row:
            return self.adjacency_structure[col - 1][row]

        # col < row
        # We now know col is less than row. This means we're in the lower left. This is the area we stored, so
        #  just read from the stored adjacency structure.
        # Row access is shifted down one due to the location of the stored region
        return self.adjacency_structure[row - 1][col]

    # read_adjacency_matrix()
    #
    # Returns INT: Converts the stored boolean to an int (Undoes the compression)
    #
    # Returns 1 if true; 0 if false
    #
    # Accesses the theoretical adjacency matrix of this graph; we only store a much smaller adjacencyStructure
    #  since the graph is assumed to be simple and undirected. See class docs for more.
    #
    # Calls read_adjacency_matrix_bool()
    def read_adjacency_matrix(self, row, col):
        if self.read_adjacency_matrix_bool(row, col):
            return 1
        return 0

    # read_square_adjacency_matrix()
    #
    # Returns int; it's the underlying data type
    #
    # Accesses the theoretical square adjacency matrix of this graph; we only store a much smaller
    # square_adjacency_structure since the graph is assumed to be simple and undirected. See class docs for more.
    #
    # the square_adjacency_matrix is cached and updated by calls to write_adjacency_matrix
    def read_square_adjacency_matrix(self, row, col):
        # if row = col it doesn't matter which branch executes, so ignore it.

        # If the column is greater than the row, we're reading from the upper right of the adj. mat.
        #  We deleted this area in order to compress the adj. structure. However, it's a mirror image
        #  over the diagonal of the lower left. Thus, swap the row and column to read from the lower left
        #  which we did store.
        if col > row:
            return self.square_adjacency_structure[col][row]

        # col < row
        # We now know col is less than row. This means we're in the lower left. This is the area we stored, so
        #  just read from the stored adjacency structure.
        return self.square_adjacency_structure[row][col]

    # write_adjacency_matrix()
    #
    # Accesses the theoretical adjacency matrix of this graph; we only store a much smaller adjacencyStructure
    #  since the graph is assumed to be simple and undirected. See class docs for more.
    #
    # Updates square_adjacency_structure
    #
    # Thus, write operations are slowed by optimized matrix calculations.
    #
    # Before the write operation, a read operation is performed to check if the write operation is making a change.
    #  The square_adjacency_structure is only updated if a change is made, and only the affected row/col are updated.
    def write_adjacency_matrix(self, row, col, val):
        # Since we assume a simple graph, no node connects to itself. Thus, if row=col, the answer is false.
        if row == col:
            raise ValueError('The OptimizedGraph data structure assumes a simple graph; thus writes that could create \
            loops are not allowed. row cannot equal col.')

        # Declare a variable to determine if adjacency strucutre has been modified.
        #  This is used to ensure square_adjacency_structure is only updated if something is changed
        adjacency_structure_modified = False

        # If the column is greater than the row, we're reading from the upper right of the adj. mat.
        #  We deleted this area in order to compress the adj. structure. However, it's a mirror image
        #  over the diagonal of the lower left. Thus, swap the row and column to read from the lower left
        #  which we do store.
        if col > row:
            # SWITCH COLUMN AND ROW
            a = row
            row = col
            col = a

        # NORMAL ROW COLUMN
        # col < row
        # We now know col is less than row. This means we're in the lower left. This is the area we stored, so
        #  just write to the stored adjacency structure.

        # Store whether or not we changed the adjacency_structure
        adjacency_structure_modified = self.adjacency_structure[row - 1][col] != val

        # perform the update
        self.adjacency_structure[row - 1][col] = val

        # Recalculate the row and column in the squared_adjacency_structure if we changed something
        if adjacency_structure_modified:
            for i in range(0, self.size):
                # recalculate cell (i, col)
                total = 0
                for x in range(0, self.size):
                    total += self.read_adjacency_matrix(i, x) * self.read_adjacency_matrix(x, col)
                # swap the row/col if we go over the border
                if col > i:
                    self.square_adjacency_structure[col][i] = total
                else:
                    self.square_adjacency_structure[i][col] = total
            for i in range(0, len(self.adjacency_structure[row-1])+1):
                # recalculate cell (row, i)
                # row, col would get covered once in each loop, so ignore it in this loop and do it in the other
                total = 0
                for x in range(0, self.size):
                    total += self.read_adjacency_matrix(row, x) * self.read_adjacency_matrix(x, i)
                self.square_adjacency_structure[row][i] = total

    # add_edge()
    #
    # Adds an edge to the graph from vertex a to vertex b
    #
    # Overwrites existing edge if it's already there; no duplicates will be created since
    #  it's an adjacency structure.
    #
    # Equivalent to calling write_adjacency_matrix(a, b, True)
    #
    # Updates square_adjacency_structure
    #
    # Thus, write operations are slowed by optimized matrix calculations.
    def add_edge(self, a, b):
        return self.write_adjacency_matrix(a, b, True)

    # remove_edge()
    #
    # Removes an edge from the graph from vertex a to vertex b
    #
    # Doesn't care if there isn't an edge there. It'll still run.
    #
    # Equivalent to calling write_adjacency_matrix(a, b, False)
    #
    # Updates square_adjacency_structure
    #
    # Thus, write operations are slowed by optimized matrix calculations.
    def remove_edge(self, a, b):
        return self.write_adjacency_matrix(a, b, False)

    # check_edge_present()
    #
    # Returns True iff an edge is present from a to b in the graph represented by
    #  this data structure.
    #
    # Equivalent to calling read_adjacency_matrix_bool(a, b)
    def check_edge_present(self, a, b):
        return self.read_adjacency_matrix_bool(a, b)

    # get_full_adjacency_matrix()
    #
    # converts the adjacency structure into a full adjacency matrix and returns it
    #
    # NOT OPTIMIZED
    #
    # returns a 2D array
    def get_full_adjacency_matrix(self):
        matrix = []
        for row_index in range(0, self.size):
            row = []
            for col_index in range(self.size):
                row.append(self.read_adjacency_matrix(row_index, col_index))
            matrix.append(row)
        return matrix

    # get_full_square_adjacency_matrix()
    #
    # converts the square adjacency structure into a full square adjacency matrix and returns it
    #
    # NOT OPTIMIZED
    #
    # returns a 2D array
    def get_full_square_adjacency_matrix(self):
        matrix = []
        for row_index in range(0, self.size):
            row = []
            for col_index in range(self.size):
                row.append(self.read_square_adjacency_matrix(row_index, col_index))
            matrix.append(row)
        return matrix

    # does_follow_rules()
    #
    # NOT COMPLETE: This function works; however, it is not fully optimized. It should not be using a numpy cubed
    #  matrix. More updates are soon to come.
    #
    # Returns true if the graph represented by this data structure follows the rules of this research
    #
    # A graph follows the rules if it contains no c3, c4, or c6 cycles.
    # This function is far less reader-friendly; however it is equivalent to
    # does_follow_rules() and should run more quickly due to linearly decreased
    # number of loops and matrix operations.
    #
    # matrix An adjacency matrix in the form of a 2D array that represents a networkx (or any other) graph
    # see nx.to_numpy_matrix() to convert networkx graphs to adjacency matrices.
    #
    # see check() in Huntington's dissertation
    # see does_follow_rules() in graph.py for a more-readable but less efficient version
    def does_follow_rules(self):
        # todo don't use numpy here
        cubed = numpy.dot(numpy.matrix(self.get_full_square_adjacency_matrix()), numpy.matrix(self.get_full_adjacency_matrix()))

        # todo don't use numpy here
        # Test for tries and return false if they exist
        cubed_diagonal_sum = numpy.sum(numpy.diagonal(cubed))
        if cubed_diagonal_sum > 0:
            return False

        # Test for quads and return false if they exist
        for i in range(1, self.size - 1):
            for j in (i + 1, self.size - 1):
                if self.read_square_adjacency_matrix(i, j) > 1:
                    return False
                if cubed[i, j] > 1 and self.read_adjacency_matrix(i, j) == 0:
                    return False

        return True


# test()
#
# Uses assert keyword to test the functionality of OptimizedGraph
#
# numpy is required
def test():
    print 'Testing up to a 20x20 for correctness...'
    for size in range(1, 21):
        g = OptimizedGraph(size)

        adjmat_manual = numpy.zeros((size, size), dtype=numpy.int)

        for i in range(0, size):
            for j in range(0, size):
                if i != j:
                    g.add_edge(i, j)
                    adjmat_manual[i][j] = 1
                    adjmat_manual[j][i] = 1

                    adjmat2_manual = numpy.dot(adjmat_manual, adjmat_manual)

                    adjmat_from_class = numpy.matrix(g.get_full_adjacency_matrix())
                    adjmat2_from_class = numpy.matrix(g.get_full_square_adjacency_matrix())

                    assert numpy.array_equal(adjmat2_manual, adjmat2_from_class)

        print 'Passed <%s tests for matrix of size %s' % (size*size, size)
    print 'Done testing correctness.'

    print 'Testing up to a 50x50 for speed...'
    for size in range(2, 51):
        g = OptimizedGraph(size)

        edge_count = 0
        start = time()

        for i in range(0, size):
            for j in range(0, size):
                if i != j:
                    g.add_edge(i, j)
                    edge_count += 1
        end = time()

        duration = end-start
        duration_per_edge = duration/edge_count

        print 'Added <%s edges (size=%s) in %s seconds (%s seconds per edge)' % (edge_count, size, duration, duration_per_edge)
    print 'Done testing speed.'

    print 'Testing up to a 41x41 for speed checking cycles...'
    for size in range(2, 42):
        g = OptimizedGraph(size)

        graph_count = 0
        start = time()

        for i in range(0, size):
            for j in range(0, size):
                if i != j:
                    g.add_edge(i, j)
                    g.does_follow_rules()
                    graph_count += 1
        end = time()

        duration = end-start
        duration_per_graph = duration/graph_count

        print 'Checked <%s graphs (size=%s) in %s seconds (%s seconds per graph)' % (graph_count, size, duration, duration_per_graph)
    print 'Done testing speed.'


# If somebody ever runs this file, invoke test() to test OptimizedGraph()
if __name__ == '__main__':
    test()
