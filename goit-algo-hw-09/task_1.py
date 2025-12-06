"""
Cash register system for optimal change delivery.
Implemented greedy algorithm and dynamic programming for coin change problem.
"""

import time
from typing import Dict

COINS = [50, 25, 10, 5, 2, 1]

def find_coins_greedy(amount: int) -> Dict[int, int]:
    """
    Greedy algorithm for change delivery.
    
    Selects the largest available coin denominations first.
    
    Args:
        amount: sum for change delivery
        
    Returns:
        dictionary {denomination: number of coins}
    """
    result = {}
    remaining = amount
    
    # Sort coins in descending order (largest first)
    for coin in sorted(COINS, reverse=True):
        if remaining >= coin:
            count = remaining // coin
            result[coin] = count
            remaining -= count * coin
    
    return result

def find_min_coins(amount: int) -> Dict[int, int]:
    """
    Dynamic programming for minimum number of coins.
    
    Finds optimal decomposition with the smallest number of coins.
    
    Args:
        amount: sum for change delivery
        
    Returns:
        dictionary {denomination: number of coins}
    """
    if amount == 0:
        return {}
    
    # dp[i] = minimum number of coins for sum i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    # coin_used[i] stores the combination of coins for sum i
    coin_used = [{} for _ in range(amount + 1)]
    
    for i in range(1, amount + 1):
        for coin in COINS:
            if i >= coin and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                # Copy combination from previous state
                coin_used[i] = coin_used[i - coin].copy()
                # Add current coin
                coin_used[i][coin] = coin_used[i].get(coin, 0) + 1
    
    return coin_used[amount]

def compare_algorithms(test_amounts: list) -> None:
    """
    Compares performance of both algorithms on test amounts.
    """
    print("ALGORITHM COMPARISON")
    print(f"{'Amount':<8} {'Greedy':<12} {'DP':<10} {'Coins Greedy':<12} {'Coins DP'}")
    
    for amount in test_amounts:
        # Greedy algorithm
        start_greedy = time.time()
        greedy_result = find_coins_greedy(amount)
        greedy_time = (time.time() - start_greedy) * 1000  # milliseconds
        greedy_coins = sum(greedy_result.values())
        
        # Dynamic programming
        start_dp = time.time()
        dp_result = find_min_coins(amount)
        dp_time = (time.time() - start_dp) * 1000  # milliseconds
        dp_coins = sum(dp_result.values())
        
        print(f"{amount:<8} {greedy_time:<12.3f} {dp_time:<10.3f} "
              f"{greedy_coins:<12} {dp_coins}")

if __name__ == "__main__":
    # Test for example from task
    amount = 113
    print("TEST FOR SUM 113")
    print(f"Greedy algorithm: {find_coins_greedy(amount)}")
    print(f"Dynamic programming: {find_min_coins(amount)}")
    print()
    
    # Performance comparison
    test_amounts = [30, 113, 250, 1000, 5000]
    compare_algorithms(test_amounts)
    
    print("\nTIME COMPLEXITY:")
    print("Greedy: O(n), where n is the number of coin denominations (fast)")
    print("Dynamic programming: O(amount × n) (slower for large amounts)")
