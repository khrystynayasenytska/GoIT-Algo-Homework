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


# Recursive function that finds the sum of all values in the tree
def sum_tree(root):
    """
    Returns the sum of all values in the tree.
    If the tree is empty, returns 0.
    """
    if root is None:
        return 0
    # sum = value of current node +
    #       sum of left subtree +
    #       sum of right subtree
    return root.key + sum_tree(root.left) + sum_tree(root.right)


# Small demonstration of how it works
if __name__ == "__main__":
    # Create a tree and add elements
    values = [15, 10, 20, 8, 12, 17, 25]
    root = None
    for v in values:
        root = insert(root, v)

    total_sum = sum_tree(root)
    print("Sum of all values in the tree:", total_sum)
