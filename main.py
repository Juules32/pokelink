# main.py

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from db import Database

load_dotenv()

app = FastAPI()
db = Database()

@app.get("/graph")
def get_test():
    return JSONResponse(content=db.get_graph(), status_code=200)
