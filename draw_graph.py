
import matplotlib.pyplot as plt
import networkx as nx

from graph_data_generation import generate_graph, generate_pos

if __name__ == "__main__":
    G = generate_graph()
    pos = generate_pos(G)
    nx.draw(G, with_labels=True, pos=pos)
    plt.show()
