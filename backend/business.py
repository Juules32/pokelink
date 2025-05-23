import pickle, random, httpx
from typing import Union
from networkx import Graph
from exceptions import InvalidSolutionException, NotFoundException
from date import get_date_str
from env import BLOB_HOST
from database import Database
from model import GraphData, Puzzle, PuzzleSolution, PuzzlesItem
import networkx as nx
from networkx import Graph
from pokemon_data_generation import region_number
from graph_data_generation import get_graph_data, load_graph, types_in_common
from urllib.parse import urljoin

class Business:
    def __init__(self):
        self.graph = self.get_blob_graph()
        print("Loaded graph data")
        self.db = Database()

    def get_blob_graph(self) -> Graph:
        if not BLOB_HOST:
            raise Exception

        # Requests the pickled file directly from the blob host
        response = httpx.get(urljoin(BLOB_HOST, "graph_data.pkl"))
        if response.status_code == 200:
            print("Downloading pickled file")
            return pickle.loads(response.content)
        else:
            print("Failed to download pickled file")
            raise NotFoundException("Graph data not found")
    
    def get_graph(self) -> Graph:
        return self.graph
    
    def get_graph_data(self, graph: Graph) -> GraphData:
        return get_graph_data(graph)
    
    def get_puzzle_solution(self, date: str, userid: str) -> PuzzleSolution:
        puzzle = self.db.get_puzzle(date)
        if not puzzle:
            raise NotFoundException("Puzzle not found 😢")
        
        solution = self.db.get_user_solution(userid, date)

        return PuzzleSolution(
            puzzle=puzzle,
            solution=solution
        )
    
    def generate_puzzle(self, graph: Graph, date: str, strict: bool) -> Puzzle:
        pokemon_names = list(graph.nodes.keys())
        source=random.choice(pokemon_names)
        target=random.choice(pokemon_names)

        print(f"Generating data for puzzle between {source} and {target}...")

        if not nx.has_path(graph, source, target):
            raise Exception(f"Found Puzzle with no connection: {source} to {target}")
        if strict and not self.is_valid(graph, source, target):
            print("Puzzle wan't valid! Retrying...")
            return self.generate_puzzle(graph, date, strict=True)
        
        shortest_path = nx.shortest_path(graph, source, target)
        shortest_path_length = nx.shortest_path_length(graph, source, target)

        assert isinstance(shortest_path, list), "Expected shortest_path to return a list"

        return Puzzle(
            date=date,
            source=source,
            target=target,
            shortest_path=shortest_path,
            shortest_path_length=shortest_path_length
        )

    def generate_n_puzzles(self, graph: Graph, n: int) -> list[Puzzle]:
        return [self.generate_puzzle(graph, get_date_str(-i), strict=True) for i in range(n)]

    def get_generational_difference(self, graph: Graph, source: str, target: str) -> int:
        source_region_number = region_number[graph.nodes[source]["region"]]
        target_region_number = region_number[graph.nodes[target]["region"]]
        return abs(source_region_number - target_region_number)

    def is_valid(self, graph: Graph, source: str, target: str) -> bool:
        MIN_SHORTEST_PATH_LENGTH = 4
        MIN_GENERATIONAL_DIFFERENCE = 1

        generational_difference = self.get_generational_difference(graph, source, target)
        shortest_path_length = nx.shortest_path_length(graph, source, target)
        return (
            shortest_path_length >= MIN_SHORTEST_PATH_LENGTH and 
            generational_difference >= MIN_GENERATIONAL_DIFFERENCE and
            not types_in_common(set(graph.nodes[source]["types"]), set(graph.nodes[target]["types"]))
        )
    
    def get_hint(self, graph: Graph, source: str, target: str) -> str:
        shortest_path = nx.shortest_path(graph, source, target)
        return shortest_path[1] if len(shortest_path) >= 2 else shortest_path[0]

    def get_puzzles(self, userid: str, page: int) -> list[PuzzlesItem]:
        puzzle_dates = self.db.get_puzzle_dates(page)
        if not puzzle_dates:
            raise NotFoundException("No puzzles found 💀")

        completed_puzzles = self.db.get_completed_puzzles(userid)
        return [
            PuzzlesItem(date=date, source=source, target=target, completed=date in completed_puzzles)
            for date, source, target in puzzle_dates
        ]

    def validate_solution(self, solution: list[str]) -> bool:
        graph = self.get_graph()
        for i in range(len(solution) - 1):
            if not graph.has_edge(solution[i], solution[i + 1]):
                print("Invalid solution detected")
                return False
        return True

    def get_num_puzzles(self) -> int:
        return self.db.get_num_puzzles()

    def set_user_solution(self, userid: str, date: str, solution: list[str]) -> None:
        if not self.validate_solution(solution):
            raise InvalidSolutionException()

        self.db.set_user_solution(userid, date, solution)
