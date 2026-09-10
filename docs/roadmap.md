# Class-driven roadmap

1. **V1 — A***: weighted grid, from-scratch heap search, expansion playback, UCS
   comparison, independent correctness tests. Implemented.
2. **Search foundations**: add BFS and DFS when covered in class. Compare BFS
   optimality on uniform-cost maps with failures on weighted maps. Record DFS
   dependence on neighbor order. Add a shared search interface and trace events.
3. **Heuristic search**: add Greedy Best-First and explicit per-state g/h/f values.
   Compare optimality, expansions, and repeated timing distributions across a
   reproducible map suite. Export experiment data.
4. **Web presentation**: retain the Python engine and add an API plus browser UI.
   Choose hosting after checking Python runtime support and current service plans.
   Build a live demo, screenshots, architecture diagram, and reproducible examples.
5. **Reinforcement learning**: introduce Gymnasium Blackjack after the class covers
   learning from rewards. Pin environment rules and seeds; start with a documented
   fixed policy, implement tabular learning, and evaluate on held-out games.
   Report reward distributions and uncertainty, not just a training win rate.
6. **Interview readiness**: write a case study covering one hypothesis, a failed
   approach, measured findings, algorithm guarantees, and engineering tradeoffs.

Blackjack is a simulation for studying policies; optimality depends on the exact
rules. Search and learning belong in separate engine modules with shared reporting.
