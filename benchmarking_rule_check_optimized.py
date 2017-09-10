import networkx as nx
from time import time
import graph

if __name__ == "__main__":
    G = graph.treex(3, 8)

    G.add_edge(2, 7)

    print "Testing network of size", len(nx.to_numpy_matrix(G))

    start_optimized = time()
    follows_rules_optimized = graph.does_follow_rules_optimized(nx.to_numpy_matrix(G))
    end_optimized = time()

    start_normal = time()
    follows_rules = graph.does_follow_rules(nx.to_numpy_matrix(G))
    end_normal = time()

    optimized_duration = end_optimized - start_optimized
    normal_duration = end_normal - start_normal

    if follows_rules != follows_rules_optimized:
        print "The functions disagree. This is a huge problem."

    print "Follows rules: ", follows_rules
    print "Time optimized: ", optimized_duration, "seconds"
    print "Time slow: ", normal_duration, "seconds"

    print "The optimized algorithm ran in ", optimized_duration/normal_duration*100, "% of the time as the normal algorithm."
