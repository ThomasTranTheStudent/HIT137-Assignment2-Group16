

import turtle
def main():
    #Ask for user input
    left_angle = float(input("Enter left branch angle: "))
    right_angle = float(input("Enter right branch angle: "))
    branch_length = float(input("Enter starting branch length: "))
    depth = int(input("Enter recursion depth: "))
    reduction_factor = float(input("Enter branch length reduction factor: "))

    #Call the draw_tree function with user inputs
    draw_tree(branch_length, left_angle, right_angle, depth, reduction_factor)

def draw_branch(t, branch_length, left_angle, right_angle, depth, reduction_factor):
    if depth == 0:
        return
    
    # Draw the main branch
    
    t.color("green")
    t.forward(branch_length)
    
    # Draw left branch
    t.left(left_angle)
    draw_branch(t, branch_length * reduction_factor, left_angle, right_angle, depth - 1, reduction_factor)
    t.right(left_angle)
    
    # Draw right branch
    t.right(right_angle)
    draw_branch(t, branch_length * reduction_factor, left_angle, right_angle, depth - 1, reduction_factor)
    t.left(right_angle)
    
    # Move back to previous position
    t.backward(branch_length)

def draw_tree(branch_length=100, left_angle=20, right_angle=25, depth=5, reduction_factor=0.7):
 
    # Initialize turtle
    screen = turtle.Screen()
    screen.bgcolor("white")
    t = turtle.Turtle()
    # t.color("red")
    # t.left(90)
    # t.forward(100)
    t.left(90)
    
    # Draw the tree
    draw_branch(t, branch_length, left_angle, right_angle, depth, reduction_factor)
    
    # Keep window open
    screen.mainloop()

if __name__ == "__main__":
    main()