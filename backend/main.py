from dotenv import load_dotenv
from fastapi import FastAPI
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
    return bn.graph_data

@app.get("/puzzle")
def get_puzzle() -> Puzzle:
    return bn.get_puzzle()

@app.get("/puzzle/{date}")
def get_puzzle(date: str) -> Puzzle:
    return bn.get_puzzle(date)


@app.get("/hint")
def get_hint(source: str, target: str) -> PokemonNode:
    return bn.get_hint(source, target)
