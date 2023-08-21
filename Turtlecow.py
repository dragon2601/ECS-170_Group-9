import turtle as t

# Set up the turtle
t.speed(1)
t.bgcolor("white")
t.title("Cow")

def go(x,y):
    t.penup()
    t.goto(x,y)
    t.pendown()

# Draw the head and mouth
t.circle(60)
go(-50,20)
t.seth(-50)
t.fillcolor("#F4C2C2")
t.begin_fill()
t.circle(70,100)
t.circle(50//2, 90)
t.circle(70,90)
t.circle(50//2, 90)
t.end_fill()

#drawing the nose
go(-30, 30)
t.seth(-50)
t.fillcolor("grey")
t.begin_fill()
t.circle(10,100)
t.circle(10//2, 90)
t.circle(10,90)
t.circle(10//2, 90)
t.end_fill()
go(30, 30)
t.seth(-50)
t.fillcolor("grey")
t.begin_fill()
t.circle(10,100)
t.circle(10//2, 90)
t.circle(10,90)
t.circle(10//2, 90)
t.end_fill()

#drawing the eyes

go(-30, 90)
t.seth(-120)
t.fillcolor("black")
t.begin_fill()
t.circle(20,100)
t.circle(10//2, 90)
t.circle(20,90)
t.circle(10//2, 90)
t.end_fill()
go(30, 90)
t.seth(-1200)
t.fillcolor("black")
t.begin_fill()
t.circle(20,100)
t.circle(10//2, 90)
t.circle(20,90)
t.circle(10//2, 90)
t.end_fill()


#drawing the ears


# Hide the turtle
t.penup()
t.done()
