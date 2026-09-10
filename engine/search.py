"""Inspectable A* and uniform-cost search on positive-cost, four-way grids."""
from dataclasses import dataclass, field
from heapq import heappop, heappush
from itertools import count
from time import perf_counter
import math

Cell = tuple[int, int]

@dataclass
class Grid:
    width: int
    height: int
    walls: set[Cell] = field(default_factory=set)
    weights: dict[Cell, float] = field(default_factory=dict)

    def valid(self, cell):
        x, y = cell
        return 0 <= x < self.width and 0 <= y < self.height

    def validate(self, start, goal):
        if self.width < 1 or self.height < 1:
            raise ValueError("Grid dimensions must be positive.")
        if any(not self.valid(c) for c in self.walls | self.weights.keys()):
            raise ValueError("Terrain must be inside the grid.")
        if any(not math.isfinite(w) or w <= 0 for w in self.weights.values()):
            raise ValueError("Movement costs must be finite and positive.")
        if any(not self.valid(c) or c in self.walls for c in (start, goal)):
            raise ValueError("Start and goal must be open cells inside the grid.")

    def neighbors(self, cell):
        x, y = cell
        for c in ((x+1,y), (x,y+1), (x-1,y), (x,y-1)):
            if self.valid(c) and c not in self.walls:
                yield c

@dataclass
class Result:
    path: list[Cell]
    expanded: list[Cell]
    discovered: int
    cost: float | None
    elapsed_ms: float
    algorithm: str


def search(grid: Grid, start: Cell, goal: Cell, algorithm="astar") -> Result:
    """Cost is paid on entry; start costs zero. Stable ties use insertion order.

    A* uses Manhattan distance times a lower bound on step cost. Setting h=0
    yields uniform-cost search. No search/pathfinding libraries are used.
    """
    grid.validate(start, goal)
    if algorithm not in ("astar", "ucs"):
        raise ValueError("Choose astar or ucs.")
    begin = perf_counter()
    minimum = min(1.0, *grid.weights.values()) if grid.weights else 1.0
    def heuristic(c):
        return minimum * (abs(c[0]-goal[0]) + abs(c[1]-goal[1])) if algorithm == "astar" else 0
    serial = count()
    frontier = [(heuristic(start), next(serial), 0.0, start)]
    best = {start: 0.0}
    parent = {}
    expanded = []
    path = []
    final_cost = None
    while frontier:
        _, _, cost, current = heappop(frontier)
        if cost != best[current]:  # An improved route superseded this queue entry.
            continue
        expanded.append(current)
        if current == goal:
            final_cost = cost
            path = [current]
            while current != start:
                current = parent[current]
                path.append(current)
            path.reverse()
            break
        for neighbor in grid.neighbors(current):
            candidate = cost + grid.weights.get(neighbor, 1.0)
            if candidate < best.get(neighbor, math.inf):
                best[neighbor] = candidate
                parent[neighbor] = current
                heappush(frontier, (candidate + heuristic(neighbor), next(serial), candidate, neighbor))
    return Result(path, expanded, len(best), final_cost,
                  (perf_counter()-begin)*1000, algorithm)
