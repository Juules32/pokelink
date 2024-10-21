from typing import Union
from networkx import Graph
from database import Database
from model import PokemonNode, Puzzle
import random
import networkx as nx
from networkx import Graph
from pokemon_data_generation import region_number
from date import get_date_str
from graph_data_generation import get_graph_data

class Business:
    def __init__(self):
        self.db = Database()
        self.graph = self.db.get_graph()
        self.pokemon_names: list[str] = list(self.graph.nodes.keys())
        self.graph_data = get_graph_data(self.graph)
    
    def get_graph(self) -> Graph:
        return self.graph
    
    def get_puzzle(self, date: Union[str, None] = None) -> Puzzle:
        return self.db.get_puzzle(date)
    
    def get_node_data(self, name: str) -> PokemonNode:
        node_data = self.graph.nodes[name]
        return PokemonNode(
            name=name,
            id=node_data["id"],
            types=node_data["types"],
            region=node_data["region"]
        )

    def generate_puzzle(self, strict: bool) -> Puzzle:
        source=random.choice(self.pokemon_names)
        target=random.choice(self.pokemon_names)

        print(f"Generating data for puzzle between {source} and {target}...")

        if not nx.has_path(self.graph, source, target):
            raise Exception(f"Found Puzzle with no connection: {source} to {target}")
        if strict and not self.is_valid(source, target):
            return self.generate_puzzle(strict=True)
        
        return Puzzle(
            source=source,
            target=target,
            shortest_path=self.get_shortest_path(source, target),
            shortest_path_length=self.get_shortest_path_length(source, target)
        )

    def generate_10_puzzles(self) -> list[Puzzle]:
        return [self.generate_puzzle(strict=True) for _ in range(10)]

    def get_shortest_path(self, source: str, target: str) -> list[str]:
        return nx.shortest_path(self.graph, source, target)

    def get_shortest_path_length(self, source: str, target: str) -> int:
        return nx.shortest_path_length(self.graph, source, target)

    def get_generational_difference(self, source: str, target: str) -> int:
        source_region_number = region_number[self.graph.nodes[source]["region"]]
        target_region_number = region_number[self.graph.nodes[target]["region"]]
        return abs(source_region_number - target_region_number)

    def is_valid(self, source: str, target: str) -> bool:
        MIN_SHORTEST_PATH_LENGTH = 4
        MIN_GENERATIONAL_DIFFERENCE = 1

        generational_difference = self.get_generational_difference(source, target)
        shortest_path_length = self.get_shortest_path_length(source, target)
        return shortest_path_length >= MIN_SHORTEST_PATH_LENGTH and generational_difference >= MIN_GENERATIONAL_DIFFERENCE

    def get_hint(self, source: str, target: str) -> PokemonNode:
        shortest_path = self.get_shortest_path(source, target)
        return self.get_node_data(shortest_path[1] if len(shortest_path) >= 2 else shortest_path[0])

if __name__ == "__main__":
    bn = Business()
    ten_puzzles = bn.generate_10_puzzles()
    for i, puzzle in enumerate(ten_puzzles):
        bn.db.set_puzzle(get_date_str(i), puzzle)
    print(bn.db.get_puzzle(get_date_str()))
