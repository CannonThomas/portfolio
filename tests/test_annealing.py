import math
import unittest
from engine.annealing import acceptance_probability, solve, tour_length

class AnnealingTests(unittest.TestCase):
    def test_closed_tour(self):
        self.assertEqual(tour_length([(0,0),(1,0),(1,1),(0,1)],[0,1,2,3]),4)

    def test_acceptance(self):
        self.assertEqual(acceptance_probability(-2,0),1)
        self.assertEqual(acceptance_probability(0,0),1)
        self.assertEqual(acceptance_probability(2,0),0)
        self.assertAlmostEqual(acceptance_probability(2,2),math.exp(-1))
        self.assertGreater(acceptance_probability(2,20),acceptance_probability(2,2))

    def test_zero_temperature_matches_hill_climbing(self):
        r=solve(temperature=0,iterations=150)
        for s in r['trace']:
            self.assertAlmostEqual(s['cost'],s['hill'])
            self.assertEqual(s['uphill'],0)

    def test_trace_invariants_and_reproducibility(self):
        r=solve(iterations=200,temperature=100)
        self.assertEqual(r,solve(iterations=200,temperature=100))
        previous=r['trace'][0]
        for s in r['trace']:
            self.assertEqual(sorted(s['route']),list(range(18)))
            self.assertEqual(sorted(s['best_route']),list(range(18)))
            self.assertAlmostEqual(s['cost'],tour_length(r['points'],s['route']))
            self.assertAlmostEqual(s['best'],tour_length(r['points'],s['best_route']))
            self.assertLessEqual(s['best'],previous['best'])
            self.assertLessEqual(s['hill'],previous['hill'])
            self.assertLessEqual(s['best'],s['cost'])
            if s['step'] and not s['accepted']:self.assertEqual(s['route'],previous['route'])
            previous=s
        self.assertGreater(r['trace'][-1]['uphill'],0)

    def test_schedule_and_comparison_inputs(self):
        a=solve(iterations=20,temperature=20,cooling=.5)
        b=solve(iterations=20,temperature=0)
        self.assertEqual(a['points'],b['points'])
        self.assertEqual(a['trace'][0]['route'],b['trace'][0]['route'])
        self.assertEqual(a['trace'][2]['temperature'],10)
        self.assertEqual([s['hill'] for s in a['trace']],[s['hill'] for s in b['trace']])

    def test_validation(self):
        for kwargs in [dict(temperature=-1),dict(cooling=0),dict(iterations=5001),dict(seed=-1),dict(temperature=math.nan)]:
            with self.assertRaises(ValueError):solve(**kwargs)
