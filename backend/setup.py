from business import Business
from database import Database
from date import get_date_str

# Running this script sets up the database tables
# And generates and sets 10 puzzles
if __name__ == "__main__":
    db = Database()
    db.create_puzzle_table()
    bn = Business()
    ten_puzzles = bn.generate_10_puzzles(bn.get_graph())
    for i, puzzle in enumerate(ten_puzzles):
        db.set_puzzle(get_date_str(i), puzzle)
    print(db.get_puzzle(get_date_str()))
