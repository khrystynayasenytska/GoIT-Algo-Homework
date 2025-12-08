import turtle
import math

def draw_branch(t, x, y, angle, length, level):
    """
    Recursive function to draw classic Pythagoras Tree with branches (not squares).
    Uses line segments instead of squares for a more natural tree appearance.
    
    Parameters:
    t: turtle object
    x, y: starting position
    angle: direction angle in degrees
    length: length of current branch
    level: recursion depth
    """
    if level == 0:
        return
    
    # Calculate end point of current branch
    x_end = x + length * math.cos(math.radians(angle))
    y_end = y + length * math.sin(math.radians(angle))
    
    # Draw the branch line
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.goto(x_end, y_end)
    
    # Calculate length for next branches (scaled by sqrt(2)/2)
    new_length = length * math.sqrt(2) / 2
    
    # Left branch (rotate 45 degrees counterclockwise)
    draw_branch(t, x_end, y_end, angle + 45, new_length, level - 1)
    
    # Right branch (rotate 45 degrees clockwise)
    draw_branch(t, x_end, y_end, angle - 45, new_length, level - 1)


def main():
    """Main function to run the Pythagoras Tree (branch style) visualization"""
    screen = turtle.Screen()
    screen.setup(1200, 1000)
    screen.bgcolor("white")
    screen.title("Fractal: Pythagoras Tree - Branch Style")

    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.color("darkred")
    t.pensize(1.5)

    # Starting parameters
    start_x = 0
    start_y = -400
    start_angle = 90  # Point upward
    initial_length = 150

    # Get recursion level from user
    level = int(screen.numinput("Recursion Level", 
                                "Enter recursion level (1-12):", 
                                default=10, minval=1, maxval=12))

    # Build the Pythagoras Tree with branches
    draw_branch(t, start_x, start_y, start_angle, initial_length, level)

    screen.mainloop()

if __name__ == "__main__":
    main()
