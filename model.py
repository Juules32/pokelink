from pydantic import BaseModel

# Stored in the database as daily puzzles
class Puzzle(BaseModel):
    source: str                             # The name of the starting pokémon
    target: str                             # The name of the finishing pokémon
    shortest_path: list[str]                # The names of the pokémon of the shortest path
    shortest_path_length: int               # The length of the shortest path

# A grouping of pokémon data used in AdjacencyData
class PokemonData(BaseModel):
    name: str                               # The name of the pokémon
    types: list[str]                        # The types of the pokémon
    region: str                             # The region of the pokémon

# Returned as response to valid client guess
class AdjacencyData(BaseModel):
    guess: PokemonData
    adjacent_pokemon: list[PokemonData]
