from fastapi import FastAPI, HTTPException, Request
from exceptions import InvalidSolutionException, NotFoundException
from model import GraphData, PuzzleSolution, PuzzlesItem, SolutionRequest
from env import CRON_SECRET
from util import format_date, get_date, to_date
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
        return bn.graph_data
    except Exception:
        raise HTTPException(status_code=500, detail="Could not get graph data")

@app.get("/puzzle")
def get_home_puzzle(userid: str) -> PuzzleSolution:
    closest_date = bn.db.get_closest_date(get_date())
    if not closest_date:
        raise HTTPException(status_code=404, detail=str("No home puzzle date found 🍃"))
    return get_puzzle(format_date(closest_date), userid)

@app.get("/puzzle/{date_str}")
def get_puzzle(date_str: str, userid: str) -> PuzzleSolution:
    try:
        return bn.get_puzzle_solution(to_date(date_str), userid)
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

@app.post("/solution/{date_str}")
def post_solution(solution_request: SolutionRequest, date_str: str) -> None:
    try:
        bn.set_user_solution(solution_request.userid, to_date(date_str), solution_request.solution)
    except InvalidSolutionException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except:
        raise HTTPException(status_code=500, detail="Could not set solution")

# Removes old puzzles and generates new ones (that don't already exist)
@app.get("/cron/update/puzzles")
def get_cron_update_puzzles(request: Request) -> None:
    authorization_header = request.headers.get("authorization")

    if not authorization_header:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    if authorization_header != f"Bearer {CRON_SECRET}":
        raise HTTPException(status_code=403, detail="Invalid authorization header")

    all_dates = {
        get_date(i)
        for i in range(1, -99, -1)
    }

    existing_dates = bn.db.get_all_puzzle_dates()
    missing_dates = all_dates - existing_dates

    # Generates new puzzles for all dates that don't already have puzzles
    # (within the last 100 days)
    for date in sorted(missing_dates):
        new_puzzle = bn.generate_puzzle(bn.get_graph(), date, strict=True)
        bn.db.set_puzzle(new_puzzle)
        print(f"Set puzzle for date {date} successfully!")
    
    # Removes puzzles older than 99 days
    cutoff_date = get_date(-99)
    for old_date in [date for date in existing_dates if date <= cutoff_date]:
        bn.db.delete_puzzle_by_date(old_date)    
