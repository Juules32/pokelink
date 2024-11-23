from business import Business
from date import get_date_str

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
