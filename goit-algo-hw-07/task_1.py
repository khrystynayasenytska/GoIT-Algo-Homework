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


# Function that finds the maximum value in BST / AVL tree
def find_max(root):
    """
    Returns the maximum value in the tree.
    If the tree is empty, returns None.
    """
    if root is None:
        return None

    current = root
    # in BST and AVL tree the maximum element is in the rightmost node
    while current.right is not None:
        current = current.right
    return current.key


# Small demonstration of how it works
if __name__ == "__main__":
    # Create a tree and add elements
    values = [15, 10, 20, 8, 12, 17, 25, 19]
    root = None
    for v in values:
        root = insert(root, v)

    max_value = find_max(root)
    print("Maximum value in the tree:", max_value)
