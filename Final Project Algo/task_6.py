"""
Food Selection Problem: Comparison of Greedy and Dynamic Programming Approaches

This module solves the classic food selection problem where we need to maximize
calories within a given budget constraint. Two different algorithmic approaches
are implemented and compared:

1. GREEDY ALGORITHM:
   - Selects items based on calories-to-cost ratio (calories per currency unit)
   - Does NOT guarantee optimal solution for this problem
   - Time Complexity: O(n log n) due to sorting
   - Space Complexity: O(n)
   - Fast but can miss better combinations

2. DYNAMIC PROGRAMMING:
   - Uses a 2D DP table where DP[i][c] represents maximum calories using
     first i items with exactly c budget available
   - GUARANTEES optimal solution (0/1 knapsack problem)
   - Time Complexity: O(n * budget)
   - Space Complexity: O(n * budget)
   - Slower but finds the best possible selection
"""

# Dictionary of available food items with their properties
# Each item has a cost and calorie value
items = {
    "pizza": {"cost": 50, "calories": 300},        # High cost, good calories
    "hamburger": {"cost": 40, "calories": 250},    # Medium-high cost
    "hot-dog": {"cost": 30, "calories": 200},      # Medium cost
    "pepsi": {"cost": 10, "calories": 100},        # Low cost, low calories
    "cola": {"cost": 15, "calories": 220},         # Low-medium cost, decent calories
    "potato": {"cost": 25, "calories": 350}        # Best ratio: 14 calories per unit cost
}

#  GREEDY ALGORITHM
def greedy_algorithm(items, budget):
    """
    Greedy Algorithm for Food Selection Problem.
    
    Uses a greedy approach based on calories-per-cost ratio. Sorts items by
    their efficiency (calories per unit cost) in descending order and greedily
    selects items starting with the most efficient ones until budget runs out.
    
    This approach is NOT guaranteed to find the optimal solution, as some
    combinations of less efficient items might together provide more calories
    than the greedy selection.
    
    Args:
        items: Dictionary with food items as keys and dicts with 'cost' and 'calories'
        budget: Maximum total cost we can spend
    
    Returns:
        tuple: (selected_items_list, total_calories, total_cost_spent)
    """
    # Create array of tuples: (name, cost, calories, calories_per_cost_ratio)
    # The ratio helps us determine which items give the best value
    arr = [
        (name, data["cost"], data["calories"], data["calories"] / data["cost"])
        for name, data in items.items()
    ]

    # Sort items by calories-per-cost ratio in descending order
    # Items with highest ratio (best value) appear first
    arr.sort(key=lambda x: x[3], reverse=True)

    chosen = []  # List to store selected item names
    total_cal = 0  # Accumulate total calories
    spent = 0  # Accumulate total cost spent

    # Iterate through items in order of efficiency
    for name, cost, cal, ratio in arr:
        # If we can afford this item without exceeding budget
        if spent + cost <= budget:
            chosen.append(name)  # Add to selection
            spent += cost  # Update spent amount
            total_cal += cal  # Update calorie total

    # Return selected items, total calories obtained, and total cost
    return chosen, total_cal, spent


def dynamic_programming(items, budget):
    """
    Dynamic Programming Solution for Food Selection (0/1 Knapsack Problem).
    
    Uses a 2D DP table where DP[i][c] represents the maximum calories achievable
    using the first i items with a budget of exactly c currency units.
    
    The recurrence relation is:
    - If item cost > budget: DP[i][c] = DP[i-1][c] (can't use this item)
    - Otherwise: DP[i][c] = max(DP[i-1][c], DP[i-1][c-cost] + calories)
                           = max(skip this item, take this item)
    
    This approach GUARANTEES finding the optimal solution by considering all
    possible combinations in a systematic way.
    
    Time Complexity: O(n * budget) where n is number of items
    Space Complexity: O(n * budget) for the DP table
    
    Args:
        items: Dictionary with food items as keys and dicts with 'cost' and 'calories'
        budget: Maximum total cost we can spend
    
    Returns:
        tuple: (selected_items_list, max_calories_possible)
    """
    # Get list of item names and count
    names = list(items.keys())
    n = len(names)

    # Initialize DP table with dimensions (n+1) x (budget+1)
    # DP[i][c] = max calories using items 0...i-1 with budget c
    # Row 0 and column 0 are initialized to 0 (base case)
    DP = [[0] * (budget + 1) for _ in range(n + 1)]

    # Fill DP table bottom-up
    for i in range(1, n + 1):
        # Get current item information (convert from 0-indexed to 1-indexed)
        name = names[i - 1]
        cost = items[name]["cost"]
        cal = items[name]["calories"]

        # For each possible budget amount
        for c in range(budget + 1):
            # If item cost exceeds current budget, we cannot take it
            if cost > c:
                DP[i][c] = DP[i - 1][c]  # skip this item
            else:
                # We have two choices: skip the item or take the item
                # Skip: DP[i-1][c] (best solution without current item)
                # Take: DP[i-1][c-cost] + cal (best solution with this item added)
                # Choose the option that gives more calories
                DP[i][c] = max(DP[i - 1][c], DP[i - 1][c - cost] + cal)

    # Reconstruct which items were chosen by backtracking through DP table
    # Start from bottom-right: DP[n][budget] (best solution with full budget)
    chosen = []
    c = budget
    # Work backwards from last item to first item
    for i in range(n, 0, -1):
        # If value changed from previous row, this item was included
        if DP[i][c] != DP[i - 1][c]:
            # Retrieve the item that was added
            name = names[i - 1]
            chosen.append(name)
            # Reduce remaining budget by the cost of this item
            c -= items[name]["cost"]

    # Reverse to get items in original order (we traced backwards)
    chosen.reverse()
    
    # Return selected items and maximum calories achievable
    return chosen, DP[n][budget]


#  MAIN PROGRAM
if __name__ == "__main__":
    # Set budget constraint for food selection
    budget = 100  # You may change this value to test different budgets

    print(" BUDGET:", budget, "\n")

    g_items, g_cal, g_cost = greedy_algorithm(items, budget)
    
    print("GREEDY ALGORITHM")
    print("Selected:", g_items)  # Items selected by greedy approach
    print("Calories:", g_cal)     # Total calories obtained
    print("Cost:", g_cost)        # Total cost of selected items
    print()

    dp_items, dp_cal = dynamic_programming(items, budget)
    
    print("DYNAMIC PROGRAMMING")
    print("Selected:", dp_items)  # Items selected by DP (optimal solution)
    print("Calories:", dp_cal)     # Maximum calories possible
    # Calculate and print total cost of DP selection
    print("Cost:", sum(items[name]["cost"] for name in dp_items))

    
