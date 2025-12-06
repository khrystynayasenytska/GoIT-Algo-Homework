# Cash Register Change System - Greedy vs Dynamic Programming

## Overview

This project implements and compares two different algorithmic approaches to solve the **coin change problem**: finding the optimal way to make change using available coin denominations.

### Problem Statement
Given a set of coin denominations `[50, 25, 10, 5, 2, 1]` and an amount of money, find the minimum number of coins needed to make that amount.

## Algorithms Implemented

### 1. **Greedy Algorithm** 
**Approach:** Always select the largest coin that doesn't exceed the remaining amount.

```python
def find_coins_greedy(amount: int) -> Dict[int, int]:
```

**How it works:**
1. Sort coins in descending order
2. For each coin, use as many as possible
3. Move to the next smaller coin
4. Repeat until the amount is covered

**Characteristics:**
- **Fast**: O(n) time complexity where n = number of coin denominations
- **Simple**: Easy to understand and implement
- **Not always optimal**: May not find the absolute minimum for all coin systems
- **Optimal for standard currency**: Works perfectly for most real-world coin systems

**Example:**
```
Amount: 113
Greedy Result: {50: 2, 10: 1, 2: 1, 1: 1} = 5 coins
```

### 2. **Dynamic Programming Algorithm** 
**Approach:** Build up solutions for all amounts from 0 to the target, finding the minimum coins for each.

```python
def find_min_coins(amount: int) -> Dict[int, int]:
```

**How it works:**
1. Create a DP array where `dp[i]` = minimum coins needed for amount i
2. For each amount from 1 to target:
   - Try using each coin denomination
   - Keep track of the combination that uses fewest coins
3. Return the optimal combination for the target amount

**Characteristics:**
- **Always optimal**: Guarantees the minimum number of coins
- **Slower**: O(amount × n) time complexity
- **More memory**: Stores state for all intermediate amounts
- **Universal**: Works for any coin system

**Example:**
```
Amount: 113
DP Result: {50: 2, 10: 1, 2: 1, 1: 1} = 5 coins
```

## Code Structure

### Main Functions

#### `find_coins_greedy(amount: int) -> Dict[int, int]`
Returns a dictionary mapping coin denomination to quantity using the greedy approach.

#### `find_min_coins(amount: int) -> Dict[int, int]`
Returns a dictionary mapping coin denomination to quantity using dynamic programming.

#### `compare_algorithms(test_amounts: list) -> None`
Benchmarks both algorithms on multiple test amounts, showing execution time and coin count.

## Usage

### Basic Example
```python
from task_1 import find_coins_greedy, find_min_coins

# Using Greedy Algorithm
amount = 113
greedy_result = find_coins_greedy(amount)
print(f"Greedy: {greedy_result}")  # {50: 2, 10: 1, 2: 1, 1: 1}

# Using Dynamic Programming
dp_result = find_min_coins(amount)
print(f"DP: {dp_result}")  # {50: 2, 10: 1, 2: 1, 1: 1}
```

## Performance Comparison

### Time Complexity

| Algorithm | Time | Space | Optimal? |
|-----------|------|-------|----------|
| **Greedy** | O(n) | O(n) | For standard currency |
| **Dynamic Programming** | O(amount × n) | O(amount) | Always |

### When to Use Each

**Use Greedy When:**
- Working with standard currency denominations
- Speed is critical
- Optimal solution is guaranteed (like most real-world coins)

**Use Dynamic Programming When:**
- Any coin system is possible
- Guaranteed optimal solution is required
- Amount is relatively small
- Performance is less critical than correctness

## Key Insights

### For Amount = 113

Both algorithms produce the same result for this standard coin system:
- **2 coins of 50** (total: 100)
- **1 coin of 10** (total: 110)
- **1 coin of 2** (total: 112)
- **1 coin of 1** (total: 113)

**Total: 5 coins**

### Why They're the Same

For the standard currency system `[50, 25, 10, 5, 2, 1]`, the greedy approach is mathematically optimal. This is because the coin denominations form a **canonical coin system** where greedy always produces the minimum number of coins.

## Edge Cases

- **amount = 0**: Returns empty dictionary `{}`
- **amount = 1**: Returns `{1: 1}`
- **Large amounts**: DP becomes slower but still finds optimal solution

## Learning Outcomes

This project demonstrates:
1. Greedy algorithm design and implementation
2. Dynamic programming approach to optimization
3. Algorithm performance analysis and comparison
4. Time and space complexity trade-offs
5. When to choose which algorithm
