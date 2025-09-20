# api/stats.py
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Union
import math

app = FastAPI()

# --- Health + path debug (helps validate routing) ---
@app.get("")
@app.get("/")
async def health(req: Request):
    # Return what FastAPI thinks the path is
    return {"ok": True, "path": req.url.path}

# --- Input model ---
class NumbersIn(BaseModel):
    numbers: Union[str, List[float]]

# --- Helpers ---
def parse_numbers(value: Union[str, List[float]]) -> List[float]:
    if isinstance(value, list):
        return [float(x) for x in value]
    tokens = str(value).replace(",", " ").split()
    try:
        return [float(t) for t in tokens]
    except ValueError:
        raise HTTPException(status_code=400, detail="Input must be numbers separated by commas/spaces")

# Support BOTH /api/stats and /api/stats/ (root inside the function)
@app.post("")
@app.post("/")
def stats(payload: NumbersIn):
    nums = parse_numbers(payload.numbers)
    if not nums:
        raise HTTPException(status_code=400, detail="No numbers provided")

    nums_sorted = sorted(nums)
    n = len(nums)
    mean = sum(nums) / n
    median = nums_sorted[n//2] if n % 2 else (nums_sorted[n//2 - 1] + nums_sorted[n//2]) / 2
    stdev_pop = math.sqrt(sum((x - mean) ** 2 for x in nums) / n)
    stdev_sample = math.sqrt(sum((x - mean) ** 2 for x in nums) / (n - 1)) if n > 1 else float("nan")

    return {
        "count": n, "sum": sum(nums), "mean": mean, "median": median,
        "min": min(nums), "max": max(nums),
        "stdevPopulation": stdev_pop, "stdevSample": stdev_sample,
        "sorted": nums_sorted,
    }
