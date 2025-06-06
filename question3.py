

import turtle
def main():
    #Ask for user input for tree parameters
    left_angle = float(input("Enter left branch angle: "))
    right_angle = float(input("Enter right branch angle: "))
    branch_length = float(input("Enter starting branch length: "))
    depth = int(input("Enter recursion depth: "))
    reduction_factor = float(input("Enter branch length reduction factor: "))

    #Call the draw_tree function with user inputs
    draw_tree(branch_length, left_angle, right_angle, depth, reduction_factor)

def draw_branch(t, branch_length, left_angle, right_angle, depth, reduction_factor, original_depth):
    # Set the pen size based on branch length
    t.pensize(branch_length * 0.1)
    #Base case for recursion
    if depth == 0:
        return
    
    # Draw the branch and check whether it is the not tree trunl
    if depth < original_depth:
        t.color("green")
    t.forward(branch_length)
    
    # Draw left branch
    t.left(left_angle)
    # Recursive call for left branch
    draw_branch(t, branch_length * reduction_factor, left_angle, right_angle, depth - 1, reduction_factor, original_depth)
    t.right(left_angle)
    
    # Draw right branch
    t.right(right_angle)
    # Recursive call for right branch
    draw_branch(t, branch_length * reduction_factor, left_angle, right_angle, depth - 1, reduction_factor, original_depth)
    t.left(right_angle)
    # Move back to brown color when tree trunk is reached at the end of the recursion
    if depth == original_depth:
        t.color("brown")
    
    # Move back to previous position
    t.backward(branch_length)

def draw_tree(branch_length=100, left_angle=20, right_angle=25, depth=5, reduction_factor=0.7):
 
    # Initialize turtle
    screen = turtle.Screen()
    screen.bgcolor("white")
    t = turtle.Turtle()
    
    
    # Store the original depth for color change
    original_depth = depth
    #Set initial color and orientation of the turtle
    t.left(90)
    t.color("brown")
    t.pensize(branch_length * 0.1)
    
    # Draw the tree
    draw_branch(t, branch_length, left_angle, right_angle, depth, reduction_factor, original_depth)
    
    # Keep window open
    screen.mainloop()

if __name__ == "__main__":
    main()