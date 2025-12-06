# Simple implementation of a binary search tree node
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


# Insert into binary search tree
def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    # if key == root.key, do nothing (avoid duplicates)
    return root


# Function that finds the minimum value in BST / AVL tree
def find_min(root):
    """
    Returns the minimum value in the tree.
    If the tree is empty, returns None.
    """
    if root is None:
        return None

    current = root
    # in BST and AVL tree the minimum element is in the leftmost node
    while current.left is not None:
        current = current.left
    return current.key


# Small demonstration of how it works
if __name__ == "__main__":
    # Create a tree and add elements
    values = [15, 10, 20, 8, 12, 17, 25, 3]
    root = None
    for v in values:
        root = insert(root, v)

    min_value = find_min(root)
    print("Minimum value in the tree:", min_value)
