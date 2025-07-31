from collections import defaultdict
from math import log
from pathlib import Path
import json
from typing import List, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ortools.linear_solver import pywraplp
from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float
    rating: float


DATA_FILE = Path(__file__).parent / "products.json"
# Load and parse using Pydantic


def load_products() -> List[Product]:
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        return [Product(**item) for item in data]


PRODUCTS: List[Product] = load_products()


def calculate_values(data: List[Product], w_r: float = 0.7, w_p: float = 0.3) -> Dict[int, float]:
    values = {}
    # Group products by category
    cat_groups = defaultdict(list)
    for p in data:
        cat_groups[p.category].append(p)

    # Normalize within each category
    for cat, items in cat_groups.items():
        min_r = min(p.rating for p in items)
        max_r = max(p.rating for p in items)
        min_p = min(p.price for p in items)
        max_p = max(p.price for p in items)

        for p in items:
            norm_r = (p.rating - min_r) / (max_r - min_r) if max_r > min_r else 1.0
            norm_p = (p.price - min_p) / (max_p - min_p) if max_p > min_p else 1.0
            # Weighted score: higher rating better, lower price better
            values[p.id] = w_r * norm_r - w_p * log(norm_p + 1)

    return values


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def optimize_best_value(products: List[Product], budget: float, team_size: int = 5):
    values = calculate_values(products)
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Decision variables
    x = {}
    for i, p in enumerate(products):
        x[i] = solver.BoolVar(f'x_{i}')

    # Objective: maximize sum(rating / price)
    solver.Maximize(solver.Sum(x[i] * (values[p.id]) for i, p in enumerate(products)))

    # Budget constraint
    solver.Add(solver.Sum(x[i] * p.price for i, p in enumerate(products)) <= budget)

    # Category constraint: exactly one per category
    categories = set(p.category for p in products)
    for cat in categories:
        solver.Add(solver.Sum(x[i] for i, p in enumerate(products) if p.category == cat) <= 1)

    # Select exactly 5 products
    solver.Add(solver.Sum(x[i] for i in range(len(products))) == team_size)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        return [products[i] for i in range(len(products)) if x[i].solution_value() > 0.5]
    else:
        return []


@app.get("/team-builder", response_model=List[Product])
async def team_builder(budget: float) -> List[Product]:
    return optimize_best_value(PRODUCTS, budget)
