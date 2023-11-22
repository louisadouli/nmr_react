import turtle

class MyTurtle(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.speed(0)  # Set the turtle's speed to the fastest
        self.shape("turtle")  # Set the turtle's shape to "turtle"

        # Bind arrow keys to turtle movement methods
        turtle.onkey(self.move_forward, "Up")
        turtle.onkey(self.move_backward, "Down")
        turtle.onkey(self.turn_left, "Left")
        turtle.onkey(self.turn_right, "Right")
        turtle.listen()  # Start listening for keyboard events

    def move_forward(self):
        self.forward(10)

    def move_backward(self):
        self.backward(10)

    def turn_left(self):
        self.left(10)

    def turn_right(self):
        self.right(10)

# Create an instance of MyTurtle class
t = MyTurtle()

# Keep the turtle graphics window open
turtle.done()