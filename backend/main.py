from typing import Union
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
def get_graph_data() -> JSONResponse:
    graph = bn.get_graph()
    return JSONResponse(content=bn.get_graph_data(graph).model_dump(), status_code=200)

@app.get("/puzzle")
def get_puzzle() -> JSONResponse:
    return get_puzzle(None)

@app.get("/puzzle/{date}")
def get_puzzle(date: Union[str, None]) -> JSONResponse:
    puzzle = bn.get_puzzle(date)
    if not puzzle:
        return JSONResponse(content={"error": "Puzzle not found"},status_code=404)
    return JSONResponse(content=puzzle.model_dump(), status_code=200)

@app.get("/hint")
def get_hint(source: str, target: str) -> JSONResponse:
    graph = bn.get_graph()
    return JSONResponse(content=bn.get_hint(graph, source, target), status_code=200)
