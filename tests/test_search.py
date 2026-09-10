import math
import random
import unittest
from engine.search import Grid, search

class SearchTests(unittest.TestCase):
    def test_open(self):
        r=search(Grid(5,5),(0,0),(4,4))
        self.assertEqual(r.cost,8)
        self.assertEqual(len(r.path),9)

    def test_weighted_detour(self):
        r=search(Grid(3,2,weights={(1,0):10}),(0,0),(2,0))
        self.assertEqual(r.cost,4)
        self.assertNotIn((1,0),r.path)

    def test_unreachable(self):
        r=search(Grid(3,1,walls={(1,0)}),(0,0),(2,0))
        self.assertIsNone(r.cost)
        self.assertEqual(r.path,[])

    def test_same_endpoint(self):
        r=search(Grid(1,1),(0,0),(0,0))
        self.assertEqual(r.cost,0)
        self.assertEqual(r.path,[(0,0)])

    def test_invalid(self):
        for w in [0,-1,math.inf,math.nan]:
            with self.assertRaises(ValueError): search(Grid(2,1,weights={(1,0):w}),(0,0),(1,0))
        with self.assertRaises(ValueError): search(Grid(1,1,walls={(0,0)}),(0,0),(0,0))

    def test_seeded_maps_against_independent_relaxation(self):
        # Bellman-Ford-style relaxation is independent of the priority queue.
        rng=random.Random(26)
        for _ in range(60):
            cells=[(x,y) for y in range(6) for x in range(6)]
            walls={c for c in cells if c not in [(0,0),(5,5)] and rng.random()<.25}
            grid=Grid(6,6,walls,{c:rng.choice([.5,1,3,7]) for c in cells if c not in walls})
            d={(0,0):0}
            for _ in cells:
                changed=False
                for c in cells:
                    if c in walls: continue
                    for n in grid.neighbors(c):
                        cost=d.get(c,math.inf)+grid.weights[n]
                        if cost<d.get(n,math.inf): d[n]=cost; changed=True
                if not changed: break
            expected=d.get((5,5))
            for alg in ["astar","ucs"]:
                r=search(grid,(0,0),(5,5),alg)
                self.assertEqual(r.cost,expected)
                if r.path:
                    self.assertEqual(r.path[0],(0,0)); self.assertEqual(r.path[-1],(5,5))
                    self.assertEqual(sum(grid.weights[c] for c in r.path[1:]),r.cost)
                    for a,b in zip(r.path,r.path[1:]): self.assertIn(b,list(grid.neighbors(a)))

if __name__=="__main__": unittest.main()
