import pickle
from networkx import Graph
import psycopg2, os
from typing import Any, Union
from dotenv import load_dotenv
from enum import Enum

from date import get_date_str
from graph_data_generation import generate_graph
from model import Puzzle

class Fetch(Enum):
    ONE = 0
    ALL = 1

class Database:
    def __init__(self):
        load_dotenv()
        self.connection_string = os.getenv("CONNECTION_STRING")
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
        self.drop_table(table_name="puzzle")
        query = """
            CREATE TABLE puzzle (
                date DATE PRIMARY KEY,
                source TEXT NOT NULL,
                target TEXT NOT NULL,
                shortest_path TEXT[] NOT NULL,
                shortest_path_length INT NOT NULL
            );
        """
        self.commit_query(query=query, message="Created puzzle table successfully")

    def get_puzzle(self, date: Union[str, None] = None) -> Union[Puzzle, None]:
        query = """
            SELECT source, target, shortest_path, shortest_path_length FROM puzzle
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
            source=source, 
            target=target, 
            shortest_path=shortest_path, 
            shortest_path_length=shortest_path_length
        )
    
    def set_puzzle(self, date: str, puzzle: Puzzle):
        query2 = """
            INSERT INTO puzzle (date, source, target, shortest_path, shortest_path_length)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.commit_query(
            query=query2, 
            vars=(date, puzzle.source, puzzle.target, puzzle.shortest_path, puzzle.shortest_path_length)
        )
