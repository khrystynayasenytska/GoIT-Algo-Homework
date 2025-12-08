"""
Monte Carlo Simulation: Probability Analysis of Rolling Two Dice

This module demonstrates the Monte Carlo method - a computational technique that uses
random sampling to compute numerical results. We compare simulated probabilities
(Monte Carlo) with theoretical/analytical probabilities for rolling two standard dice.

The Monte Carlo method is particularly useful when:
- Analytical solutions are difficult or impossible to derive
- We need to understand behavior of complex systems
- We want to verify theoretical predictions with empirical data

Key Concepts:
- Monte Carlo Simulation: Repeat random experiment many times and analyze results
- Law of Large Numbers: As sample size increases, simulated results converge to true probabilities
- Two Dice Sums: Range from 2 (1+1) to 12 (6+6), with sum of 7 being most probable

Expected Results:
As the number of rolls increases, Monte Carlo probabilities should converge to the
exact analytical probabilities. A plot comparison shows this convergence visually.
"""

import random
import matplotlib.pyplot as plt

def monte_carlo_dice_simulation(num_rolls=1000000):
    """
    Monte Carlo simulation of rolling two dice.
    
    Simulates rolling two standard six-sided dice the specified number of times,
    collecting statistics on the frequency of each possible sum (2-12).
    
    The Monte Carlo method relies on:
    1. Performing the random experiment many times
    2. Collecting frequency data
    3. Converting frequencies to probabilities (frequency / total trials)
    
    Law of Large Numbers: With more rolls, simulated probabilities approach
    true mathematical probabilities.
    
    Args:
        num_rolls: Number of times to simulate rolling two dice (default: 1,000,000)
    
    Returns:
        tuple: (probabilities_dict, counts_dict)
            - probabilities_dict: {sum: probability} for each possible sum 2-12
            - counts_dict: {sum: frequency_count} for each possible sum 2-12
    """
    
    # Initialize dictionary to count frequency of each possible sum (2-12)
    # Keys are possible sums, values are initialized to 0
    sum_counts = {s: 0 for s in range(2, 13)}

    # Monte Carlo Simulation: Perform the random experiment many times
    for _ in range(num_rolls):
        # Simulate rolling first die (random integer 1-6)
        d1 = random.randint(1, 6)
        # Simulate rolling second die (random integer 1-6)
        d2 = random.randint(1, 6)
        # Calculate sum of the two dice
        total = d1 + d2
        # Increment counter for this sum
        sum_counts[total] += 1

    # Convert frequency counts to probabilities
    # Probability = Frequency / Total Trials
    probabilities = {s: count / num_rolls for s, count in sum_counts.items()}
    
    return probabilities, sum_counts


def analytical_probabilities():
    """
    Returns exact mathematical probabilities of sums when rolling two dice.
    
    These are THEORETICAL probabilities calculated from combinatorics:
    - Total possible outcomes when rolling two dice: 6 × 6 = 36
    - For each sum, count how many ways it can occur, then divide by 36
    
    Probability calculations:
    - Sum 2: Only (1,1) → 1 way → 1/36 ≈ 0.0278
    - Sum 3: (1,2), (2,1) → 2 ways → 2/36 ≈ 0.0556
    - Sum 4: (1,3), (2,2), (3,1) → 3 ways → 3/36 ≈ 0.0833
    - ...
    - Sum 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) → 6 ways → 6/36 ≈ 0.1667 (most probable!)
    - ...
    - Sum 12: Only (6,6) → 1 way → 1/36 ≈ 0.0278
    
    Note: These exact values are what the Monte Carlo simulation should converge to
    as the number of trials increases (Law of Large Numbers).
    
    Returns:
        dict: Mapping of each sum (2-12) to its exact probability as a fraction
    """
    # Total combinations = 6 * 6 = 36
    return {
        2: 1/36,    # One way: (1,1)
        3: 2/36,    # Two ways: (1,2), (2,1)
        4: 3/36,    # Three ways: (1,3), (2,2), (3,1)
        5: 4/36,    # Four ways: (1,4), (2,3), (3,2), (4,1)
        6: 5/36,    # Five ways: (1,5), (2,4), (3,3), (4,2), (5,1)
        7: 6/36,    # Six ways: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) - MOST PROBABLE!
        8: 5/36,    # Five ways: (2,6), (3,5), (4,4), (5,3), (6,2)
        9: 4/36,    # Four ways: (3,6), (4,5), (5,4), (6,3)
        10: 3/36,   # Three ways: (4,6), (5,5), (6,4)
        11: 2/36,   # Two ways: (5,6), (6,5)
        12: 1/36    # One way: (6,6)
    }


def print_comparison_table(mc_probs, analytic_probs):
    """
    Print a formatted comparison table of Monte Carlo vs Analytical probabilities.
    
    Displays side-by-side comparison showing:
    1. Monte Carlo probability (from simulation)
    2. Analytical probability (exact mathematical value)
    3. Difference/Error (how far off the simulation was)
    
    Lower differences indicate the simulation is more accurate. With more rolls,
    differences should decrease, demonstrating convergence to true probabilities.
    
    Args:
        mc_probs: Dictionary of Monte Carlo probabilities {sum: probability}
        analytic_probs: Dictionary of analytical probabilities {sum: probability}
    """
    print("Probability Comparison (Monte Carlo vs Analytical)\n")
    # Print table header with column names and alignment
    print(f"{'Sum':<5} {'MC Probability':<20} {'Analytical':<15} {'Difference'}")
    print("-" * 50)  # Separator line for readability
    
    # Iterate through all possible sums (2-12)
    for s in range(2, 13):
        # Get Monte Carlo probability for this sum
        mc = mc_probs[s]
        # Get analytical (exact) probability for this sum
        an = analytic_probs[s]
        # Calculate absolute error between simulation and exact value
        diff = abs(mc - an)
        # Print formatted row with all four values
        print(f"{s:<5} {mc:<20.6f} {an:<15.6f} {diff:.6f}")


def plot_results(mc_probs, analytic_probs):
    """
    Create a visualization comparing Monte Carlo and Analytical probabilities.
    
    Generates a line plot with two curves:
    1. Monte Carlo (circles): Simulated probabilities from random trials
    2. Analytical (squares): Exact mathematical probabilities
    
    The plot clearly shows how closely the simulation matches theory. With more
    trials, the Monte Carlo line should overlay the analytical line more closely,
    demonstrating the Law of Large Numbers in action.
    
    The characteristic "pyramid" shape shows that sum 7 is most probable, with
    probabilities decreasing toward the extremes (sums 2 and 12).
    
    Args:
        mc_probs: Dictionary of Monte Carlo probabilities {sum: probability}
        analytic_probs: Dictionary of analytical probabilities {sum: probability}
    """
    # Prepare data for plotting
    sums = list(range(2, 13))  # List of possible sums: [2, 3, 4, ..., 12]
    mc_values = [mc_probs[s] for s in sums]  # Extract MC probabilities in order
    analytic_values = [analytic_probs[s] for s in sums]  # Extract analytical probabilities in order

    # Create figure with specified size
    plt.figure(figsize=(10, 6))
    
    # Plot Monte Carlo line with circle markers
    plt.plot(sums, mc_values, marker="o", label="Monte Carlo Probability")
    
    # Plot Analytical line with square markers
    plt.plot(sums, analytic_values, marker="s", label="Analytical Probability")
    
    # Add title describing the plot
    plt.title("Dice Roll Probability Distribution (Monte Carlo vs Analytical)")
    
    # Label x-axis
    plt.xlabel("Sum of Two Dice")
    
    # Label y-axis
    plt.ylabel("Probability")
    
    # Enable grid for easier reading
    plt.grid(True)
    
    # Add legend to identify the two lines
    plt.legend()
    
    # Display the plot
    plt.show()


def main():
    """
    Main function orchestrating the Monte Carlo simulation and analysis.
    
    Workflow:
    1. Run Monte Carlo simulation with specified number of rolls
    2. Get analytical (exact) probabilities
    3. Display simulation results and frequency counts
    4. Print comparison table of simulated vs exact probabilities
    5. Visualize results with a plot showing both distributions
    
    The main purpose is to demonstrate that empirical results from simulation
    converge to theoretical expectations as sample size increases.
    """
    # Set number of dice rolls for simulation (adjust for accuracy vs speed tradeoff)
    # More rolls = more accurate simulation but slower execution
    # 200,000 rolls provides good accuracy while running quickly
    # For even better accuracy, increase to 1,000,000 (takes longer)
    NUM_ROLLS = 200000
    
    # Run the Monte Carlo simulation
    # Returns: probabilities dict and frequency counts dict
    mc_probs, counts = monte_carlo_dice_simulation(NUM_ROLLS)
    
    # Get the exact analytical (mathematical) probabilities
    analytic_probs = analytical_probabilities()

    # Display header with simulation details
    print(f"\nMONTE CARLO SIMULATION ({NUM_ROLLS} rolls)\n")
    
    # Display frequency counts for each sum
    # Shows raw count of how many times each sum occurred
    print("Counts:", counts)
    print()

    # Print formatted comparison table
    # Shows Monte Carlo probability vs Analytical probability vs Difference
    print_comparison_table(mc_probs, analytic_probs)

    # Display visualization comparing the two distributions
    plot_results(mc_probs, analytic_probs)

if __name__ == "__main__":
    # Entry point: Run the main program when this file is executed
    main()
