# Understanding the A* implementation

A state is one grid coordinate. An action moves to an adjacent open cell.
The transition cost is the destination cell's terrain cost. The search problem
asks for a minimum-cost path from start to goal.

A* prioritizes **f(n) = g(n) + h(n)**. Here g is the best known cost from start,
and h is Manhattan distance to goal multiplied by a lower bound on step cost.
Each four-way move can reduce Manhattan distance by at most one. Obstacles only
make a route longer. Consequently this heuristic never overestimates the remaining
cost (admissibility), and satisfies h(n) ≤ cost(n,m) + h(m) (consistency).
With these assumptions, removing the goal from the priority queue gives an optimal
path. Discovering the goal is not sufficient to stop.

Setting h to zero gives uniform-cost search. Both implementations share the
queue loop so that their behavioral difference is the heuristic itself.
The tests use a separate relaxation algorithm to avoid treating shared code as
independent proof of correctness.

The heap stores priority, tie sequence, g, and coordinate. If a cheaper route is
found later, we push a new entry rather than editing the heap in place. An older
entry is skipped when its g differs from the best known g. Parent pointers rebuild
the final path. The sequence number makes equal-priority choices reproducible.

For this finite grid with the consistent heuristic, time is O((V+E) log V) and
space O(V+E), including lazy heap entries and the expansion trace; E ≤ 4V here.
A heuristic does not guarantee a dramatic speedup: ties on open grids can cause
A* to expand many states with the same f score. Timings also fluctuate.

## First learning session

1. On paper, calculate g, h, and f for the start and its neighbors.
2. Run the example one expansion at a time. Explain which state should come next.
3. Paint an expensive direct route. Explain why the shortest path in steps may
   differ from the cheapest path.
4. Compare A* and UCS. Check cost equality before comparing expansion counts.
5. Explain why multiplying h by an arbitrary number greater than one can break
   the guarantee. Keep such experiments separate from the verified algorithm.

Next improvement: expose frontier snapshots and g/h/f values without coupling
the engine to the UI. Keep a short experiment log of predictions and outcomes.
