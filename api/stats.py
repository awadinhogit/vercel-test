# api/stats.py
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Union
import math

app = FastAPI()

# ---- Health (helps verify the exact path FastAPI sees in prod) ----
@app.get("")
@app.get("/")
@app.get("/api/stats")
@app.get("/api/stats/")
async def health(req: Request):
    return {"ok": True, "path": req.url.path}

class NumbersIn(BaseModel):
    numbers: Union[str, List[float]]

def parse_numbers(value: Union[str, List[float]]) -> List[float]:
    if isinstance(value, list):
        return [float(x) for x in value]
    tokens = str(value).replace(",", " ").split()
    out: List[float] = []
    for t in tokens:
        try:
            out.append(float(t))
        except ValueError:
            raise HTTPException(status_code=400, detail="Input must be numbers separated by commas/spaces")
    if not out:
        raise HTTPException(status_code=400, detail="No numbers provided")
    return out

# ---- Support BOTH adapter behaviors (root & prefixed) ----
@app.post("")
@app.post("/")
@app.post("/api/stats")
@app.post("/api/stats/")
def stats(payload: NumbersIn):
    nums = parse_numbers(payload.numbers)
    nums_sorted = sorted(nums)
    n = len(nums)
    mean = sum(nums) / n
    median = nums_sorted[n // 2] if n % 2 else (nums_sorted[n // 2 - 1] + nums_sorted[n // 2]) / 2
    var_pop = sum((x - mean) ** 2 for x in nums) / n
    var_samp = sum((x - mean) ** 2 for x in nums) / (n - 1) if n > 1 else float("nan")

    return {
        "count": n,
        "sum": sum(nums),
        "mean": mean,
        "median": median,
        "min": min(nums),
        "max": max(nums),
        "stdevPopulation": math.sqrt(var_pop),
        "stdevSample": math.sqrt(var_samp),
        "sorted": nums_sorted,
    }
