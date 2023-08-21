import turtle as t

# Set up the turtle
t.speed(15)
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


#drawing the Horns
t.fillcolor("#968566")
go(-55,90)
t.seth(120)
t.begin_fill()
t.circle(-25,100)
t.seth(-110)
t.circle(25,70)
t.seth(-165)
t.circle(45,33)
t.end_fill()

t.fillcolor("#968566")
go(55,90)
t.seth(60)
t.begin_fill()
t.circle(25,100)
t.seth(-60)
t.circle(-25,70)
t.seth(-18)
t.circle(-45,30)
t.end_fill()

#Drawing the ears
#Right ear
go(60,70)
t.seth(-20)
t.fillcolor("#fab4b4")
t.begin_fill()
t.circle(20,80)
t.seth(120)
t.circle(30,82)
t.seth(-53)
t.circle(-70,25)
t.end_fill()

t.circle(-70,-15)
t.seth(22)
t.fillcolor("#6b6b6b")
t.begin_fill()
t.circle(-30,60)
t.seth(120)
t.circle(30,78)
t.end_fill()

#left ear
go(-60,70)
t.seth(-170)
t.fillcolor("#fab4b4")
t.begin_fill()
t.circle(-20,80)
t.seth(58)
t.circle(-30,82)
t.seth(-129)
t.circle(70,25)
t.end_fill()

t.circle(70,-15)
t.seth(150)
t.fillcolor("#6b6b6b")
t.begin_fill()
t.circle(30,60)
t.seth(58)
t.circle(-30,78)
t.end_fill()



# Hide the turtle
t.penup()
t.hideturtle()
t.done()
