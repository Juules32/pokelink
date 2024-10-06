import psycopg2, os, json
from typing import Any, Union
from dotenv import load_dotenv
from enum import Enum

class Fetch(Enum):
    ONE = 0
    ALL = 1

class Database:
    def __init__(self, connection_string):

        self.connection_string = connection_string
        try:
            self.connection = psycopg2.connect(self.connection_string)
            print("Connection to the database established successfully")
        except Exception as e:
            print(f"Error: {e}")    

    def commit_query(self, query: str, vars: Any = None, fetch: Union[Fetch, None] = None, message: Union[str, None] = None) -> Any:
        try:
            with self.connection.cursor() as cur:
                cur.execute(query=query, vars=vars)
                result = None
                if fetch:
                    match fetch:
                        case Fetch.ONE:
                            result = cur.fetchone()
                            if result:
                                result = result[0]
                        case Fetch.ALL:
                            result = cur.fetchall()
                self.connection.commit()
                if message:
                    print(message)
                return result
        except Exception as e:
            print(f"Error: {e}")
            self.connection.rollback()

    def create_graph_table(self):
        self.drop_table(table_name="graph")

        query = """
            CREATE TABLE graph (
                data JSON NOT NULL
            );
        """
        self.commit_query(query=query, message="Created graph table successfully")

    def drop_table(self, table_name: str) -> None:
        query = f"""
            DROP TABLE IF EXISTS {table_name};
        """
        self.commit_query(
            query=query, 
            message=f"Dropped {table_name} table successfully (if it existed)"
        )

    def get_graph(self) -> dict:
        query = """
            SELECT data FROM graph;
        """
        data: dict = self.commit_query(
            query=query, 
            fetch=Fetch.ONE, 
            message=f"Got graph data successfully"
        )
        return data

    def set_graph(self, data: dict):
        query1 = """
            DELETE FROM graph;
        """
        self.commit_query(query=query1)
        
        data_string: str = json.dumps(data)

        query2 = """
            INSERT INTO graph (data)
            VALUES (%s)
        """
        self.commit_query(query=query2, vars=(data_string,))

load_dotenv()

connection_string = os.getenv("CONNECTION_STRING")

db = Database(connection_string)

# Running this script sets up the database tables
if __name__ == "__main__":
    db.create_graph_table()
