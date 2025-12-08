"""
Task 3: Dijkstra's Algorithm using binary heap (heapq).

– A weighted graph is created (adjacency list).
– Binary heap (min-heap) is used to select vertices.
– Shortest paths from start vertex to all others are computed.
"""

import heapq

class Graph:
    def __init__(self):
        # adjacency_list[u] = list of (v, weight)
        self.adjacency_list = {}

    def add_edge(self, u, v, w, undirected=True):
        """Add edge u -> v with weight w. If undirected=True, also adds v -> u."""
        self.adjacency_list.setdefault(u, []).append((v, w))
        if undirected:
            self.adjacency_list.setdefault(v, []).append((u, w))
        else:
            self.adjacency_list.setdefault(v, [])

    def vertices(self):
        return list(self.adjacency_list.keys())

def dijkstra_heap(graph: Graph, start):
    """
    Dijkstra's algorithm using binary heap (min-heap).

    Args:
        graph: Graph object with adjacency list
        start: starting vertex

    Returns:
        dist: dict {vertex: shortest distance from start}
        prev: dict {vertex: predecessor in shortest path}
    """
    # 1. Initialize distances
    dist = {v: float('inf') for v in graph.vertices()}
    dist[start] = 0
    prev = {v: None for v in graph.vertices()}

    # 2. Min-heap with tuples (distance, vertex)
    heap = [(0, start)]  # start with start vertex

    # 3. Main loop
    while heap:
        current_dist, u = heapq.heappop(heap)

        # Lazy deletion: if heap contains outdated record – skip it
        if current_dist > dist[u]:
            continue

        # For each neighbor update distance
        for v, weight in graph.adjacency_list[u]:
            distance_through_u = current_dist + weight
            if distance_through_u < dist[v]:
                dist[v] = distance_through_u
                prev[v] = u
                # Add new record to heap (update priority by re-adding)
                heapq.heappush(heap, (distance_through_u, v))

    return dist, prev

def reconstruct_path(prev, start, target):
    """Reconstruct shortest path from prev dictionary."""
    if prev[target] is None and start != target:
        return None  # no path exists
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    return list(reversed(path))

def build_sample_graph():
    """
    Create a weighted graph example for demonstration:
    
         10      15
        A -------- B ------- C
        |  \       |  \    / |
        5   7     12  8   4  2
        |    \     |  \  /  |
        D ----- E ----- F --- G
         \ 3  /  \ 6 /  \ 1 /
          \   /    \   /   /
           \ /      \ /   /
            H ------ I -- J
               9      5
    
    Vertices: A, B, C, D, E, F, G, H, I, J
    """
    g = Graph()
    
    # Top row connections
    g.add_edge("A", "B", 10)
    g.add_edge("B", "C", 15)
    
    # Middle row connections
    g.add_edge("A", "D", 5)
    g.add_edge("A", "E", 7)
    g.add_edge("B", "E", 12)
    g.add_edge("B", "F", 8)
    g.add_edge("C", "F", 4)
    g.add_edge("C", "G", 2)
    
    # Bottom row connections
    g.add_edge("D", "H", 3)
    g.add_edge("E", "F", 6)
    g.add_edge("E", "H", 9)
    g.add_edge("F", "G", 1)
    g.add_edge("F", "I", 11)
    g.add_edge("G", "J", 7)
    g.add_edge("H", "I", 9)
    g.add_edge("I", "J", 5)
    
    return g

def main():
    """Main function to demonstrate Dijkstra's algorithm"""
    # Create graph
    graph = build_sample_graph()
    start = "A"

    # Run Dijkstra's algorithm
    dist, prev = dijkstra_heap(graph, start)

    print("Shortest distances from vertex", start)
    for v in sorted(graph.vertices()):
        print(f"  {start} -> {v}: {dist[v]}")

    print("\nShortest paths:")
    for v in sorted(graph.vertices()):
        path = reconstruct_path(prev, start, v)
        if path is None:
            print(f"  Path {start} -> {v} does not exist")
        else:
            print(f"  {start} -> {v}: {' -> '.join(path)} (length {dist[v]})")

if __name__ == "__main__":
    main()
