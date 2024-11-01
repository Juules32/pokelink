from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from model import PuzzleResponse, SolutionRequest
from env import CRON_SECRET
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
def get_puzzle(userid: str) -> JSONResponse:
    return get_puzzle(get_date_str(), userid)

@app.get("/puzzle/{date}")
def get_puzzle(date: str, userid: str) -> JSONResponse:
    puzzle = bn.get_puzzle(date)
    if not puzzle:
        return JSONResponse(content="Puzzle not found", status_code=404)
    
    solution = bn.db.get_user_solution(userid, date)

    puzzle_response = PuzzleResponse(
        puzzle=puzzle,
        solution=solution
    )

    return JSONResponse(content=puzzle_response.model_dump(), status_code=200)

@app.get("/puzzles")
def get_puzzles(userid: str) -> JSONResponse:
    return bn.get_puzzles(userid)

@app.get("/hint")
def get_hint(source: str, target: str) -> JSONResponse:
    graph = bn.get_graph()
    return JSONResponse(content=bn.get_hint(graph, source, target), status_code=200)

@app.get("/cron/generate/puzzle")
def generate_daily_data(request: Request) -> JSONResponse:
    authorization_header = request.headers.get("authorization")

    if not authorization_header:
        return JSONResponse(content="Missing authorization header", status_code=401)

    if authorization_header != f"Bearer {CRON_SECRET}":
        return JSONResponse(content="Invalid authorization header", status_code=403)

    new_puzzle = bn.generate_puzzle(bn.get_graph(), get_date_str(1), strict=True)
    bn.db.set_puzzle(new_puzzle)
    print("Set tomorrow's puzzle successfully!")

    return JSONResponse(content="Success", status_code=200)

@app.post("/solution/{date}")
def post_solution(solution_request: SolutionRequest, date: str) -> JSONResponse:
    if not bn.validate_solution(solution_request.solution):
        return JSONResponse(content="Invalid Solution", status_code=400)

    bn.db.set_user_solution(userid=solution_request.userid, date=date, solution=solution_request.solution)
    return JSONResponse(content="Solution set successfully", status_code=200)
