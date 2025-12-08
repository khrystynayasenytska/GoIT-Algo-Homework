# Task 7: Monte Carlo Simulation - Dice Roll Probability Analysis

## Overview

This task demonstrates the **Monte Carlo method** - a way to estimate probabilities by running many random experiments and analyzing the results. We compare the simulated results with exact mathematical calculations.

## What We're Doing

We roll two dice many times (200,000 times) and compare:
1. **Simulated Results** - What actually happened in our simulation
2. **Mathematical Results** - What should happen theoretically

## How It Works

### Exact Math (Analytical)

When rolling two dice, there are 36 possible outcomes (6 × 6).
- Sum 2: Only 1 way (1,1) → Probability = 1/36
- Sum 3: 2 ways (1,2 and 2,1) → Probability = 2/36
- Sum 4: 3 ways → Probability = 3/36
- ...
- **Sum 7: 6 ways** → Probability = 6/36 **(Most common!)**
- ...
- Sum 12: Only 1 way (6,6) → Probability = 1/36

| Sum | Ways to Get It | Probability |
|-----|---------------|------------|
| 2-6 | Increases | 1/36 to 5/36 |
| **7** | **6 ways** | **6/36 (16.67%)** |
| 8-12 | Decreases | 5/36 to 1/36 |

### Simulation (Monte Carlo)

1. Roll two dice 200,000 times
2. Count how many times each sum appears
3. Calculate probability = count / 200,000
4. Compare with exact math

## Algorithm

### Monte Carlo Simulation

```
1. Create counter for sums 2-12
2. Repeat 200,000 times:
   - Roll die 1 (random 1-6)
   - Roll die 2 (random 1-6)
   - Add them together
   - Increment counter for that sum
3. Convert counts to probabilities (divide by 200,000)
4. Compare with exact math
```

### Exact Calculation

Pre-calculate exact probabilities based on counting all 36 possible outcomes.

## Results and Conclusions 
**The simulation results match the exact math almost perfectly!**

#### 1. Sum 7 is Most Common

Both methods show:
- Sum 7 appears most often
- Probability = 6/36 ≈ **16.67%**
- This makes sense: 6 ways to roll a 7, but only 1 way to roll a 2 or 12

#### 2. Perfect Symmetry

- Sums on opposite sides are equally likely
- P(2) = P(12) - both are rarest
- P(3) = P(11) - both equally rare
- P(7) is peak in the middle

#### 3. Simulation Matches Math

Example results from 200,000 rolls:

| Sum | Simulation | Exact Math | Difference |
|-----|-----------|-----------|-----------|
| 2 | 0.0281 | 0.0278 | 0.0003 |
| 7 | 0.1667 | 0.1667 | ~0.0000 |
| 12 | 0.0285 | 0.0278 | 0.0007 |

**Differences are tiny!** 

#### 4. Why the Difference?

Small differences between simulation and exact math occur because:
- Simulation uses random sampling (won't be perfect)
- With 200,000 rolls, this is very close to exact values
- With more rolls, differences become even smaller

### Why This Matters

 **Simulation works!** The Monte Carlo method gives accurate results
 **We proved it!** By comparing with exact mathematical calculations
 **Both are valid** - Use each when appropriate:
- Need exact answer? Use math
- Can't solve with math? Use simulation
