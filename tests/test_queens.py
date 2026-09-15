import unittest
from engine.queens import solve, attacking_pairs

class QueensTests(unittest.TestCase):
    def test_attacks(self):
        self.assertEqual(attacking_pairs([0,0,-1]),[(0,1)])
        self.assertEqual(attacking_pairs([0,1,-1]),[(0,1)])
        self.assertEqual(attacking_pairs([1,3,0,2]),[])

    def test_solutions_and_trace_invariants(self):
        for n in [1,4,8,10]:
            r=solve(n)
            self.assertTrue(r['solved'])
            final=r['trace'][-1]
            self.assertEqual(final['action'],'solved')
            self.assertEqual(len(set(final['board'])),n)
            self.assertNotIn(-1,final['board'])
            for event in r['trace']:
                self.assertEqual(attacking_pairs(event['board']),[])
                self.assertEqual(len(event['board']),n)
                if event['action']=='reject':
                    candidate=event['board'][:];candidate[event['row']]=event['col']
                    self.assertTrue(attacking_pairs(candidate))

    def test_impossible(self):
        for n in [2,3]:
            r=solve(n)
            self.assertFalse(r['solved'])
            self.assertEqual(r['trace'][-1]['action'],'unsolved')
            self.assertEqual(r['trace'][-1]['board'],[-1]*n)
            self.assertGreater(r['trace'][-1]['backtracks'],0)

    def test_reproducible_and_validated(self):
        self.assertEqual(solve(4),solve(4))
        for n in [0,11,4.5,True]:
            with self.assertRaises(ValueError):solve(n)
