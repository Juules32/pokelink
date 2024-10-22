
import matplotlib.pyplot as plt
import networkx as nx
from typing import Counter
from networkx import Graph
from business import Business
from graph_data_generation import generate_pos

def visualize_path_length_distribution(graph: Graph, bn: Business):
    path_lengths = []
    for _ in range(100):
        puzzle = bn.generate_puzzle(graph, strict=True)
        path_lengths.append(nx.shortest_path_length(graph, puzzle.source, puzzle.target))

    # Count occurrences of each path length
    length_counts = Counter(path_lengths)
    
    # Sort the counts by path length
    lengths = sorted(length_counts.keys())
    occurrences = [length_counts[length] for length in lengths]

    # Plot the frequencies using a line graph
    plt.plot(lengths, occurrences, marker='o', linestyle='-', color='b')
    plt.title("Frequency of Shortest Path Lengths")
    plt.xlabel("Path Length")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

def visualize_graph(graph: Graph):
    pos = generate_pos(graph)
    nx.draw(graph, with_labels=True, pos=pos)
    plt.show()

# Running this script generates and visualizes the graph
if __name__ == "__main__":
    bn = Business()
    graph = bn.get_graph()
    visualize_path_length_distribution(graph, bn)
    visualize_graph(graph)
