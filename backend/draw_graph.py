
import matplotlib.pyplot as plt
import networkx as nx
from typing import Counter
from business import Business
from graph_data_generation import generate_pos

def visualize_path_length_distribution(bn: Business):
    path_lengths = []
    for _ in range(100):
        puzzle = bn.generate_puzzle(strict=True)
        path_lengths.append(bn.get_shortest_path_length(puzzle.source, puzzle.target))

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

def visualize_graph(bn: Business):
    pos = generate_pos(bn.graph)
    nx.draw(bn.graph, with_labels=True, pos=pos)
    plt.show()

# Running this script generates and visualizes the graph
if __name__ == "__main__":
    bn = Business()
    visualize_path_length_distribution(bn)
    visualize_graph(bn)
