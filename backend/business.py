from typing import Union
from networkx import Graph
from db import Database
from model import AdjacencyData, PokemonData, Puzzle

class Business:
    def __init__(self):
        self.db = Database()
        self.graph = self.db.get_graph()
    
    def get_graph(self) -> Graph:
        return self.graph
    
    def get_puzzle(self, date: Union[str, None] = None) -> Puzzle:
        return self.db.get_puzzle(date)
    
    def get_adjacency_data(self, guess: str) -> AdjacencyData:
        guess_graph_data = self.graph.nodes[guess]
        guess_data = PokemonData(
            name=guess,
            id=guess_graph_data["id"],
            types=guess_graph_data["types"],
            region=guess_graph_data["region"]
        )

        neighbor_data: list[PokemonData] = []
        for neighbor in self.graph.neighbors(guess):
            neighbor_graph_data = self.graph.nodes[neighbor]
            neighbor_data.append(PokemonData(
                name=neighbor,
                id=neighbor_graph_data["id"],
                types=neighbor_graph_data["types"],
                region=neighbor_graph_data["region"]
            ))

        return AdjacencyData(
            guess=guess_data,
            adjacent_pokemon=neighbor_data
        )
