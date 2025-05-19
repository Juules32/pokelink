from fastapi import FastAPI, HTTPException, Request
from exceptions import InvalidSolutionException, NotFoundException
from model import GraphData, PuzzleSolution, PuzzlesItem, SolutionRequest
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
def get_graph_data() -> GraphData:
    try:
        graph = bn.get_graph()
        return bn.get_graph_data(graph)
    except Exception:
        raise HTTPException(status_code=500, detail="Could not get graph data")

@app.get("/puzzle")
def get_today_puzzle(userid: str) -> PuzzleSolution:
    return get_puzzle(get_date_str(), userid)

@app.get("/puzzle/{date}")
def get_puzzle(date: str, userid: str) -> PuzzleSolution:
    try:
        return bn.get_puzzle_solution(date, userid)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Could not get puzzle")

@app.get("/puzzles")
def get_puzzles(userid: str, page: int) -> list[PuzzlesItem]:
    try:
        return bn.get_puzzles(userid, page)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Could not get puzzles")

@app.get("/num_puzzles")
def get_num_puzzles() -> int:
    try:
        return bn.get_num_puzzles()
    except Exception:
        raise HTTPException(status_code=500, detail="Could not get number of puzzles")

@app.get("/hint")
def get_hint(source: str, target: str) -> str:
    try:
        graph = bn.get_graph()
        return bn.get_hint(graph, source, target)
    except Exception:
        raise HTTPException(status_code=500, detail="Could not get hint")

@app.get("/cron/generate/puzzle")
def generate_daily_data(request: Request) -> None:
    authorization_header = request.headers.get("authorization")

    if not authorization_header:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    if authorization_header != f"Bearer {CRON_SECRET}":
        raise HTTPException(status_code=403, detail="Invalid authorization header")

    new_puzzle = bn.generate_puzzle(bn.get_graph(), get_date_str(1), strict=True)
    bn.db.set_puzzle(new_puzzle)
    print("Set tomorrow's puzzle successfully!")

@app.post("/solution/{date}")
def post_solution(solution_request: SolutionRequest, date: str) -> None:
    try:
        bn.set_user_solution(userid=solution_request.userid, date=date, solution=solution_request.solution)
    except InvalidSolutionException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except:
        raise HTTPException(status_code=500, detail="Could not set solution")
