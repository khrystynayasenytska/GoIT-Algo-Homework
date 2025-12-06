"""
Task 1: Beverage Production Optimization using PuLP
Maximize total number of "Lemonade" + "Fruit Juice"
with resource constraints
"""

import pulp

def optimize_production():
    """
    Linear programming model for maximizing beverage production.
    
    Returns:
        dict: optimization results (product quantities, resources used, status)
    """
    
    # Create optimization problem (maximize)
    prob = pulp.LpProblem("Beverage_production_optimization", pulp.LpMaximize)
    
    # Decision variables: quantity of each product
    lemonade = pulp.LpVariable("Lemonade", lowBound=0, cat='Continuous')
    fruit_juice = pulp.LpVariable("Fruit_juice", lowBound=0, cat='Continuous')
    
    # Objective function: maximize total quantity of products
    prob += lemonade + fruit_juice, "Total_product_quantity"
    
    # Resource constraints
    # Water: 2*Lemonade + 1*Juice <= 100
    prob += 2 * lemonade + 1 * fruit_juice <= 100, "Water_constraint"
    
    # Sugar: 1*Lemonade <= 50
    prob += 1 * lemonade <= 50, "Sugar_constraint"
    
    # Lemon juice: 1*Lemonade <= 30
    prob += 1 * lemonade <= 30, "Lemon_juice_constraint"
    
    # Fruit puree: 2*Juice <= 40
    prob += 2 * fruit_juice <= 40, "Fruit_puree_constraint"
    
    # Run optimization
    prob.solve(pulp.PULP_CBC_CMD(msg=0))  # msg=0 removes log output
    
    # Results
    results = {
        'status': pulp.LpStatus[prob.status],
        'total_products': pulp.value(prob.objective),
        'lemonade': pulp.value(lemonade),
        'fruit_juice': pulp.value(fruit_juice),
        'resources_used': {
            'water': 2 * pulp.value(lemonade) + 1 * pulp.value(fruit_juice),
            'sugar': 1 * pulp.value(lemonade),
            'lemon_juice': 1 * pulp.value(lemonade),
            'fruit_puree': 2 * pulp.value(fruit_juice)
        }
    }
    
    return results

def print_detailed_results(results):
    """Outputs detailed optimization results."""
    print("OPTIMIZATION RESULTS")
    print(f"Solution status: {results['status']}")
    print(f"MAXIMUM TOTAL PRODUCT QUANTITY: {results['total_products']:.0f}")
    print()
    
    print("PRODUCTION:")
    print(f"   Lemonade: {results['lemonade']:.0f} units")
    print(f"   Fruit juice: {results['fruit_juice']:.0f} units")
    print()
    
    print("RESOURCES USED:")
    print(f"   Water: {results['resources_used']['water']:.0f}/100 units")
    print(f"   Sugar: {results['resources_used']['sugar']:.0f}/50 units")
    print(f"   Lemon juice: {results['resources_used']['lemon_juice']:.0f}/30 units")
    print(f"   Fruit puree: {results['resources_used']['fruit_puree']:.0f}/40 units")
    print()

if __name__ == "__main__":
    # Run optimization
    results = optimize_production()
    
    # Output results
    print_detailed_results(results)
    
    # Clear answer to the task requirement
    print("TASK ANSWER:")
    print(f"Maximum total number of products produced: {results['total_products']:.0f}")
