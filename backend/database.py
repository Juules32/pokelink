from datetime import date, datetime
import psycopg2
from typing import Any, Union
from enum import Enum

from env import CONNECTION_STRING
from model import Puzzle

class Fetch(Enum):
    ONE = 0
    ALL = 1

class Database:
    def __init__(self):
        self.connection_string = CONNECTION_STRING
        self.connection = None

    def commit_query(self, query: str, vars: Any = None, fetch: Union[Fetch, None] = None, message: Union[str, None] = None) -> Any:
        try:
            self.connection = psycopg2.connect(self.connection_string)
            with self.connection.cursor() as cur:
                cur.execute(query=query, vars=vars)
                result = None
                if fetch:
                    match fetch:
                        case Fetch.ONE:
                            result = cur.fetchone()
                        case Fetch.ALL:
                            result = cur.fetchall()
                self.connection.commit()
                if message:
                    print(message)
                return result
        except Exception as e:
            print(f"Error: {e}")
            if self.connection:
                self.connection.rollback()
        finally:
            if self.connection:
                self.connection.close()

    def drop_table(self, table_name: str) -> None:
        query = f"""
            DROP TABLE IF EXISTS {table_name};
        """
        self.commit_query(
            query=query, 
            message=f"Dropped {table_name} table successfully (if it existed)"
        )

    def create_puzzle_table(self) -> None:
        self.drop_table(table_name="pokelink_puzzle")
        query = """
            CREATE TABLE pokelink_puzzle (
                date DATE PRIMARY KEY,
                source TEXT NOT NULL,
                target TEXT NOT NULL,
                shortest_path TEXT[] NOT NULL,
                shortest_path_length INT NOT NULL
            );
        """
        self.commit_query(
            query=query,
            message="Created pokelink_puzzle table successfully"
        )

    def get_puzzle(self, date: str) -> Union[Puzzle, None]:
        query = """
            SELECT source, target, shortest_path, shortest_path_length FROM pokelink_puzzle
            WHERE date = %s;
        """

        fetched_row = self.commit_query(
            query=query,
            vars=(date,),
            fetch=Fetch.ONE,
            message="Got puzzle data successfully"
        )

        if not fetched_row:
            return None
        
        source, target, shortest_path, shortest_path_length = fetched_row
        return Puzzle(
            date=date,
            source=source, 
            target=target, 
            shortest_path=shortest_path, 
            shortest_path_length=shortest_path_length
        )
    
    def set_puzzle(self, puzzle: Puzzle) -> None:
        query2 = """
            INSERT INTO pokelink_puzzle (date, source, target, shortest_path, shortest_path_length)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (date) DO UPDATE SET 
                source = EXCLUDED.source,
                target = EXCLUDED.target,
                shortest_path = EXCLUDED.shortest_path,
                shortest_path_length = EXCLUDED.shortest_path_length
        """
        self.commit_query(
            query=query2, 
            vars=(puzzle.date, puzzle.source, puzzle.target, puzzle.shortest_path, puzzle.shortest_path_length),
            message=f"Set puzzle data from {puzzle.source} to {puzzle.target} successfully"
        )

    def get_puzzle_dates(self, page: int) -> list[tuple[str, str, str]]:
        query = """
            SELECT date, source, target
            FROM pokelink_puzzle
            ORDER BY date DESC
            LIMIT 10 OFFSET %s
        """

        offset = page * 10 - 10

        fetched_data = self.commit_query(
            query=query,
            vars=(offset,),
            fetch=Fetch.ALL,
            message="Got puzzle dates successfully"
        )

        return [
            (date.strftime('%Y-%m-%d'), source, target)
            for date, source, target in fetched_data
        ] if fetched_data else []

    def get_closest_date(self, date: datetime) -> str:
        query = """
            SELECT date
            FROM pokelink_puzzle
            ORDER BY ABS(DATE_PART('day', date - %s))
            LIMIT 1;
        """

        fetched_row = self.commit_query(
            query=query,
            vars=(date,),
            fetch=Fetch.ONE,
            message="Got closest date successfully"
        )

        return str(fetched_row[0])

    def create_user_solution_table(self) -> None:
        self.drop_table(table_name="pokelink_user_solution")
        query = """
            CREATE TABLE pokelink_user_solution (
                userid UUID NOT NULL,
                date DATE NOT NULL,
                solution TEXT[] NOT NULL,
                PRIMARY KEY (userid, date)
            );
        """

        self.commit_query(
            query=query,
            message="Created pokelink_user_solution table successfully"
        )

    def set_user_solution(self, userid: str, date: str, solution: list[str]) -> None:
        query = """
            INSERT INTO pokelink_user_solution (userid, date, solution)
            VALUES (%s, %s, %s)
        """
        
        self.commit_query(
            query=query,
            vars=(userid, date, solution),
            message="Set user solution successfully")
    
    def get_user_solution(self, userid: str, date: str) -> Union[list[str], None]:
        query = """
            SELECT solution from pokelink_user_solution
            WHERE userid = %s
            AND date = %s
        """
        
        solution = self.commit_query(
            query=query,
            vars=(userid, date),
            fetch=Fetch.ONE,
            message="Got user solution successfully"
        )

        # Returns the solution if it exists, otherwise None
        return solution[0] if solution else None

    def get_completed_puzzles(self, userid: str) -> list[str]:
        query = """
            SELECT date from pokelink_user_solution
            WHERE userid = %s
        """

        dates = self.commit_query(
            query=query,
            vars=(userid,),
            fetch=Fetch.ALL,
            message="Got completed puzzles successfully"
        )

        return [str(row[0]) for row in dates] if dates else []

    def delete_puzzle_by_date(self, date: date) -> None:
        query = """
            DELETE FROM pokelink_puzzle
            WHERE date = %s;
        """

        self.commit_query(
            query=query,
            vars=(date,),
            fetch=None,
            message=f"Deleted puzzles for date {date}"
        )

    def get_num_puzzles(self) -> int:
        query = "SELECT COUNT(*) from pokelink_puzzle"

        num_puzzles = self.commit_query(
            query=query,
            fetch=Fetch.ONE,
            message="Got number of puzzles successfully"
        )[0]

        return num_puzzles

    def get_all_puzzle_dates(self) -> set[datetime]:
        query = "SELECT date FROM pokelink_puzzle;"

        rows = self.commit_query(
            query=query,
            vars=None,
            fetch=Fetch.ALL,
            message="Fetched all puzzle dates"
        )
        return {row[0] for row in rows}  # row[0] = date string
