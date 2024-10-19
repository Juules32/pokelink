# main.py

from dotenv import load_dotenv
from fastapi import FastAPI
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

@app.get("/graph")
def get_test():
    return bn.get_graph()

@app.get("/puzzle")
def get_puzzle():
    return bn.get_puzzle()

@app.get("/puzzle/{date}")
def get_puzzle(date: str):
    return bn.get_puzzle(date)

@app.get("/adjacency_data/{guess}")
def get_adjacency_data(guess: str):
    return bn.get_adjacency_data(guess)
