# api/stats.py
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Union
import math

app = FastAPI()

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
            raise HTTPException(
                status_code=400,
                detail="Input must be numbers separated by commas/spaces",
            )
    if not out:
        raise HTTPException(status_code=400, detail="No numbers provided")
    return out

# --- Health routes (catch both "" and any subpath) ---
@app.api_route("", methods=["GET"])
@app.api_route("/{rest:path}", methods=["GET"])
async def health(req: Request, rest: str | None = None):
    # Show the exact path FastAPI sees (for debugging)
    return {"ok": True, "path": req.url.path}

# --- Stats routes (catch both "" and any subpath) ---
@app.api_route("", methods=["POST"])
@app.api_route("/{rest:path}", methods=["POST"])
def stats(payload: NumbersIn, rest: str | None = None):
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
