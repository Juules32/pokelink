from business import Business
from date import get_date_str

# Running this script sets up the database tables
# And generates and sets 10 puzzles
if __name__ == "__main__":
    bn = Business()
    bn.db.create_pokelink_puzzle_table()
    bn.db.create_pokelink_user_solution_table()
    puzzles = bn.generate_pokelink_puzzles(bn.get_graph(), 5)
    for puzzle in puzzles:
        bn.db.set_pokelink_puzzle(puzzle)
    print("Last generated puzzle:", bn.db.get_pokelink_puzzle(get_date_str()))
