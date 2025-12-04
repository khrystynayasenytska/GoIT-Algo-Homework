"""
Description:
The program implements Depth-First Search (DFS) and Breadth-First Search (BFS) algorithms
for finding paths in the metro transport network graph.
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import deque
import pandas as pd

# 1. CREATING THE METRO TRANSPORT NETWORK GRAPH

def create_metro_graph():
    """Creates a graph of the Kyiv metro transport network"""
    G = nx.Graph()

    # Adding stations (nodes)
    stations = {
        'Хрещатик': {'line': 'M1', 'district': 'Center'},
        'Майдан Незалежності': {'line': 'M1', 'district': 'Center'},
        'Поштова площа': {'line': 'M1', 'district': 'Center'},
        'Контрактова площа': {'line': 'M1', 'district': 'Podil'},
        'Тарасова Шевченка': {'line': 'M1', 'district': 'Podil'},
        'Палац Спорту': {'line': 'M2', 'district': 'Center'},
        'Площа Льва Толстого': {'line': 'M2', 'district': 'Center'},
        'Олімпійська': {'line': 'M2', 'district': 'Center'},
        'Палац "Україна"': {'line': 'M2', 'district': 'Pechersk'},
        'Либідська': {'line': 'M2', 'district': 'Pechersk'},
        'Театральна': {'line': 'M3', 'district': 'Center'},
        'Золоті ворота': {'line': 'M3', 'district': 'Center'},
        'Палац культури': {'line': 'M3', 'district': 'Solomianka'},
        'Шулявська': {'line': 'M3', 'district': 'Solomianka'},
    }

    for station, attrs in stations.items():
        G.add_node(station, **attrs)

    # Adding connections (edges)
    edges = [
        # Red line (M1)
        ('Хрещатик', 'Майдан Незалежності', 2),
        ('Майдан Незалежності', 'Поштова площа', 3),
        ('Поштова площа', 'Контрактова площа', 2),
        ('Контрактова площа', 'Тарасова Шевченка', 3),
        # Blue line (M2)
        ('Палац Спорту', 'Площа Льва Толстого', 2),
        ('Площа Льва Толстого', 'Олімпійська', 3),
        ('Олімпійська', 'Палац "Україна"', 2),
        ('Палац "Україна"', 'Либідська', 3),
        # Green line (M3)
        ('Театральна', 'Золоті ворота', 2),
        ('Золоті ворота', 'Палац культури', 4),
        ('Палац культури', 'Шулявська', 3),
        # Interchanges between lines
        ('Хрещатик', 'Театральна', 5),
        ('Майдан Незалежності', 'Площа Льва Толстого', 4),
        ('Театральна', 'Палац Спорту', 6),
    ]

    for u, v, time in edges:
        G.add_edge(u, v, time=time)

    return G

# 2. IMPLEMENTATION OF THE DFS ALGORITHM (DEPTH-FIRST SEARCH)

def dfs_path(graph, start, goal):
    """
    Finding a path using the DFS algorithm (Depth-First Search)

    Parameters:
        graph: NetworkX graph
        start: starting node
        goal: target node

    Returns:
        tuple: (found path, order of visited nodes)
    """
    visited = set()
    stack = [[start]]  # Stack of paths (LIFO - Last In, First Out)
    visited_order = []  # Order of visited nodes

    while stack:
        path = stack.pop()  # Take the last added path
        node = path[-1]

        if node not in visited:
            visited.add(node)
            visited_order.append(node)

            # If we found the target node
            if node == goal:
                return path, visited_order

            # Add neighbors to the stack (in reverse order)
            neighbors = sorted(list(graph.neighbors(node)), reverse=True)
            for neighbor in neighbors:
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    stack.append(new_path)

    return None, visited_order

# 3. IMPLEMENTATION OF THE BFS ALGORITHM (BREADTH-FIRST SEARCH)

def bfs_path(graph, start, goal):
    """
    Finding a path using the BFS algorithm (Breadth-First Search)

    Parameters:
        graph: NetworkX graph
        start: starting node
        goal: target node

    Returns:
        tuple: (found path, order of visited nodes)
    """
    visited = set([start])
    queue = deque([[start]])  # Queue of paths (FIFO - First In, First Out)
    visited_order = [start]  # Order of visited nodes

    while queue:
        path = queue.popleft()  # Take the first added path
        node = path[-1]

        # If we found the target node
        if node == goal:
            return path, visited_order

        # Add neighbors to the queue
        neighbors = sorted(list(graph.neighbors(node)))
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                visited_order.append(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None, visited_order

# 4. FUNCTION FOR COMPARING RESULTS

def compare_algorithms(graph, start, goal):
    """
    Compares the results of DFS and BFS algorithms

    Parameters:
        graph: NetworkX graph
        start: starting node
        goal: target node

    Returns:
        dict: results of both algorithms
    """
    # Run DFS
    dfs_result, dfs_visited = dfs_path(graph, start, goal)

    # Run BFS
    bfs_result, bfs_visited = bfs_path(graph, start, goal)

    return {
        'start': start,
        'goal': goal,
        'dfs_path': dfs_result,
        'bfs_path': bfs_result,
        'dfs_length': len(dfs_result) - 1 if dfs_result else 0,
        'bfs_length': len(bfs_result) - 1 if bfs_result else 0,
        'dfs_visited': len(dfs_visited),
        'bfs_visited': len(bfs_visited)
    }

# 5. VISUALIZATION OF RESULTS

def visualize_comparison(graph, start, goal, dfs_path_result, bfs_path_result):
    """Creates visualization of DFS and BFS comparison"""

    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    pos = nx.spring_layout(graph, k=2, iterations=50, seed=42)

    # Visualization of DFS
    ax1 = axes[0]
    node_colors_dfs = []
    for node in graph.nodes():
        if node == start:
            node_colors_dfs.append('#FFD700')
        elif node == goal:
            node_colors_dfs.append('#FF1493')
        elif node in dfs_path_result:
            node_colors_dfs.append('#90EE90')
        else:
            node_colors_dfs.append('#D3D3D3')

    nx.draw_networkx_nodes(graph, pos, node_color=node_colors_dfs, 
                           node_size=800, alpha=0.9, ax=ax1,
                           edgecolors='black', linewidths=2)
    nx.draw_networkx_edges(graph, pos, width=1.5, alpha=0.3, 
                           edge_color='gray', ax=ax1)

    path_edges_dfs = [(dfs_path_result[i], dfs_path_result[i+1]) 
                      for i in range(len(dfs_path_result)-1)]
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges_dfs, 
                           width=3.5, alpha=0.8, edge_color='#32CD32', ax=ax1)
    nx.draw_networkx_labels(graph, pos, font_size=8, font_weight='bold', ax=ax1)

    ax1.set_title(f'DFS: {start} → {goal}\nLength: {len(dfs_path_result)-1} edges', 
                  fontsize=13, fontweight='bold')
    ax1.axis('off')

    # Visualization of BFS
    ax2 = axes[1]
    node_colors_bfs = []
    for node in graph.nodes():
        if node == start:
            node_colors_bfs.append('#FFD700')
        elif node == goal:
            node_colors_bfs.append('#FF1493')
        elif node in bfs_path_result:
            node_colors_bfs.append('#87CEEB')
        else:
            node_colors_bfs.append('#D3D3D3')

    nx.draw_networkx_nodes(graph, pos, node_color=node_colors_bfs, 
                           node_size=800, alpha=0.9, ax=ax2,
                           edgecolors='black', linewidths=2)
    nx.draw_networkx_edges(graph, pos, width=1.5, alpha=0.3, 
                           edge_color='gray', ax=ax2)

    path_edges_bfs = [(bfs_path_result[i], bfs_path_result[i+1]) 
                      for i in range(len(bfs_path_result)-1)]
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges_bfs, 
                           width=3.5, alpha=0.8, edge_color='#1E90FF', ax=ax2)
    nx.draw_networkx_labels(graph, pos, font_size=8, font_weight='bold', ax=ax2)

    ax2.set_title(f'BFS: {start} → {goal}\nLength: {len(bfs_path_result)-1} edges', 
                  fontsize=13, fontweight='bold')
    ax2.axis('off')

    plt.tight_layout()
    plt.savefig('task2_dfs_bfs_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

# 6. MAIN FUNCTION

def main():
    """Main function of the program"""

    print("TASK 2: COMPARISON OF DFS AND BFS ALGORITHMS")

    # Create a graph
    G = create_metro_graph()
    print(f"\nGraph created: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    # Test cases
    test_cases = [
        ('Тарасова Шевченка', 'Либідська'),
        ('Шулявська', 'Контрактова площа'),
        ('Хрещатик', 'Палац "Україна"'),
        ('Золоті ворота', 'Поштова площа'),
    ]

    results = []

    # Testing algorithms
    for i, (start, goal) in enumerate(test_cases, 1):
        print(f"TEST {i}: {start} → {goal}")

        result = compare_algorithms(G, start, goal)
        results.append(result)

        # Print results
        print(f"\nDFS:")
        print(f"  Path: {' → '.join(result['dfs_path'])}")
        print(f"  Length: {result['dfs_length']} edges")
        print(f"  Visited nodes: {result['dfs_visited']}")

        print(f"\nBFS:")
        print(f"  Path: {' → '.join(result['bfs_path'])}")
        print(f"  Length: {result['bfs_length']} edges")
        print(f"  Visited nodes: {result['bfs_visited']}")

        print(f"\nComparison:")
        if result['bfs_length'] < result['dfs_length']:
            print(f"BFS found a shorter path ({result['bfs_length']} vs {result['dfs_length']})")
        elif result['dfs_length'] < result['bfs_length']:
            print(f"DFS found a shorter path ({result['dfs_length']} vs {result['bfs_length']})")
        else:
            print(f"Both algorithms found paths of equal length ({result['dfs_length']})")

    # Create visualization for the most instructive example
    print("Creating visualization...")
    visualize_comparison(G, test_cases[1][0], test_cases[1][1],
                        results[1]['dfs_path'], results[1]['bfs_path'])
    print("Visualization saved")

    # Save results to CSV
    df = pd.DataFrame(results)
    df.to_csv('task2_results.csv', index=False, encoding='utf-8-sig')
    print("Results saved: task2_results.csv")

    # Statistics
    print("STATISTICS:")
    bfs_better = sum(1 for r in results if r['bfs_length'] < r['dfs_length'])
    same = sum(1 for r in results if r['bfs_length'] == r['dfs_length'])
    print(f" BFS found a shorter path: {bfs_better}/{len(results)} tests")
    print(f" Equal path lengths: {same}/{len(results)} tests")
    print(f" Average number of visited nodes:")
    print(f"  - DFS: {sum(r['dfs_visited'] for r in results) / len(results):.1f}")
    print(f"  - BFS: {sum(r['bfs_visited'] for r in results) / len(results):.1f}")
    print(f"\nProgram completed successfully!")

# PROGRAM EXECUTION
if __name__ == "__main__":
    main()
