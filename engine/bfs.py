"""Breadth-first graph search with inspectable nodes and frontier snapshots."""
from collections import deque
from dataclasses import dataclass

@dataclass
class Node:
    state: str
    parent: 'Node | None' = None
    depth: int = 0

    def path(self):
        result = []
        node = self
        while node is not None:
            result.append(node.state)
            node = node.parent
        return result[::-1]


def expand(graph, node):
    """Yield one child at a time in the graph's neighbor order."""
    for state in graph[node.state]:
        yield Node(state, node, node.depth + 1)


def breadth_first(graph, start, goal):
    if start not in graph or goal not in graph:
        raise ValueError('Start and goal must be graph nodes.')
    if any(n not in graph for neighbors in graph.values() for n in neighbors):
        raise ValueError('Every edge must point to a graph node.')
    frontier = deque([Node(start)])
    seen = {start}
    parents = {start: None}
    expanded = []
    steps = [dict(current=None, queue=[start], expanded=[], parents=dict(parents),
                  added=[], depth=0, path=[], done=False)]
    while frontier:
        node = frontier.popleft()
        # Goal is tested on removal, before generating its children.
        if node.state == goal:
            steps.append(dict(current=node.state, queue=[n.state for n in frontier],
                              expanded=list(expanded), parents=dict(parents), added=[],
                              depth=node.depth, path=node.path(), done=True))
            return steps
        added = []
        for child in expand(graph, node):
            if child.state not in seen:
                seen.add(child.state)  # Mark on enqueue to avoid duplicate frontier nodes.
                parents[child.state] = node.state
                frontier.append(child)
                added.append(child.state)
        expanded.append(node.state)
        steps.append(dict(current=node.state, queue=[n.state for n in frontier],
                          expanded=list(expanded), parents=dict(parents), added=added,
                          depth=node.depth, path=[], done=not frontier))
    return steps
