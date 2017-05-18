from Tkinter import *
import networkx as nx

WIDTH = 1024
HEIGHT = 480
ROW_HEIGHT = 64
CENTER = WIDTH / 2
NODE_WIDTH = 32
SAME_LAYER_VERTICAL_OFFSET = 20
SAME_LAYER_HORIZONTAL_OFFSET = 6

# Quick and dirty Tkinter function to visualize tree-like graphs from networkx
# Layers are determined using the shortest path to the root node
def draw_network(G, root=1):
    master = Tk()

    w = Canvas(master, width=WIDTH, height=480)
    w.pack()
    layer_nodes = {}
    node_layers = {}

    # Calculate node locations
    nodeCoordinates = {}

    for node in G.nodes():
        # The layer of each node is its shortest distance from the root node
        layer = len(nx.shortest_path(G, node, root))

        if not layer in layer_nodes.keys():
            layer_nodes[layer] = []
        layer_nodes[layer].append(node)
        node_layers[node] = layer

    for layer in layer_nodes.keys():
        nodes = layer_nodes[layer]
        index = 0
        for node in sorted(nodes):
            x1 = CENTER - NODE_WIDTH * (len(nodes) / 2 - index)
            y1 = ROW_HEIGHT * layer

            nodeCoordinates[node] = (x1, y1)

            index += 1

    # Draw edges
    for edge in G.edges():
        if node_layers[edge[0]] == node_layers[edge[1]]:
            # Draw an arc when nodes are on the same layer
            a = nodeCoordinates[edge[0]]
            b = nodeCoordinates[edge[1]]
            w.create_line(a[0], a[1], a[0]+SAME_LAYER_HORIZONTAL_OFFSET, a[1]+SAME_LAYER_VERTICAL_OFFSET)
            w.create_line(b[0], b[1], b[0]-SAME_LAYER_HORIZONTAL_OFFSET, b[1]+SAME_LAYER_VERTICAL_OFFSET)
            w.create_line(a[0]+SAME_LAYER_HORIZONTAL_OFFSET, a[1]+SAME_LAYER_VERTICAL_OFFSET, b[0]-SAME_LAYER_HORIZONTAL_OFFSET, b[1]+SAME_LAYER_VERTICAL_OFFSET)
        else:
            # Draw a straight line when nodes are on different layers
            a = nodeCoordinates[edge[0]]
            b = nodeCoordinates[edge[1]]
            w.create_line(a[0], a[1], b[0], b[1])

    # Draw nodes
    for node in G.nodes():
        coordinates = nodeCoordinates[node]
        w.create_oval(coordinates[0] - 12, coordinates[1] - 12, coordinates[0] + 12, coordinates[1] + 12, fill="white")
        w.create_text(coordinates[0], coordinates[1], text=str(node))

    mainloop()
