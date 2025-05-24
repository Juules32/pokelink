from business import Business
from util import get_date

# Running this script sets up the database tables
# And generates and sets 10 puzzles
if __name__ == "__main__":
    bn = Business()
    bn.db.create_puzzle_table()
    bn.db.create_user_solution_table()
