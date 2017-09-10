import networkx as nx
from time import time
import graph

if __name__ == "__main__":
    WIDTH = 3
    DEPTH = 5

    G = graph.treex(WIDTH, DEPTH)
    G2 = graph.treex(WIDTH, DEPTH)

    G.add_edge(2, 7)

    print "Testing network of size", len(nx.to_numpy_matrix(G))

    start_optimized = time()
    follows_rules_optimized = graph.does_follow_rules_optimized(nx.to_numpy_matrix(G))
    end_optimized = time()

    start_normal = time()
    follows_rules = graph.does_follow_rules(nx.to_numpy_matrix(G))
    end_normal = time()

    start_iso_false = time()
    iso_false = nx.is_isomorphic(G, G2)
    end_iso_false = time()

    G2.add_edge(2, 7)

    start_iso_true = time()
    iso_true = nx.is_isomorphic(G, G2)
    end_iso_true = time()

    optimized_duration = end_optimized - start_optimized
    normal_duration = end_normal - start_normal
    iso_true_duration = end_iso_true - start_iso_true
    iso_false_duration = end_iso_false - start_iso_false

    if follows_rules != follows_rules_optimized:
        print "The functions disagree. This is a huge problem."
    if not iso_true:
        print "Networks that were supposed to me isomorphic were not. This is a problem."
    if iso_false:
        print "Networks that were not supposed to me isomorphic were. This is a problem."

    print "Follows rules: ", follows_rules
    print "Time optimized: ", optimized_duration, "seconds"
    print "Time slow: ", normal_duration, "seconds"
    print "Time isomorphic (true): ", iso_true_duration, "seconds"
    print "Time isomorphic (false): ", iso_false_duration, "seconds"

    print "The optimized algorithm ran in ", optimized_duration/normal_duration*100, "% of the time as the normal algorithm."
    print "The isomorphism algorithm (on isomorphic graphs) ran in ", iso_true_duration/optimized_duration*100, "% of the time as the optimized check algorithm."
    print "The isomorphism algorithm (on non-isomorphic graphs) ran in ", iso_false_duration/optimized_duration*100, "% of the time as the optimized check algorithm."
