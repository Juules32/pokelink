import copy
import pickle, random, httpx
from typing import Union
from networkx import Graph
from file_io import pickle_load
from exceptions import InvalidSolutionException, NotFoundException
from date import get_date_str
from env import BLOB_HOST, ENVIRONMENT
from database import Database
from model import GraphData, PokelinkPuzzle, PokelinkPuzzleSolution, PokelinkPuzzlesItem
import networkx as nx
from networkx import Graph
from pokemon_data_generation import region_number
from graph_data_generation import get_graph_data, types_in_common

class Business:
    def __init__(self):
        self.environment: Union[str, None] = ENVIRONMENT
        if self.environment == "DEVELOPMENT":
            self.graph = pickle_load("graph")
            self.criteria_data: dict = pickle_load("criteria_data")
            print("Loaded graph and criteria data from local file")
        self.db = Database()
    
    def get_blob_file(self, name: str) -> Graph:
        # Requests the pickled file directly from the blob host
        response = httpx.get(f"{BLOB_HOST}/{name}")
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
            return self.get_blob_file("graph.pkl")
    
    def get_criteria_data(self) -> dict:
        if self.environment == "DEVELOPMENT":
            return self.criteria_data
        else:
            return self.get_blob_file("criteria_data.pkl")
    
    def get_graph_data(self, graph: Graph) -> GraphData:
        return get_graph_data(graph)
    
    def get_pokelink_puzzle_solution(self, date: str, userid: str) -> PokelinkPuzzleSolution:
        puzzle = self.db.get_pokelink_puzzle(date)
        if not puzzle:
            raise NotFoundException("Puzzle not found 😢")
        
        solution = self.db.get_pokelink_user_solution(userid, date)

        return PokelinkPuzzleSolution(
            puzzle=puzzle,
            solution=solution
        )
    
    def generate_pokelink_puzzle(self, graph: Graph, date: str, strict: bool) -> PokelinkPuzzle:
        pokemon_names = list(graph.nodes.keys())
        source=random.choice(pokemon_names)
        target=random.choice(pokemon_names)

        print(f"Generating data for puzzle between {source} and {target}...")

        if not nx.has_path(graph, source, target):
            print(f"Found Puzzle with no connection: {source} to {target}. Retrying...")
            return self.generate_pokelink_puzzle(graph, date, strict=strict)
        if strict and not self.is_pokelink_puzzle_valid(graph, source, target):
            print("Puzzle wan't valid! Retrying...")
            return self.generate_pokelink_puzzle(graph, date, strict=strict)
        
        return PokelinkPuzzle(
            date=date,
            source=source,
            target=target,
            shortest_path=nx.shortest_path(graph, source, target),
            shortest_path_length=nx.shortest_path_length(graph, source, target)
        )

    def generate_pokelink_puzzles(self, graph: Graph, n: int) -> list[PokelinkPuzzle]:
        return [self.generate_pokelink_puzzle(graph, get_date_str(-i), strict=True) for i in range(n)]

    def get_generational_difference(self, graph: Graph, source: str, target: str) -> int:
        source_region_number = region_number[graph.nodes[source]["region"]]
        target_region_number = region_number[graph.nodes[target]["region"]]
        return abs(source_region_number - target_region_number)

    def is_pokelink_puzzle_valid(self, graph: Graph, source: str, target: str) -> bool:
        MIN_SHORTEST_PATH_LENGTH = 4
        MIN_GENERATIONAL_DIFFERENCE = 1

        generational_difference = self.get_generational_difference(graph, source, target)
        shortest_path_length = nx.shortest_path_length(graph, source, target)
        return (
            shortest_path_length >= MIN_SHORTEST_PATH_LENGTH and 
            generational_difference >= MIN_GENERATIONAL_DIFFERENCE and
            not types_in_common(set(graph.nodes[source]["types"]), set(graph.nodes[target]["types"]))
        )
    
    def get_pokelink_hint(self, graph: Graph, source: str, target: str) -> str:
        shortest_path = nx.shortest_path(graph, source, target)
        return shortest_path[1] if len(shortest_path) >= 2 else shortest_path[0]

    def get_pokelink_puzzles(self, userid: str, page: int) -> list[PokelinkPuzzlesItem]:
        puzzle_dates = self.db.get_pokelink_puzzle_dates(page)
        if not puzzle_dates:
            raise NotFoundException("No puzzles found 💀")

        completed_puzzles = self.db.get_pokelink_completed_puzzles(userid)
        return [
            PokelinkPuzzlesItem(date=date, source=source, target=target, completed=date in completed_puzzles)
            for date, source, target in puzzle_dates
        ]

    def validate_pokelink_solution(self, solution: list[str]) -> bool:
        graph = self.get_graph()
        for i in range(len(solution) - 1):
            if not graph.has_edge(solution[i], solution[i + 1]):
                print("Invalid solution detected")
                return False
        return True

    def get_pokelink_num_puzzles(self) -> int:
        return self.db.get_pokelink_num_puzzles()

    def set_pokelink_user_solution(self, userid: str, date: str, solution: list[str]) -> None:
        if not self.validate_pokelink_solution(solution):
            raise InvalidSolutionException()

        self.db.set_pokelink_user_solution(userid, date, solution)

    def generate_pokedoku2_puzzle(self, criteria_data: dict, date: str) -> dict:
        for key, value in criteria_data.items():
            criteria_data[key] = set(value)

        criteria = list(criteria_data.keys())

        def generate_criteria(unused_criteria: list):
            selected_criteria = []
            for _ in range(3):
                selected_criteria.append(unused_criteria.pop(random.randrange(len(unused_criteria))))
            return selected_criteria

        def get_results(criteria: list):
            return [
                criteria_data[criterion]
                for criterion in criteria
            ]

        retries = 0
    
        while True:
            unused_criteria = copy.deepcopy(criteria)
            
            column_criteria = generate_criteria(unused_criteria)
            column_results = get_results(column_criteria)
            
            row_criteria = generate_criteria(unused_criteria)
            row_results = get_results(row_criteria)
            
            valid_pokemon = [
                # Finds the intersection between the two sets
                list(column_result & row_result)
                for row_result in row_results
                for column_result in column_results
            ]
            
            # Returns generated data if no cells contains no valid pokemon
            if not any(len(sublist) == 0 for sublist in valid_pokemon):
                return {
                    "date": date,
                    "column_criteria": column_criteria,
                    "row_criteria": row_criteria,
                    "valid_pokemon": valid_pokemon
                }
            else:
                retries += 1
                print(f"Combination of criteria contained empty result. Retries: {retries}")

    def generate_pokedoku2_puzzles(self, criteria_data: dict, n: int) -> list[dict]:
        return [self.generate_pokedoku2_puzzle(criteria_data, get_date_str(-i)) for i in range(n)]

# Running this script sets up the database tables
# And generates and sets 10 puzzles
if __name__ == "__main__":
    bn = Business()
    bn.db.create_pokelink_puzzle_table()
    bn.db.create_pokelink_user_solution_table()
    bn.db.create_pokedoku2_puzzle_table()
    pokelink_puzzles = bn.generate_pokelink_puzzles(bn.get_graph(), 5)
    for puzzle in pokelink_puzzles:
        bn.db.set_pokelink_puzzle(puzzle)
    print("Last generated pokelink puzzle:", bn.db.get_pokelink_puzzle(get_date_str()))

    pokedoku2_puzzles = bn.generate_pokedoku2_puzzles(bn.get_criteria_data(), 5)
    for puzzle in pokedoku2_puzzles:
        bn.db.set_pokedoku2_puzzle(puzzle)
    print("Last generated pokedoku2 puzzle:", bn.db.get_pokedoku2_puzzle(get_date_str()))
