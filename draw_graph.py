
import matplotlib.pyplot as plt
import networkx as nx
from typing import Counter

from graph_data_generation import generate_graph, generate_pos
from puzzle_generation import generate_puzzle, get_shortest_path_length

def visualize_path_length_distribution():
    G = generate_graph()

    # Collect shortest path lengths over 100 iterations
    path_lengths = [get_shortest_path_length(G, generate_puzzle()) for _ in range(100)]

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

def visualize_graph():
    G = generate_graph()
    pos = generate_pos(G)
    nx.draw(G, with_labels=True, pos=pos)
    plt.show()

# Running this script generates and visualizes the graph
if __name__ == "__main__":
    visualize_path_length_distribution()
    visualize_graph()
