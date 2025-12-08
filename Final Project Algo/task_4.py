import uuid
import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    """Binary tree node for heap visualization"""
    def __init__(self, key, color="skyblue"):
        self.left = None      # Left child
        self.right = None     # Right child
        self.val = key        # Node value
        self.color = color    # Node color for visualization
        self.id = str(uuid.uuid4())  # Unique identifier

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """
    Recursively add nodes and edges to the graph with proper positioning.
    Uses breadth positioning: positions nodes horizontally based on tree level.
    
    Args:
        graph: networkx graph object
        node: current tree node
        pos: dictionary of node positions
        x: horizontal position
        y: vertical position
        layer: tree depth level for positioning calculation
    """
    if node is not None:
        # Add node to graph with color and label
        graph.add_node(node.id, color=node.color, label=node.val)
        
        # Process left child
        if node.left:
            graph.add_edge(node.id, node.left.id)
            # Calculate left child position (move left)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        
        # Process right child
        if node.right:
            graph.add_edge(node.id, node.right.id)
            # Calculate right child position (move right)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    
    return graph

def draw_tree(tree_root):
    """
    Draw binary tree visualization using networkx and matplotlib.
    
    Args:
        tree_root: root node of the binary tree
    """
    # Create directed graph
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    
    # Add all edges and nodes
    tree = add_edges(tree, tree_root, pos)

    # Extract colors and labels for visualization
    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    # Create and display the plot
    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=2500, node_color=colors)
    plt.show()

def build_heap_tree(heap_array, color="lightcoral"):
    """
    Create a binary tree from a heap array (0-indexed).
    
    In a heap array representation:
    - Node at index i has:
      - Left child at index 2*i + 1
      - Right child at index 2*i + 2
    
    Args:
        heap_array: list representing a heap
        color: color for all nodes in the tree
    
    Returns:
        Root node of the constructed binary tree
    """
    # Handle empty heap
    if not heap_array:
        return None

    # Create Node objects for all elements in the heap
    nodes = [Node(key, color=color) for key in heap_array]
    
    # Build parent-child relationships according to heap structure
    n = len(heap_array)
    for i in range(n):
        left_i = 2 * i + 1      # Left child index
        right_i = 2 * i + 2     # Right child index
        
        # Link left child if it exists
        if left_i < n:
            nodes[i].left = nodes[left_i]
        
        # Link right child if it exists
        if right_i < n:
            nodes[i].right = nodes[right_i]
    
    return nodes[0]  # Return root (first element)

def draw_heap(heap_array):
    """
    Visualize a heap array as a binary tree.
    
    Args:
        heap_array: list representing a heap structure
    """
    # Convert heap array to tree structure
    root = build_heap_tree(heap_array)
    
    # Handle empty heap
    if root is None:
        print("Heap is empty")
        return
    
    # Draw the tree
    draw_tree(root)

if __name__ == "__main__":
    # Initial unsorted array
    array = [7, 1, 5, 3, 9, 11, 13]

    # Transform array into min-heap structure
    heapq.heapify(array)
    print("Min-heap:", array)

    # Visualize the heap as a binary tree
    draw_heap(array)
