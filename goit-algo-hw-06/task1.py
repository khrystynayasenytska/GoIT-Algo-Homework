
"""
Metro Transport Network Graph using NetworkX
"""

import networkx as nx
import matplotlib.pyplot as plt
# create a graph
G = nx.Graph()
# add nodes
stations = {
    'Хрещатик': {'line': 'M1', 'district': 'Центр'},
    'Майдан Незалежності': {'line': 'M1', 'district': 'Центр'},
    'Поштова площа': {'line': 'M1', 'district': 'Центр'},
    'Контрактова площа': {'line': 'M1', 'district': 'Поділ'},
    'Тарасова Шевченка': {'line': 'M1', 'district': 'Поділ'},
    'Палац Спорту': {'line': 'M2', 'district': 'Центр'},
    'Площа Льва Толстого': {'line': 'M2', 'district': 'Центр'},
    'Олімпійська': {'line': 'M2', 'district': 'Центр'},
    'Палац "Україна"': {'line': 'M2', 'district': 'Печерськ'},
    'Либідська': {'line': 'M2', 'district': 'Печерськ'},
    'Театральна': {'line': 'M3', 'district': 'Центр'},
    'Золоті ворота': {'line': 'M3', 'district': 'Центр'},
    'Палац культури': {'line': 'M3', 'district': 'Солом\'янка'},
    'Шулявська': {'line': 'M3', 'district': 'Солом\'янка'},
}

# add nodes to the graph
for station, attrs in stations.items():
    G.add_node(station, **attrs)
# 3. add edges with weights
edges = [
    # reds line (M1)
    ('Хрещатик', 'Майдан Незалежності', 2),
    ('Майдан Незалежності', 'Поштова площа', 3),
    ('Поштова площа', 'Контрактова площа', 2),
    ('Контрактова площа', 'Тарасова Шевченка', 3),

    # blue line (M2)
    ('Палац Спорту', 'Площа Льва Толстого', 2),
    ('Площа Льва Толстого', 'Олімпійська', 3),
    ('Олімпійська', 'Палац "Україна"', 2),
    ('Палац "Україна"', 'Либідська', 3),

    # green line (M3)
    ('Театральна', 'Золоті ворота', 2),
    ('Золоті ворота', 'Палац культури', 4),
    ('Палац культури', 'Шулявська', 3),

    # interchanges
    ('Хрещатик', 'Театральна', 5),
    ('Майдан Незалежності', 'Площа Льва Толстого', 4),
    ('Театральна', 'Палац Спорту', 6),
]

# add edges to the graph
for u, v, time in edges:
    G.add_edge(u, v, time=time)
# 4. analysis of the graph
print("Analysis of the Metro Transport Network Graph")

# basic characteristics
print(f"\nBasic characteristics:")
print(f"   Nodes numbers(metro stations): {G.number_of_nodes()}")
print(f"   Edges number(connections): {G.number_of_edges()}")

# dagree
degrees = dict(G.degree())
print(f"\nDegree of nodes:")
for station, degree in sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"   {station}: {degree}")

# Avg degree
avg_degree = sum(degrees.values()) / G.number_of_nodes()
print(f"\nAvg degree: {avg_degree:.2f}")

# Graph density
density = nx.density(G)
print(f"Graph density: {density:.4f}")

# diameter and radius
if nx.is_connected(G):
    diameter = nx.diameter(G)
    radius = nx.radius(G)
    print(f"Diameter: {diameter}")
    print(f"Radius: {radius}")

# centrality measures
degree_centrality = nx.degree_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)

print(f"\nTop 3 Station by Degree Centrality:")
for station, centrality in sorted(betweenness_centrality.items(), 
                                  key=lambda x: x[1], reverse=True)[:3]:
    print(f"   {station}: {centrality:.4f}")

# coefficient of clustering
clustering = nx.average_clustering(G)
print(f"\nCoefficient of clastering: {clustering:.4f}")
# 5. visualization of the graph
print(f"\nvisualization of the Metro Transport Network Graph...")

# create figure and axis
fig, ax = plt.subplots(figsize=(14, 10))

# positioning of nodes
pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

# size of nodes by degree
node_sizes = [degrees[node] * 600 for node in G.nodes()]

# color of nodes by line
line_colors = {
    'M1': '#e74c3c',  
    'M2': '#3498db',  
    'M3': '#2ecc71'   
}
node_colors = [line_colors.get(G.nodes[node].get('line'), '#95a5a6') 
               for node in G.nodes()]

# draw nodes
nx.draw_networkx_nodes(G, pos, 
                       node_size=node_sizes, 
                       node_color=node_colors,
                       alpha=0.9, 
                       edgecolors='black', 
                       linewidths=2.5,
                       ax=ax)

# draw edges
nx.draw_networkx_edges(G, pos, 
                       width=2.5, 
                       alpha=0.6, 
                       edge_color='gray',
                       ax=ax)

# define font properties for labels
nx.draw_networkx_labels(G, pos, 
                        font_size=9, 
                        font_weight='bold',
                        font_family='DejaVu Sans',
                        ax=ax)

# add edge labels (travel time)
edge_labels = nx.get_edge_attributes(G, 'time')
nx.draw_networkx_edge_labels(G, pos, 
                             edge_labels, 
                             font_size=8,
                             ax=ax)

# graph title and axis off
ax.set_title('Metro Transport Network Graph\n(node size = number of connections)', 
             fontsize=16, 
             fontweight='bold', 
             pad=20)
ax.axis('off')

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#e74c3c', edgecolor='black', label='Red Line (M1)'),
    Patch(facecolor='#3498db', edgecolor='black', label='Blue Line (M2)'),
    Patch(facecolor='#2ecc71', edgecolor='black', label='Green Line (M3)')
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=11, framealpha=0.9)

plt.tight_layout()
plt.savefig('metro_network.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Visualization saved as 'metro_network.png'")
plt.show()
# 6. ADDITIONAL ANALYSIS: SHORTEST PATHS
print(f"\nEXAMPLES OF SHORTEST PATHS:")

# Example 1
start = 'Тарасова Шевченка'
end = 'Либідська'
try:
    path = nx.shortest_path(G, start, end)
    length = nx.shortest_path_length(G, start, end)
    print(f"\n   {start} → {end}:")
    print(f"   Path: {' → '.join(path)}")
    print(f"   Number of stations: {length}")
except nx.NetworkXNoPath:
    print(f"   Path not found between {start} and {end}")

# Example 2
start = 'Шулявська'
end = 'Контрактова площа'
try:
    path = nx.shortest_path(G, start, end)
    length = nx.shortest_path_length(G, start, end)
    print(f"\n   {start} → {end}:")
    print(f"   Path: {' → '.join(path)}")
    print(f"   Number of stations: {length}")
except nx.NetworkXNoPath:
    print(f"   Path not found between {start} and {end}")

print("ANALYSIS COMPLETED!")

