from typing import Union
from pydantic import BaseModel

# A grouping of pokémon data used in AdjacencyData
class PokemonNode(BaseModel):
    name: str                               # The name of the pokémon
    id: int                                 # The id of the pokémon
    types: list[str]                        # The types of the pokémon
    region: str                             # The region of the pokémon

# Stored in the database as daily puzzles
class Puzzle(BaseModel):
    date: str
    source: str                             # The name of the starting pokémon
    target: str                             # The name of the finishing pokémon
    shortest_path: list[str]                # The names of the pokémon of the shortest path
    shortest_path_length: int               # The length of the shortest path

    def __str__(self):
        return f"""
Source = {self.source}
Target = {self.target}
Shortest Path = {self.shortest_path}
Shortest Path Length = {self.shortest_path_length}
        """

# The the nodes and edges of the networkx graph
class GraphData(BaseModel):
    nodes: dict[str, PokemonNode]
    edges: dict[str, list[str]]

# Represents one puzzle in a list of puzzles
class PuzzlesItem(BaseModel):
    date: str
    source: str
    target: str
    completed: bool

# Sent along with user request to set a solution
class SolutionRequest(BaseModel):
    userid: str
    solution: list[str]

# A puzzle with a user's solution attached
class PuzzleSolution(BaseModel):
    puzzle: Puzzle
    solution: Union[list[str], None]
