import psycopg2
from typing import Any, Union
from enum import Enum

from env import CONNECTION_STRING
from date import get_date_str
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
            self.connection.rollback()
        finally:
            self.connection.close()

    def drop_table(self, table_name: str):
        query = f"""
            DROP TABLE IF EXISTS {table_name};
        """
        self.commit_query(
            query=query, 
            message=f"Dropped {table_name} table successfully (if it existed)"
        )

    def create_puzzle_table(self):
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
        self.commit_query(query=query, message="Created pokelink_puzzle table successfully")

    def get_puzzle(self, date: Union[str, None] = None) -> Union[Puzzle, None]:
        query = """
            SELECT source, target, shortest_path, shortest_path_length FROM pokelink_puzzle
            WHERE date = %s;
        """
        fetched_row = self.commit_query(
            query=query,
            vars=(date if date else get_date_str(),),
            fetch=Fetch.ONE,
            message=f"Got puzzle data successfully"
        )

        if not fetched_row:
            return None
        
        source, target, shortest_path, shortest_path_length = fetched_row
        return Puzzle(
            date=date if date else get_date_str(),
            source=source, 
            target=target, 
            shortest_path=shortest_path, 
            shortest_path_length=shortest_path_length
        )
    
    def set_puzzle(self, puzzle: Puzzle):
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
            vars=(puzzle.date, puzzle.source, puzzle.target, puzzle.shortest_path, puzzle.shortest_path_length)
        )

    def get_puzzle_dates(self) -> list[tuple[str, str, str]]:
        query = "SELECT date, source, target FROM pokelink_puzzle ORDER BY date DESC"
        fetched_data = self.commit_query(
            query=query,
            fetch=Fetch.ALL
        )
        return [
            (str(date), source, target)
            for date, source, target in fetched_data
        ]
