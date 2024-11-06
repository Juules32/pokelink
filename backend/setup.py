from business import Business
from date import get_date_str

# Running this script sets up the database tables
# And generates and sets 10 puzzles
if __name__ == "__main__":
    bn = Business()
    bn.db.create_puzzle_table()
    bn.db.create_user_solution_table()
    puzzles = bn.generate_n_puzzles(bn.get_graph(), 55)
    for puzzle in puzzles:
        bn.db.set_puzzle(puzzle)
    print("Last generated puzzle:", bn.db.get_puzzle(get_date_str()))
