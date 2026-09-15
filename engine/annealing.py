"""Seeded simulated annealing and a hill-climbing baseline for a closed city tour."""
import math
import random


def tour_length(points, route):
    """Euclidean distance, including the return to the starting city."""
    return sum(math.dist(points[a], points[b])
               for a, b in zip(route, route[1:] + route[:1]))


def acceptance_probability(delta, temperature):
    """For minimization: accept improvements; sometimes accept uphill moves."""
    if not math.isfinite(delta) or not math.isfinite(temperature) or temperature < 0:
        raise ValueError('Use finite costs and a nonnegative temperature.')
    if delta <= 0:
        return 1.0
    return math.exp(-delta / temperature) if temperature > 0 else 0.0


def solve(seed=26, temperature=20.0, cooling=0.995, iterations=1200, city_count=18):
    if not isinstance(seed, int) or isinstance(seed, bool) or not 0 <= seed <= 99999:
        raise ValueError('Seed must be an integer between 0 and 99999.')
    if not isinstance(iterations, int) or not 1 <= iterations <= 5000:
        raise ValueError('Use 1 to 5000 iterations.')
    if not isinstance(city_count, int) or not 4 <= city_count <= 30:
        raise ValueError('Use 4 to 30 cities.')
    if not math.isfinite(temperature) or not 0 <= temperature <= 100:
        raise ValueError('Temperature must be between 0 and 100.')
    if not math.isfinite(cooling) or not 0 < cooling <= 1:
        raise ValueError('Cooling must be greater than 0 and at most 1.')
    # Separate RNGs keep city generation and proposal order stable across settings.
    setup = random.Random(seed)
    proposal_rng = random.Random(seed + 1)
    acceptance_rng = random.Random(seed + 2)
    points = [(setup.uniform(8, 92), setup.uniform(8, 92)) for _ in range(city_count)]
    route = list(range(city_count))
    setup.shuffle(route)
    best = route[:]
    hill = route[:]
    cost = best_cost = hill_cost = tour_length(points, route)
    uphill_accepted = 0
    trace = [dict(step=0, route=route[:], best_route=best[:], cost=cost,
                  best=best_cost, hill=hill_cost, temperature=temperature,
                  delta=0.0, probability=1.0, accepted=True, uphill=0)]
    for step in range(1, iterations + 1):
        # Reversing a segment is a 2-opt move; city zero in the tour stays anchored.
        i, j = sorted(proposal_rng.sample(range(1, city_count), 2))
        candidate = route[:i] + route[i:j+1][::-1] + route[j+1:]
        candidate_cost = tour_length(points, candidate)
        delta = candidate_cost - cost
        probability = acceptance_probability(delta, temperature)
        accepted = acceptance_rng.random() < probability
        if accepted:
            route, cost = candidate, candidate_cost
            if delta > 0:
                uphill_accepted += 1
            if cost < best_cost:
                best, best_cost = route[:], cost
        # Same initial tour, same segment-index proposals, same iteration budget.
        hill_candidate = hill[:i] + hill[i:j+1][::-1] + hill[j+1:]
        hill_candidate_cost = tour_length(points, hill_candidate)
        if hill_candidate_cost <= hill_cost:
            hill, hill_cost = hill_candidate, hill_candidate_cost
        trace.append(dict(step=step, route=route[:], best_route=best[:], cost=cost,
                          best=best_cost, hill=hill_cost, temperature=temperature,
                          delta=delta, probability=probability, accepted=accepted,
                          uphill=uphill_accepted))
        temperature *= cooling
    return dict(points=points, initial=trace[0]['cost'], trace=trace,
                hill_route=hill, seed=seed, iterations=iterations)
