import heapq

def min_cost_to_connect_cables(cables):
    """
    Finds the minimum cost to connect all cables.
    
    Args:
        cables: list of cable lengths
        
    Returns:
        minimum total cost
    """
    if len(cables) <= 1:
        return 0
    
    # Create a min-heap
    heapq.heapify(cables)
    total_cost = 0
    
    while len(cables) > 1:
        # Extract two smallest cables
        first = heapq.heappop(cables)
        second = heapq.heappop(cables)
        
        # Cost to connect = sum of lengths
        connection_cost = first + second
        total_cost += connection_cost
        
        # Push new cable back to heap
        heapq.heappush(cables, connection_cost)
    
    return total_cost


# Example of how it works
if __name__ == "__main__":
    # Test data: [4, 3, 2, 6]
    cables = [4, 3, 2, 6]
    print(f"Cables: {cables}")
    
    result = min_cost_to_connect_cables(cables.copy())
    print(f"Minimum cost: {result}")  # Expected 29
    
    print("\nStep by step:")
    cables = [4, 3, 2, 6]
    heapq.heapify(cables)
    print(f"Initial heap: {cables}")
    
    total = 0
    while len(cables) > 1:
        first = heapq.heappop(cables)
        second = heapq.heappop(cables)
        cost = first + second
        total += cost
        heapq.heappush(cables, cost)
        print(f"Connected {first}+{second}={cost}, total_cost={total}, heap={cables}")
