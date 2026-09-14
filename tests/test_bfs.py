import unittest
from engine.bfs import Node, expand, breadth_first

class BFSTests(unittest.TestCase):
    def test_nodes_and_yield(self):
        root=Node('A')
        children=expand({'A':['B','C']},root)
        b=next(children)
        self.assertEqual(b.path(),['A','B'])
        self.assertEqual(b.depth,1)
        self.assertEqual(next(children).state,'C')
        with self.assertRaises(StopIteration):next(children)

    def test_cycle_and_shortest_path(self):
        g={'A':['B','C'],'B':['A','D'],'C':['A','D'],'D':['B','C']}
        steps=breadth_first(g,'A','D')
        self.assertEqual(steps[-1]['path'],['A','B','D'])
        self.assertEqual(steps[-1]['expanded'],['A','B','C'])
        self.assertEqual(steps[1]['queue'],['B','C'])
        for step in steps:self.assertEqual(len(step['queue']),len(set(step['queue'])))

    def test_unreachable(self):
        steps=breadth_first({'A':['B'],'B':['A'],'C':[]},'A','C')
        self.assertTrue(steps[-1]['done'])
        self.assertEqual(steps[-1]['path'],[])
        self.assertEqual(steps[-1]['queue'],[])

    def test_start_goal(self):
        s=breadth_first({'A':[]},'A','A')[-1]
        self.assertEqual(s['path'],['A'])
        self.assertEqual(s['expanded'],[])

    def test_bad_edge(self):
        with self.assertRaises(ValueError):breadth_first({'A':['B']},'A','A')
