import pickle
from typing import Union
from networkx import Graph
from database import Database
from model import GraphData, Puzzle
import random
import networkx as nx
from networkx import Graph
from pokemon_data_generation import region_number
from date import get_date_str
from graph_data_generation import get_graph_data, load_graph
from dotenv import load_dotenv
import os
import httpx

class Business:
    def __init__(self):
        load_dotenv()
        self.environment: Union[str, None] = os.getenv("ENVIRONMENT")
        if self.environment == "DEVELOPMENT":
            self.graph = load_graph()
            print("Loaded graph from local file")
    
    def download_graph(self) -> Graph:
        response = httpx.get(f"{os.getenv('BLOB_HOST')}/graph_data.pkl")
        if response.status_code == 200:
            print("Downloading pickled file")
            return pickle.loads(response.content)
        else:
            print("Failed to download pickled file")
            raise None
    
    # Returns loaded file for local development
    # In production (vercel), instead download the graph from the blob storage
    def get_graph(self) -> Graph:
        if self.environment == "DEVELOPMENT":
            return self.graph
        else:
            return self.download_graph()
    
    def get_graph_data(self, graph: Graph) -> GraphData:
        return get_graph_data(graph)
    
    def get_puzzle(self, date: Union[str, None] = None) -> Puzzle:
        return Database().get_puzzle(date)
    
    def generate_puzzle(self, graph: Graph, strict: bool) -> Puzzle:
        pokemon_names = list(graph.nodes.keys())
        source=random.choice(pokemon_names)
        target=random.choice(pokemon_names)

        print(f"Generating data for puzzle between {source} and {target}...")

        if not nx.has_path(graph, source, target):
            raise Exception(f"Found Puzzle with no connection: {source} to {target}")
        if strict and not self.is_valid(graph, source, target):
            return self.generate_puzzle(graph, strict=True)
        
        return Puzzle(
            source=source,
            target=target,
            shortest_path=nx.shortest_path(graph, source, target),
            shortest_path_length=nx.shortest_path_length(graph, source, target)
        )

    def generate_10_puzzles(self, graph: Graph) -> list[Puzzle]:
        return [self.generate_puzzle(graph, strict=True) for _ in range(10)]

    def get_generational_difference(self, graph: Graph, source: str, target: str) -> int:
        source_region_number = region_number[graph.nodes[source]["region"]]
        target_region_number = region_number[graph.nodes[target]["region"]]
        return abs(source_region_number - target_region_number)

    def is_valid(self, graph: Graph, source: str, target: str) -> bool:
        MIN_SHORTEST_PATH_LENGTH = 4
        MIN_GENERATIONAL_DIFFERENCE = 1

        generational_difference = self.get_generational_difference(graph, source, target)
        shortest_path_length = nx.shortest_path_length(graph, source, target)
        return shortest_path_length >= MIN_SHORTEST_PATH_LENGTH and generational_difference >= MIN_GENERATIONAL_DIFFERENCE

    def get_hint(self, graph: Graph, source: str, target: str) -> str:
        shortest_path = nx.shortest_path(graph, source, target)
        return shortest_path[1] if len(shortest_path) >= 2 else shortest_path[0]

if __name__ == "__main__":
    db = Database()
    bn = Business()
    ten_puzzles = bn.generate_10_puzzles(bn.get_graph())
    for i, puzzle in enumerate(ten_puzzles):
        db.set_puzzle(get_date_str(i), puzzle)
    print(db.get_puzzle(get_date_str()))
