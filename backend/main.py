from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from env import CRON_SECRET
from database import Database
from date import get_date_str
from business import Business
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/cron/generate/puzzle")
def generate_daily_data(request: Request) -> JSONResponse:
    authorization_header = request.headers.get("authorization")

    if not authorization_header:
        return JSONResponse({"error": "Missing authorization header"}, status_code=401)

    if authorization_header != f"Bearer {CRON_SECRET}":
        return JSONResponse({"error": "Invalid authorization header"}, status_code=403)

    new_puzzle = bn.generate_puzzle(bn.get_graph(), strict=True)
    Database().set_puzzle(get_date_str(1), new_puzzle)
    print("Set tomorrow's puzzle successfully!")

    return JSONResponse({"result": "success"}, status_code=200)
