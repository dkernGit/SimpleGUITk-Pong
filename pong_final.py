# Implementation of classic arcade game Pong

import simpleguitk as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    global LEFT, RIGHT
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    horizontal = random.randrange(2, 5)
    vertical = random.randrange(1, 4)
    
    if direction == RIGHT: 
        ball_vel = [horizontal, - vertical]
    else: 
        ball_vel = [- horizontal, - vertical]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(False)
    paddle1_pos = [[PAD_WIDTH/2, HEIGHT/2 - PAD_HEIGHT/2], # top of paddle1
                   [PAD_WIDTH/2, HEIGHT/2 + PAD_HEIGHT/2]]
    paddle2_pos = [[WIDTH - PAD_WIDTH/2, HEIGHT/2 - PAD_HEIGHT/2], # top of paddle2
                   [WIDTH - PAD_WIDTH/2, HEIGHT/2 + PAD_HEIGHT/2]]
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, BALL_RADIUS
    global LEFT, RIGHT
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White") # Left Gutter
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White") # Right Gutter
        
    # update ball horizontal
    ball_pos[0] += ball_vel[0]
    
    # Check if ball is colliding with Left or Right Gutter
    # determine whether paddle and ball collide
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH and ball_pos[1] > paddle1_pos[0][1] and ball_pos[1] < paddle1_pos[1][1]:
        ball_vel[0] = - ball_vel[0] * 1.1
    elif ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        score2 += 1
        spawn_ball(RIGHT)
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH and ball_pos[1] > paddle2_pos[0][1] and ball_pos[1] < paddle2_pos[1][1]:
        ball_vel[0] = - ball_vel[0] * 1.1        
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        score1 += 1
        spawn_ball(LEFT)
    # update ball vertical
    ball_pos[1] += ball_vel[1]
    
    # Check if ball is colliding with Top or Bottom and reflect
    if ball_pos[1] - BALL_RADIUS <= 0:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[1] = - ball_vel[1]    
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Yellow", "White")
        
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[0][1] + paddle1_vel > 0 and paddle1_pos[1][1] + paddle1_vel <= HEIGHT:
        paddle1_pos[0][1] += paddle1_vel
        paddle1_pos[1][1] += paddle1_vel
    
    if paddle2_pos[0][1] + paddle2_vel > 0 and paddle2_pos[1][1] + paddle2_vel <= HEIGHT:
        paddle2_pos[0][1] += paddle2_vel
        paddle2_pos[1][1] += paddle2_vel
    
    # draw paddles
    canvas.draw_line(paddle1_pos[0], paddle1_pos[1], PAD_WIDTH, "Red")
    canvas.draw_line(paddle2_pos[0], paddle2_pos[1], PAD_WIDTH, "Blue")
 
    # draw scores
    canvas.draw_text(str(score1), [WIDTH/2 - 38, 50], 30, "White")
    canvas.draw_text(str(score2), [WIDTH/2 + 20, 50], 30, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    vel = 4
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= vel
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += vel
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += vel
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= vel  
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0 
    paddle2_vel = 0
    
def restart_handler():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
restart_buton = frame.add_button('Restart', restart_handler)

# start frame
new_game()
frame.start()
