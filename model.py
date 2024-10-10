from pydantic import BaseModel

class Puzzle(BaseModel):
    source: str
    target: str
    shortest_path: list[str]
    shortest_path_length: int
