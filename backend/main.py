from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model import PokemonNode, Puzzle
from business import Business
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bn = Business()

@app.get("/graph_data")
def get_test():
    graph = bn.get_graph()
    return bn.get_graph_data(graph)

@app.get("/puzzle")
def get_puzzle() -> Puzzle:
    return bn.get_puzzle()

@app.get("/puzzle/{date}")
def get_puzzle(date: str) -> JSONResponse:
    puzzle = bn.get_puzzle(date)
    if not puzzle:
        return JSONResponse(content={"error": "Puzzle not found"},status_code=404)
    return JSONResponse(content=puzzle.model_dump(), status_code=200)

@app.get("/hint")
def get_hint(source: str, target: str) -> str:
    graph = bn.get_graph()
    return bn.get_hint(graph, source, target)
