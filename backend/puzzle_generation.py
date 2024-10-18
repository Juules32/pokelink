import random
import networkx as nx
from networkx import Graph
from graph_data_generation import generate_graph
from model import Puzzle
from pokemon_data_generation import region_number

def generate_puzzle(G: Graph, pokemon_names: list[str], strict: bool) -> Puzzle:
    source=random.choice(pokemon_names)
    target=random.choice(pokemon_names)
    if not nx.has_path(G, source, target):
        raise Exception(f"Found Puzzle with no connection: {source} to {target}")
    if strict and not is_valid(G, source, target):
        return generate_puzzle(G, pokemon_names, strict=True)
    return Puzzle(
        source=source,
        target=target,
        shortest_path=get_shortest_path(G, source, target),
        shortest_path_length=get_shortest_path_length(G, source, target)
    )

def generate_10_puzzles(G: Graph, pokemon_names: list[str]) -> list[Puzzle]:
    return [generate_puzzle(G, pokemon_names, strict=True) for _ in range(10)]

def get_shortest_path(G: Graph, source: str, target: str) -> list[str]:
    return nx.shortest_path(G, source, target)

def get_shortest_path_length(G: Graph, source: str, target: str) -> int:
    return nx.shortest_path_length(G, source, target)

def get_generational_difference(G: Graph, source: str, target: str) -> int:
    source_region_number = region_number[G.nodes[source]["region"]]
    target_region_number = region_number[G.nodes[target]["region"]]
    return abs(source_region_number - target_region_number)

MIN_GENERATIONAL_DIFFERENCE = 2
MIN_PATH_LENGTH = 8

def is_valid(G: Graph, source: str, target: str) -> bool:
    generational_difference = get_generational_difference(G, source, target)
    shortest_path_length = get_shortest_path_length(G, source, target)
    return generational_difference >= MIN_GENERATIONAL_DIFFERENCE and shortest_path_length >= MIN_PATH_LENGTH

if __name__ == "__main__":
    G = generate_graph()
    pokemon_names = list(G.nodes.keys())
    puzzle = generate_puzzle(G, pokemon_names, strict=False)
    print(puzzle)
