import heapq

def merge_k_lists(lists):
    """
    Merges k sorted lists into one sorted list using a min-heap.
    
    Args:
        lists: list of sorted lists
        
    Returns:
        one sorted list
    """
    if not lists or not any(lists):
        return []
    
    # Min-heap: (value, list_index, element_index_in_list)
    min_heap = []
    
    # Add first element of each non-empty list
    for i, lst in enumerate(lists):
        if lst:  # if list is not empty
            heapq.heappush(min_heap, (lst[0], i, 0))
    
    result = []
    
    while min_heap:
        # Extract the smallest element
        val, list_idx, elem_idx = heapq.heappop(min_heap)
        result.append(val)
        
        # Add next element from the same list, if it exists
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(min_heap, (next_val, list_idx, elem_idx + 1))
    
    return result


# Example of usage
if __name__ == "__main__":
    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    print("Input lists:", lists)
    
    merged_list = merge_k_lists(lists)
    print("Sorted list:", merged_list)
    
    print("\nStep by step:")
    lists_step = [[1, 4, 5], [1, 3, 4], [2, 6]]
    heap = []
    
    # Initial heap
    for i, lst in enumerate(lists_step):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
    print(f"Initial heap: {heap}")
    
    result_step = []
    steps = 0
    while heap and steps < 8:  # show first 8 steps
        val, list_idx, elem_idx = heapq.heappop(heap)
        result_step.append(val)
        print(f"Taken {val} (list {list_idx}, position {elem_idx}), result: {result_step}")
        
        if elem_idx + 1 < len(lists_step[list_idx]):
            next_val = lists_step[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
            print(f"Added next: {next_val}")
        steps += 1
