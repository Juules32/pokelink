from pydantic import BaseModel

# A grouping of pokémon data used in AdjacencyData
class PokemonNode(BaseModel):
    name: str                               # The name of the pokémon
    id: int                                 # The id of the pokémon
    types: list[str]                        # The types of the pokémon
    region: str                             # The region of the pokémon

# Returned as response to valid client guess
class AdjacencyData(BaseModel):
    guess: PokemonNode
    adjacent_pokemon: list[PokemonNode]

# Stored in the database as daily puzzles
class Puzzle(BaseModel):
    source: PokemonNode                     # The name of the starting pokémon
    target: PokemonNode                     # The name of the finishing pokémon
    shortest_path: list[PokemonNode]        # The names of the pokémon of the shortest path
    shortest_path_length: int               # The length of the shortest path
