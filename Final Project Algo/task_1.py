class Node:
    """Node of singly linked list"""
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList:
    """Singly linked list"""
    def __init__(self):
        self.head = None
    
    def append(self, data):
        """Add element to end of list"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def __str__(self):
        """String representation of list"""
        nodes = []
        current = self.head
        visited = set()  # Track visited nodes to detect cycles
        while current and current not in visited:
            visited.add(current)
            nodes.append(str(current.data))
            current = current.next
        return " -> ".join(nodes)

def reverse_list(head):
    """
    Reverse singly linked list by changing references.
    Time Complexity: O(n), Space Complexity: O(1)
    """
    prev = None
    current = head
    while current:
        # Save next node before changing reference
        next_node = current.next
        # Reverse the link
        current.next = prev
        # Move forward
        prev = current
        current = next_node
    return prev

def insertion_sort(head):
    """
    Sort singly linked list using insertion sort algorithm.
    Time Complexity: O(n²), Space Complexity: O(1)
    Stable sorting algorithm.
    """
    if not head or not head.next:
        return head
    
    # Initialize sorted list with None
    sorted_head = None 
    
    # Process each node from original list
    current = head
    while current:
        # Save next node before modifying current
        next_node = current.next 
        
        # Insert current node into sorted list
        if sorted_head is None or current.data < sorted_head.data:
            # Insert at beginning
            current.next = sorted_head
            sorted_head = current
        else:
            # Find correct position in sorted list
            sorted_current = sorted_head
            while sorted_current.next and sorted_current.next.data < current.data:
                sorted_current = sorted_current.next
            # Insert current node
            current.next = sorted_current.next
            sorted_current.next = current
        
        # Move to next node from original list
        current = next_node 
    
    return sorted_head

def merge_sorted_lists(list1, list2):
    """
    Merge two sorted linked lists into one sorted list.
    Time Complexity: O(n + m), Space Complexity: O(1)
    where n and m are lengths of the two lists.
    """
    # Create dummy node to simplify merge logic
    dummy = Node(0)
    current = dummy
    
    # Compare and merge both lists
    while list1 and list2:
        if list1.data <= list2.data:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
    
    # Attach remaining nodes from either list
    current.next = list1 or list2
    return dummy.next

def print_list(head, title="List"):
    """
    Print linked list with safety check for cycles.
    Limits output to 20 nodes to prevent infinite loops.
    """
    print(f"\n{title}:")
    current = head
    count = 0
    visited = set()
    while current and current not in visited and count < 20:
        visited.add(current)
        print(f"  {current.data}", end=" -> " if current.next else "\n")
        current = current.next
        count += 1
    if count >= 20:
        print("  ... (limited to 20 nodes)")


def test_fixed():
    """Test all singly linked list operations"""
    print("Testing Singly Linked List Operations")
    
    # Create and populate first list
    lst = SinglyLinkedList()
    lst.append(5); lst.append(2); lst.append(8); lst.append(1); lst.append(9)
    print_list(lst.head, "1. Initial list")
    
    # Test reverse operation
    rev_head = reverse_list(lst.head)
    print_list(rev_head, "2. After reverse")
    
    # Test insertion sort
    sorted_head = insertion_sort(rev_head)
    print_list(sorted_head, "3. After insertion sort")
    
    # Create second sorted list
    lst2 = SinglyLinkedList()
    lst2.append(3); lst2.append(4); lst2.append(6); lst2.append(7)
    print_list(lst2.head, "4. Second sorted list")
    
    # Test merge operation
    merged = merge_sorted_lists(sorted_head, lst2.head)
    print_list(merged, "5. Merged sorted list")

if __name__ == "__main__":
    test_fixed()
