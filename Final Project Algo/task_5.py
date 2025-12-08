import uuid
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
from collections import deque

class Node:
    """
    Binary tree node for heap representation.
    
    Each node contains a value and can have left and right child nodes.
    Each node gets a unique identifier for graph visualization purposes.
    
    Attributes:
        left: Reference to the left child node
        right: Reference to the right child node
        val: The value stored in the node
        color: The color of the node for visualization (default: dark blue)
        id: Unique identifier for the node (UUID format)
    """
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key
        self.color = "#0D47A1"  # default color - dark blue
        self.id = str(uuid.uuid4())  # unique identifier for graph visualization

def build_heap_tree(heap_array):
    """
    Build a binary tree from a heap array.
    
    Converts a flat array representation of a min-heap into a tree structure
    where each element maintains the proper parent-child relationships:
    - Left child of node at index i is at index 2*i + 1
    - Right child of node at index i is at index 2*i + 2
    
    This function creates Node objects and links them hierarchically to form
    a complete binary tree matching the heap structure.
    
    Args:
        heap_array: List of integers representing a min-heap (or any binary tree array)
    
    Returns:
        Node: The root node of the constructed binary tree, or None if array is empty
    """
    if not heap_array:
        return None
    # Create a node for each element in the heap array
    nodes = [Node(k) for k in heap_array]
    n = len(heap_array)
    # Link nodes based on heap array index relationships
    for i in range(n):
        left_idx = 2*i + 1  # calculate left child index
        right_idx = 2*i + 2  # calculate right child index
        if left_idx < n:
            nodes[i].left = nodes[left_idx]  # attach left child
        if right_idx < n:
            nodes[i].right = nodes[right_idx]  # attach right child
    return nodes[0]  # return root node

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """
    Recursively add nodes and edges to a directed graph with hierarchical positioning.
    
    This function traverses the binary tree and builds a NetworkX graph representation
    with proper hierarchical layout suitable for visualization:
    - Root node is centered at (0, 0)
    - Each layer down decreases y coordinate by 1 (moving downward)
    - Left/right children are positioned symmetrically based on their layer depth
    
    The horizontal position calculation uses: x ± 1/2^layer
    This ensures that nodes at deeper layers are positioned closer to their parents.
    
    Args:
        graph: NetworkX DiGraph object to add nodes and edges to
        node: Current node being processed in the tree
        pos: Dictionary mapping node IDs to (x, y) positions for visualization
        x: Current x-coordinate position (default: 0)
        y: Current y-coordinate position (default: 0, moves negative as we go down)
        layer: Current depth level in the tree (default: 1, increases with depth)
    
    Returns:
        DiGraph: The updated graph with all nodes and edges added
    """
    if node:
        # Add current node to graph with its value and color
        graph.add_node(node.id, label=node.val, color=node.color)
        
        # Process left child: position it to the left and one layer down
        if node.left:
            graph.add_edge(node.id, node.left.id)  # create parent-child edge
            l = x - 1/2**layer  # calculate left child x-position
            pos[node.left.id] = (l, y-1)  # store position for left child
            # recursively process left subtree with updated coordinates
            add_edges(graph, node.left, pos, x=l, y=y-1, layer=layer+1)
        
        # Process right child: position it to the right and one layer down
        if node.right:
            graph.add_edge(node.id, node.right.id)  # create parent-child edge
            r = x + 1/2**layer  # calculate right child x-position
            pos[node.right.id] = (r, y-1)  # store position for right child
            # recursively process right subtree with updated coordinates
            add_edges(graph, node.right, pos, x=r, y=y-1, layer=layer+1)
    return graph  # return the built graph

def generate_colors(n, start="#0D47A1", end="#BBDEFB"):
    """
    Generate a smooth gradient of colors from start to end color.
    
    Creates a list of n colors that transition smoothly from the start color
    (dark blue by default) to the end color (light blue by default). This is useful
    for visualizing traversal order - early nodes get darker colors, later nodes 
    get lighter colors.
    
    The function interpolates RGB values linearly across the range. For example,
    with n=5, it generates 5 colors evenly distributed from start to end.
    
    Args:
        n: Number of colors to generate
        start: Starting color in hex format (default: "#0D47A1" - dark blue)
        end: Ending color in hex format (default: "#BBDEFB" - light blue)
    
    Returns:
        list: List of n color strings in hex format (e.g., ["#0D47A1", "#1A5AC8", ...])
    """
    # Extract RGB components from hex color codes
    start_rgb = tuple(int(start[i:i+2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(end[i:i+2], 16) for i in (1, 3, 5))
    
    colors = []
    for i in range(n):
        # Calculate interpolation factor t (0 to 1)
        t = i/(n-1) if n > 1 else 0  # t=0 at start, t=1 at end
        
        # Interpolate each RGB component separately
        rgb = tuple(int(start_rgb[j] + t*(end_rgb[j] - start_rgb[j])) for j in range(3))
        
        # Convert RGB back to hex format and add to list
        colors.append('#{:02X}{:02X}{:02X}'.format(*rgb))
    
    return colors  # return list of gradient colors

def bfs(root):
    """
    Perform breadth-first search (BFS) traversal of a binary tree.
    
    BFS visits nodes level by level, starting from the root and moving downward.
    Uses a queue (FIFO - First In First Out) data structure to manage which nodes
    to visit next. This guarantees that all nodes at level n are visited before
    any node at level n+1.
    
    Time Complexity: O(n) where n is the number of nodes
    Space Complexity: O(n) for the queue (worst case: complete binary tree)
    
    Args:
        root: The root node of the binary tree to traverse
    
    Returns:
        list: List of nodes in breadth-first order
    """
    # Initialize queue with root node
    queue = deque([root])
    visited = []  # accumulate visited nodes in order
    
    # Process nodes until queue is empty
    while queue:
        node = queue.popleft()  # remove and process first node in queue
        visited.append(node)  # record as visited
        
        # Add children to queue for future processing (level-order)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    return visited  # return all nodes in BFS order

def dfs(root):
    """
    Perform depth-first search (DFS) traversal of a binary tree.
    
    DFS explores as far as possible along each branch before backtracking.
    Uses a stack (LIFO - Last In First Out) data structure. To maintain
    a consistent left-to-right order, we add the right child first, then
    the left child (so left is popped first).
    
    Time Complexity: O(n) where n is the number of nodes
    Space Complexity: O(h) where h is the height (for the call stack)
    
    Args:
        root: The root node of the binary tree to traverse
    
    Returns:
        list: List of nodes in depth-first order (pre-order variant)
    """
    # Initialize stack with root node
    stack = [root]
    visited = []  # accumulate visited nodes in order
    
    # Process nodes until stack is empty
    while stack:
        node = stack.pop()  # remove and process top node from stack
        visited.append(node)  # record as visited
        
        # Add children to stack (right first, then left for proper order)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return visited  # return all nodes in DFS order

def animate_three_trees(root):
    """
    Create an animated visualization comparing BFS and DFS traversals.
    
    Displays three side-by-side subplots:
    1. Original tree: Static view of the tree structure with all nodes in uniform color
    2. BFS tree: Animates node colors to show breadth-first traversal order
    3. DFS tree: Animates node colors to show depth-first traversal order
    
    The animation progresses frame by frame, coloring nodes in the order they are
    visited by each traversal algorithm. Dark blue nodes are visited early, light
    blue nodes are visited later.
    
    Args:
        root: The root node of the binary tree to visualize and animate
    
    The animation runs with 800ms interval between frames and does not repeat.
    """
    # Create figure with 3 subplots (one for each tree view)
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    
    # Build original tree graph
    tree_orig = nx.DiGraph()
    pos_orig = {root.id: (0, 0)}  # root position at origin
    add_edges(tree_orig, root, pos_orig)  # recursively add all nodes and edges
    labels_orig = {n[0]: n[1]['label'] for n in tree_orig.nodes(data=True)}  # extract node labels

    # Build BFS tree (same structure as original, will color differently)
    tree_bfs = nx.DiGraph()
    pos_bfs = {root.id: (0, 0)}
    add_edges(tree_bfs, root, pos_bfs)
    labels_bfs = {n[0]: n[1]['label'] for n in tree_bfs.nodes(data=True)}

    # Build DFS tree (same structure as original, will color differently)
    tree_dfs = nx.DiGraph()
    pos_dfs = {root.id: (0, 0)}
    add_edges(tree_dfs, root, pos_dfs)
    labels_dfs = {n[0]: n[1]['label'] for n in tree_dfs.nodes(data=True)}

    # Perform traversals to get visit order
    bfs_nodes = bfs(root)  # get nodes in BFS order
    dfs_nodes = dfs(root)  # get nodes in DFS order

    # Generate color gradients for visualization
    bfs_colors = generate_colors(len(bfs_nodes))  # dark to light gradient for BFS
    dfs_colors = generate_colors(len(dfs_nodes))  # dark to light gradient for DFS
    node_ids_bfs = [n.id for n in bfs_nodes]  # convert nodes to IDs for color lookup
    node_ids_dfs = [n.id for n in dfs_nodes]  # convert nodes to IDs for color lookup

    def update(frame):
        """
        Animation update function called for each frame.
        
        Clears the subplots and redraws all three trees, progressively coloring
        nodes based on their visit order.
        
        Args:
            frame: Current frame number (0 to max traversal length)
        """
        # Clear all subplots for redrawing
        axs[0].clear()
        axs[1].clear()
        axs[2].clear()
        
        # Draw original tree - static, all nodes in default light blue color
        nx.draw(tree_orig, pos_orig, labels=labels_orig, arrows=False,
                node_color="#90CAF9", node_size=1200, ax=axs[0])
        axs[0].set_title("Original Heap Tree")

        # Draw BFS tree - progressively color nodes based on visit order
        # Color nodes from index 0 to current frame in visit order
        for i in range(min(frame+1, len(node_ids_bfs))):
            tree_bfs.nodes[node_ids_bfs[i]]['color'] = bfs_colors[i]
        # Extract colors for all nodes in the graph
        colors_bfs_plot = [tree_bfs.nodes[n]['color'] for n in tree_bfs.nodes()]
        nx.draw(tree_bfs, pos_bfs, labels=labels_bfs, arrows=False,
                node_color=colors_bfs_plot, node_size=1200, ax=axs[1])
        axs[1].set_title("BFS Traversal")

        # Draw DFS tree - progressively color nodes based on visit order
        # Color nodes from index 0 to current frame in visit order
        for i in range(min(frame+1, len(node_ids_dfs))):
            tree_dfs.nodes[node_ids_dfs[i]]['color'] = dfs_colors[i]
        # Extract colors for all nodes in the graph
        colors_dfs_plot = [tree_dfs.nodes[n]['color'] for n in tree_dfs.nodes()]
        nx.draw(tree_dfs, pos_dfs, labels=labels_dfs, arrows=False,
                node_color=colors_dfs_plot, node_size=1200, ax=axs[2])
        axs[2].set_title("DFS Traversal")

    # Create animation that calls update function for each frame
    # Number of frames equals the longer traversal, 800ms interval between frames
    ani = FuncAnimation(fig, update, frames=max(len(bfs_nodes), len(dfs_nodes)),
                        interval=800, repeat=False)
    plt.show()  # display the animated visualization

if __name__ == "__main__":
    # Example min-heap array: [1, 3, 5, 7, 9, 11, 13]
    # This creates a complete binary tree with minimal value at root
    heap_array = [1, 3, 5, 7, 9, 11, 13]  # min-heap example
    
    # Convert heap array to binary tree structure
    root = build_heap_tree(heap_array)
    
    # Display animated comparison of BFS vs DFS traversal
    animate_three_trees(root)
