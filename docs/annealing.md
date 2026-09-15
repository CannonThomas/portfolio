# Simulated annealing: Route Lab

Visit 18 cities exactly once, then return to the starting city. Minimize the sum
of Euclidean distances. There are no road constraints; lines may cross.

A state is a complete permutation of cities. A neighbor reverses a segment of
that tour (a 2-opt move). The energy is total tour length. For a proposed change
Δ = candidate cost − current cost, accept improvements and ties. Accept a worse
move with probability exp(−Δ/T). At T = 0, reject all worse moves.

After each proposal, T is multiplied by the cooling factor. The displayed
“Temperature used” is the temperature at which that move was evaluated.
The route shown is the accepted state after the proposal; rejected candidate
routes aren't drawn. “Proposed change” always describes that proposal.

Keep a separate best-so-far tour: a deliberately exploratory current state can
be worse than an earlier one. The best recorded cost never increases.

The comparison is stochastic hill climbing with the same initial tour, same
sequence of segment-index proposals, and same number of moves. Its state may
diverge, so the resulting candidate tours need not match. Separate seeded random
generators keep maps, proposals, and acceptance draws reproducible. With T = 0,
annealing and hill climbing follow the same trajectory.

## Experiments

1. Keep seed 26 and run temperature 0, then 20. Compare costs and accepted uphill moves.
2. Keep temperature 20; compare cooling 0.98, 0.995, and 0.999. Record the best
   distance after the same budget. Slower cooling isn't automatically better.
3. Try multiple seeds before claiming one method wins. Report the distribution
   of final best distances, not a single favorable run.
4. Pause on an uphill acceptance. Predict exp(−Δ/T) before reading the percentage.

This finite geometric cooling schedule does not guarantee an optimal tour.
The hill-climbing baseline can win individual runs. This is an educational
experiment, not an optimal TSP solver. No optimization libraries are used.

The algorithm costs O(k n) time for k proposals and n cities, computing both
candidate tour lengths each iteration. Full playback stores O(k n) trace data;
a production optimizer would usually retain far less history.
