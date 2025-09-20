from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union
from fastapi.middleware.cors import CORSMiddleware
import math

app = FastAPI()

# Allow localhost / 127.0.0.1 on any port for dev
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^http://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_methods=["*"],
    allow_headers=["*"],
)


class NumbersIn(BaseModel):
    numbers: Union[str, List[float]]


@app.post("/")
def stats(payload: NumbersIn):
    # Parse input numbers
    if isinstance(payload.numbers, str):
        try:
            nums = [float(x) for x in payload.numbers.replace(",", " ").split()]
        except ValueError:
            raise HTTPException(status_code=400, detail="Input must be numbers separated by spaces/commas")
    else:
        nums = payload.numbers

    if not nums:
        raise HTTPException(status_code=400, detail="No numbers provided")

    nums_sorted = sorted(nums)
    n = len(nums)
    mean = sum(nums) / n
    median = nums_sorted[n // 2] if n % 2 == 1 else (nums_sorted[n // 2 - 1] + nums_sorted[n // 2]) / 2
    stdev_pop = math.sqrt(sum((x - mean) ** 2 for x in nums) / n)
    stdev_sample = math.sqrt(sum((x - mean) ** 2 for x in nums) / (n - 1)) if n > 1 else float("nan")

    return {
        "count": n,
        "sum": sum(nums),
        "mean": mean,
        "median": median,
        "min": min(nums),
        "max": max(nums),
        "stdevPopulation": stdev_pop,
        "stdevSample": stdev_sample,
        "sorted": nums_sorted,
    }
