"""
Description:
The program implements Dijkstra's algorithm for finding shortest paths
between all nodes of a weighted graph of the metro transport network.
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from collections import deque

# 1. CREATING A WEIGHTED METRO TRANSPORT NETWORK GRAPH

def create_weighted_metro_graph():
    """
    Creates a weighted graph of the Kyiv metro transport network

    Returns:
        G: NetworkX graph with weights on edges (travel time in minutes)
    """
    G = nx.Graph()

    # Adding stations (nodes) with attributes
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

    # Adding edges with weights (travel time in minutes)
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

    for u, v, weight in edges:
        G.add_edge(u, v, weight=weight)

    return G

# 2. FINDING SHORTEST PATHS USING DIJKSTRA'S ALGORITHM

def find_all_shortest_paths(graph):
    """
    Finds the shortest paths between all pairs of nodes
    using Dijkstra's algorithm

    Parameters:
        graph: weighted NetworkX graph

    Returns:
        tuple: (dictionary of paths, dictionary of lengths)
    """
    nodes = list(graph.nodes())
    all_paths = {}
    all_lengths = {}

    for source in nodes:
        # Using built-in Dijkstra's algorithm from NetworkX
        paths = nx.single_source_dijkstra_path(graph, source, weight='weight')
        lengths = nx.single_source_dijkstra_path_length(graph, source, weight='weight')

        all_paths[source] = paths
        all_lengths[source] = lengths

    return all_paths, all_lengths


def display_shortest_path(graph, source, target, all_paths, all_lengths):
    """
    Displays detailed information about the shortest path

    Parameters:
        graph: NetworkX graph
        source: starting node
        target: target node
        all_paths: dictionary with paths
        all_lengths: dictionary with lengths
    """
    path = all_paths[source][target]
    length = all_lengths[source][target]

    print(f"ROUTE: {source} → {target}")
    print(f"\nShortest path (Dijkstra's algorithm):")
    print(f"   {' → '.join(path)}")
    print(f"\nCharacteristics:")
    print(f"  Number of stations: {len(path)}")
    print(f"  Number of transfers: {len(path) - 1}")
    print(f"  Total time: {length} minutes")

    # Route details by segments
    print(f"\nRoute details:")
    total_time = 0
    for i in range(len(path) - 1):
        segment_weight = graph[path[i]][path[i+1]]['weight']
        total_time += segment_weight
        print(f"   {i+1}. {path[i]} → {path[i+1]}: {segment_weight} min (cumulative: {total_time} min)")

# 3. CREATING A DISTANCE MATRIX

def create_distance_matrix(graph, all_lengths):
    """
    Creates a matrix of shortest distances between all nodes

    Parameters:
        graph: NetworkX graph
        all_lengths: dictionary with path lengths

    Returns:
        DataFrame: distance matrix
    """
    nodes = list(graph.nodes())
    distance_matrix = pd.DataFrame(index=nodes, columns=nodes, dtype=float)

    for source in nodes:
        for target in nodes:
            if source == target:
                distance_matrix.loc[source, target] = 0
            else:
                distance_matrix.loc[source, target] = all_lengths[source][target]

    return distance_matrix

# 4. STATISTICAL ANALYSIS

def analyze_shortest_paths(graph, all_paths, all_lengths):
    """
    Performs statistical analysis of shortest paths

    Parameters:
        graph: NetworkX graph
        all_paths: dictionary with paths
        all_lengths: dictionary with lengths

    Returns:
        dict: statistical indicators
    """
    nodes = list(graph.nodes())

    # Find extreme routes
    max_distance = 0
    min_distance = float('inf')
    max_route = None
    min_route = None

    for source in nodes:
        for target in nodes:
            if source != target:
                dist = all_lengths[source][target]
                if dist > max_distance:
                    max_distance = dist
                    max_route = (source, target)
                if dist < min_distance:
                    min_distance = dist
                    min_route = (source, target)

    # Calculate statistics
    all_distances = []
    for source in nodes:
        for target in nodes:
            if source != target:
                all_distances.append(all_lengths[source][target])

    # Most accessible stations
    accessibility = {}
    for node in nodes:
        avg_time = np.mean([all_lengths[node][target] for target in nodes if target != node])
        accessibility[node] = avg_time

    return {
        'max_route': max_route,
        'max_distance': max_distance,
        'min_route': min_route,
        'min_distance': min_distance,
        'avg_distance': np.mean(all_distances),
        'median_distance': np.median(all_distances),
        'std_distance': np.std(all_distances),
        'accessibility': accessibility
    }


def print_statistics(stats, all_paths):
    """Prints statistics"""
    print("STATISTICAL ANALYSIS")

    print(f"\n Longest route:")
    print(f"   {stats['max_route'][0]} → {stats['max_route'][1]}")
    print(f"   Time: {stats['max_distance']} minutes")
    print(f"   Path: {' → '.join(all_paths[stats['max_route'][0]][stats['max_route'][1]])}")

    print(f"\n Shortest route:")
    print(f"   {stats['min_route'][0]} → {stats['min_route'][1]}")
    print(f"   Time: {stats['min_distance']} minutes")

    print(f"\n Distance statistics:")
    print(f"    Average time: {stats['avg_distance']:.2f} minutes")
    print(f"    Median: {stats['median_distance']:.2f} minutes")
    print(f"    Standard deviation: {stats['std_distance']:.2f} minutes")
    print(f"    Minimum: {stats['min_distance']} minutes")
    print(f"    Maximum: {stats['max_distance']} minutes")

    print(f"\n Most accessible stations (top-5):")
    sorted_accessibility = sorted(stats['accessibility'].items(), key=lambda x: x[1])
    for i, (station, avg_time) in enumerate(sorted_accessibility[:5], 1):
        print(f"   {i}. {station}: {avg_time:.2f} min")

# 5. COMPARISON WITH BFS

def bfs_path(graph, start, goal):
    """Finding a path using BFS (for comparison)"""
    visited = set([start])
    queue = deque([[start]])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path

        neighbors = sorted(list(graph.neighbors(node)))
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None


def compare_dijkstra_bfs(graph, source, target, all_paths, all_lengths):
    """
    Compares the results of Dijkstra and BFS

    Returns:
        dict: comparison results
    """
    # Dijkstra
    dijkstra_path = all_paths[source][target]
    dijkstra_length = all_lengths[source][target]

    # BFS
    bfs_result = bfs_path(graph, source, target)
    bfs_time = sum(graph[bfs_result[i]][bfs_result[i+1]]['weight'] 
                   for i in range(len(bfs_result) - 1))

    return {
        'dijkstra_path': dijkstra_path,
        'dijkstra_time': dijkstra_length,
        'dijkstra_hops': len(dijkstra_path) - 1,
        'bfs_path': bfs_result,
        'bfs_time': bfs_time,
        'bfs_hops': len(bfs_result) - 1,
        'time_saved': bfs_time - dijkstra_length
    }

# 6. VISUALIZATION

def visualize_shortest_path(graph, source, target, path, length, distance_matrix):
    """
    Creates visualization of the shortest path and distance matrix

    Parameters:
        graph: NetworkX graph
        source: starting node
        target: target node
        path: shortest path
        length: path length
        distance_matrix: distance matrix
    """
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))

    # Node positions
    pos = nx.spring_layout(graph, k=2, iterations=50, seed=42)

    # Visualization 1: Graph with shortest path
    ax1 = axes[0]

    # Node colors
    node_colors = []
    for node in graph.nodes():
        if node == source:
            node_colors.append('#FFD700')  # Gold
        elif node == target:
            node_colors.append('#FF1493')  # Pink
        elif node in path:
            node_colors.append('#87CEEB')  # Sky blue
        else:
            node_colors.append('#D3D3D3')  # Gray

    node_sizes = [1000 if node in [source, target] else 700 for node in graph.nodes()]

    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, 
                           node_size=node_sizes, alpha=0.9, ax=ax1,
                           edgecolors='black', linewidths=2.5)

    # Draw all edges
    nx.draw_networkx_edges(graph, pos, width=1.5, alpha=0.3, 
                           edge_color='gray', ax=ax1)

    # Highlight path edges
    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges, 
                           width=4, alpha=0.9, edge_color='#1E90FF', ax=ax1)

    # Labels
    nx.draw_networkx_labels(graph, pos, font_size=8, font_weight='bold', ax=ax1)

    # Edge weights
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels, font_size=7, ax=ax1)

    ax1.set_title(f'Shortest Path (Dijkstra)\n{source} → {target}\nTime: {length} min', 
                  fontsize=13, fontweight='bold', pad=15)
    ax1.axis('off')

    # Legend
    legend_elements = [
        mpatches.Patch(color='#FFD700', label='Starting station'),
        mpatches.Patch(color='#FF1493', label='Target station'),
        mpatches.Patch(color='#87CEEB', label='Stations on path'),
        mpatches.Patch(color='#1E90FF', label='Shortest path'),
    ]
    ax1.legend(handles=legend_elements, loc='upper left', fontsize=9)

    # Visualization 2: Distance matrix (heatmap)
    ax2 = axes[1]

    # Select subset of stations
    selected_stations = [
        'Хрещатик', 'Майдан Незалежності', 'Театральна', 
        'Площа Льва Толстого', 'Палац Спорту',
        'Контрактова площа', 'Золоті ворота', 'Либідська'
    ]

    subset_matrix = distance_matrix.loc[selected_stations, selected_stations]

    im = ax2.imshow(subset_matrix.astype(float), cmap='YlOrRd', aspect='auto')

    # Configure axes
    ax2.set_xticks(range(len(selected_stations)))
    ax2.set_yticks(range(len(selected_stations)))
    ax2.set_xticklabels(selected_stations, rotation=45, ha='right', fontsize=8)
    ax2.set_yticklabels(selected_stations, fontsize=8)

    # Values in cells
    for i in range(len(selected_stations)):
        for j in range(len(selected_stations)):
            ax2.text(j, i, int(subset_matrix.iloc[i, j]),
                    ha="center", va="center", color="black", fontsize=8)

    ax2.set_title('Distance Matrix of Shortest Paths\n(time in minutes)', 
                  fontsize=13, fontweight='bold', pad=15)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
    cbar.set_label('Time (minutes)', rotation=270, labelpad=20)

    plt.tight_layout()
    plt.savefig('task3_dijkstra_result.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

# 7. MAIN FUNCTION
def main():
    """Main function of the program"""

    print("TASK 3: DIJKSTRA'S ALGORITHM")

    # Create a graph
    print("\n Creating a weighted graph...")
    G = create_weighted_metro_graph()
    print(f" Graph created:")
    print(f"   Nodes: {G.number_of_nodes()}")
    print(f"   Edges: {G.number_of_edges()}")
    print(f"   Graph has weights: YES (travel time)")

    # Find all shortest paths
    print("\nComputing shortest paths using Dijkstra's algorithm...")
    all_paths, all_lengths = find_all_shortest_paths(G)
    total_pairs = len(list(G.nodes())) * (len(list(G.nodes())) - 1) // 2
    print(f" Found shortest paths for {total_pairs} pairs of nodes")

    # Demonstration on examples
    print("EXAMPLES OF SHORTEST PATHS")

    example_routes = [
        ('Тарасова Шевченка', 'Либідська'),
        ('Шулявська', 'Контрактова площа'),
        ('Хрещатик', 'Палац "Україна"'),
    ]

    for source, target in example_routes:
        display_shortest_path(G, source, target, all_paths, all_lengths)

    # Create distance matrix
    print("DISTANCE MATRIX")
    distance_matrix = create_distance_matrix(G, all_lengths)
    print("\n 14×14 matrix created")
    distance_matrix.to_csv('task3_distance_matrix.csv', encoding='utf-8-sig')
    print(" Saved: task3_distance_matrix.csv")

    # Statistical analysis
    stats = analyze_shortest_paths(G, all_paths, all_lengths)
    print_statistics(stats, all_paths)

    # Comparison with BFS
    print("COMPARISON: DIJKSTRA vs BFS")

    comparison_results = []
    for source, target in example_routes[:2]:
        result = compare_dijkstra_bfs(G, source, target, all_paths, all_lengths)
        print(f"\nRoute: {source} → {target}")
        print(f"  BFS: {len(result['bfs_path'])} stations, {result['bfs_time']} min")
        print(f"  Dijkstra: {len(result['dijkstra_path'])} stations, {result['dijkstra_time']} min")
        print(f"  Time saved: {result['time_saved']} min")

        comparison_results.append({
            'Route': f"{source} → {target}",
            'BFS: time': result['bfs_time'],
            'Dijkstra: time': result['dijkstra_time'],
            'Savings': result['time_saved']
        })

    df_comparison = pd.DataFrame(comparison_results)
    df_comparison.to_csv('task3_comparison.csv', index=False, encoding='utf-8-sig')
    print("\n Saved: task3_comparison.csv")

    # Visualization
    print("\n Creating visualization...")
    vis_source = 'Тарасова Шевченка'
    vis_target = 'Шулявська'
    visualize_shortest_path(G, vis_source, vis_target,
                           all_paths[vis_source][vis_target],
                           all_lengths[vis_source][vis_target],
                           distance_matrix)
    print(" Saved: task3_dijkstra_result.png")

    print(" PROGRAM COMPLETED SUCCESSFULLY!")
    print("\nCreated files:")
    print("   task3_distance_matrix.csv - distance matrix")
    print("   task3_comparison.csv - comparison with BFS")
    print("   task3_dijkstra_result.png - visualization")

# PROGRAM EXECUTION

if __name__ == "__main__":
    main()
