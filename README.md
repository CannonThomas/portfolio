# AI Search & Decision Engine

A learning-first Python laboratory for understanding how agents choose paths.
V1 implements A* from scratch, with uniform-cost search as an optimal-cost baseline.
A local Tkinter playground visualizes the engine's recorded expansion order.

## Run

From this repository folder:

```sh
conda activate a26
python app.py
```

Python 3.11+ and Tkinter are required. There are no pip dependencies for V1.
The existing a26 environment was detected with Tkinter available.

Paint walls or cost-5 terrain, move start/goal, and press Run. Pause/Resume and
Step control playback. Compare runs both algorithms on exactly the same map.
Reset map restores the example. Editing clears previous results.

## What the numbers mean

- **Expanded:** valid priority-queue removals, including the goal.
- **Discovered:** unique states with a tentative cost, including the start.
- **Cost:** sum of entry costs along the path; the start costs zero.
- **Time:** engine wall-clock time including trace recording, excluding validation
  and animation. One tiny run is illustrative, not a reliable benchmark.
- **Optimality:** A* cost compared with uniform-cost search. Tests also check both
  against an independent repeated-relaxation oracle.

Four-way movement only. All movement costs must be finite and positive.
A* uses Manhattan distance scaled by a lower bound on movement cost.
Equal priorities use insertion order so playback is deterministic.

## Structure

```text
engine/search.py       Grid model, A*, UCS, structured results
app.py                 Desktop visualization and playback
 tests/test_search.py  Known cases and 60 seeded oracle comparisons
 docs/astar.md         Theory, design choices, and exercises
 docs/roadmap.md       Class-driven milestones
.github/workflows/     Automated correctness checks
```

## Verify

```sh
python -m unittest discover -s tests -v
```

## GitHub Desktop

Choose File → Add Local Repository and select this folder. Then use Publish
repository to choose visibility and publish through your signed-in account.
No remote repository is created by the local build.

## Current limits

This release is local desktop software. Playback shows expansions and the final
path; it does not yet display the live frontier or per-cell g/h/f scores. BFS, DFS,
Greedy Best-First, reinforcement learning, and a hosted web UI are future work.
The UI uses a fixed 26 × 16 map. There are no paid services or account requirements.

## Honest interview description today

“I implemented A* and uniform-cost search in Python, built an interactive weighted
 grid visualizer, and verified optimal path costs against an independent oracle.”

Extend that claim as you complete later milestones, and be ready to explain the
heuristic, stale queue entries, weighted terrain, and testing strategy.
