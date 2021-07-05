# This is the main file of My Pong Project (MPP)

from tkinter import *
import MPPTable, MPPBall, MPPBat

# initialise global variables
LEFT_BOUNDARY = 3
MAX_GAME = 10
X_SPEED = 15
Y_SPEED = 10
score_left = 0
score_right = 0
first_serve = True

# ordering a window from the tkinter window factory
window = Tk()
window.title("My Pong")

my_table = MPPTable.Table(window, net_colour="green", vertical_net=True, net_width=2)
# my_table = MPPTable.Table(window, width=600, height=60, colour="black", net_colour="blue", horizontal_net=True, net_width=40)
RIGHT_BOUNDARY = my_table.width - 3

# order a ball from the ball factory
my_ball = MPPBall.Ball(MPPTable=my_table, x_speed=X_SPEED, y_speed=Y_SPEED, width=24, height=24, colour="cyan",
                       x_start=288, y_start=188)

# order a left and right bat from the bat factory
bat_L = MPPBat.Bat(table=my_table, width=15, height=100, x_posn=20, y_posn=150, colour="blue", y_speed=20)
bat_R = MPPBat.Bat(table=my_table, width=15, height=100, x_posn=575, y_posn=150, colour="yellow", y_speed=20)


#### functions:
def game_flow():
    global first_serve
    global score_left
    global score_right
    # wait for the first serve:
    if first_serve:
        my_ball.stop_ball()
        first_serve = False

    # detect if ball has hit the bats:
    bat_L.detect_collision(my_ball)
    bat_R.detect_collision(my_ball)

    # detect if the ball has hit the left wall:
    if my_ball.x_posn <= LEFT_BOUNDARY:
        reset_game_state()
        score_left = score_left + 1
        if score_left >= MAX_GAME:
            score_left, score_right = "W", "L"

        first_serve = True
        my_table.draw_score(score_left, score_right)

    # detect if the ball has hit the right wall:

    if my_ball.x_posn + my_ball.width >= RIGHT_BOUNDARY:
        reset_game_state()
        score_right = score_right + 1
        if score_right >= MAX_GAME:
            score_left, score_right = "L", "W"

        first_serve = True
        my_table.draw_score(score_left, score_right)

    my_ball.move_next()
    window.after(50, game_flow)


def reset_game_state():
    my_ball.stop_ball()
    my_ball.start_position()
    bat_L.start_position()
    bat_R.start_position()
    my_table.move_item(bat_L.rectangle, 20, 150, 35, 250)
    my_table.move_item(bat_R.rectangle, 575, 150, 590, 250)


# add restart_game function here:
def restart_game(master):
    global score_left
    global score_right
    my_ball.start_ball(x_speed=X_SPEED, y_speed=0)
    if score_left == "W" or score_left == "L":
        score_left = 0
        score_right = 0
    my_table.draw_score(score_left, score_right)


# bind the controls of the bats to keys on the keyboard
window.bind("a", bat_L.move_up)
window.bind("z", bat_L.move_down)
window.bind("<Up>", bat_R.move_up)
window.bind("<Down>", bat_R.move_down)

# bind restart to the spacebar
window.bind("<space>", restart_game)

# call the game_flow loop
game_flow()

# start the tkinter loop process
window.mainloop()
