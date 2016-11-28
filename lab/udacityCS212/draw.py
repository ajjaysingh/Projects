import turtle

window = turtle.Screen()
window.bgcolor("blue")

br = turtle.Turtle()
br.shape("turtle")
br.color("red")

for x in range(90,360):
    print(x)
    br.right(10)
    br.forward(100)
    br.right(90)
    br.forward(100)
    br.right(90)
    br.forward(100)
    br.right(90)
    br.forward(100)
